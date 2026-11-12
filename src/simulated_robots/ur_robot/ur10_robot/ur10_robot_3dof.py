import rclpy
import numpy as np
from rclpy.node import Node
from ur10_model.ur10_model_3dof import UR10Model3DOF
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Float64
from tf2_ros import TransformBroadcaster

from visualization_msgs.msg import Marker
# tf_transformations is not available in ROS 2 Jazzy, use SciPy for the quaternion
from scipy.spatial.transform import Rotation
import msbrdm_libs.ros_utils as ros_utils


class UR10Robot3DOF():
    """ A simulated RPPR robot that visualizes joint states and updates
    transformations with the model
    """

    def __init__(self, model: UR10Model3DOF, q_init: np.ndarray = None,
                 node: Node = None) -> None:
        # initialization
        self.model = model
        self.node = node

        # joint states: [q, qdot, qddot].T (3 x n)
        self.q = np.zeros(self.model.nq)
        if q_init is not None:
            self.q = q_init
        self.qdot = np.zeros(self.model.nq)
        self.qddot = np.zeros(self.model.nq)

        #######################################################################
        # TODO: Initialize the joint states publisher
        self.joint_states_pub = self.node.create_publisher(JointState, 'joint_states', 10)
        self.joint_msg = JointState()
        # the URDF has 6 joints, the last 3 stay fixed
        self.joint_msg.name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
                               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

        self.br = TransformBroadcaster(self.node)

        #######################################################################
        # TODO: Define the end-effector velocity publishers
        # Type: geometry_msgs/Twist
        self.ee_vel_from_J_pub = self.node.create_publisher(Twist, '/ee_vel_from_J', 10)
        # Type: geometry_msgs/Vector3
        self.ee_vel_from_num_diff_pub = self.node.create_publisher(Vector3, '/ee_vel_from_num_diff', 10)

        #######################################################################
        # ellispoid marker publisher
        self.marker_pub = node.create_publisher(Marker, "/manipulability_ellipsoid", 10)
        # manipulability index w, e.g. for plotting in PlotJuggler
        self.manipulability_pub = node.create_publisher(Float64, "/manipulability_index", 10)
        self.ellipoid_marker = Marker()
        self.ellipoid_marker.header.frame_id = "world"
        self.ellipoid_marker.header.stamp = node.get_clock().now().to_msg()
        self.ellipoid_marker.type = Marker.SPHERE

        self.ellipoid_marker.color.a = 0.5
        self.ellipoid_marker.color.r = 0.0
        self.ellipoid_marker.color.g = 1.0
        self.ellipoid_marker.color.b = 0.0

        #######################################################################
        # Initialize end-effector position for numerical differentiation
        self.x_ee_w = np.zeros(3)
        # None until the first position is known, avoids a velocity spike at start
        self.x_ee_w_prev = None

    def get_joint_states(self) -> np.ndarray:
        """ Get the joint states

        Returns:
            np.ndarray: joint states (3 x n)
            first row: joint positions
            second row: joint velocities
            third row: joint accelerations
        """
        joint_states = np.vstack((self.q, self.qdot, self.qddot))
        return joint_states

    def set_kinematics(self,  q: np.ndarray, qdot: np.ndarray) -> None:
        """Update the forward kinematics of the robot with the given joint states

        Args:
            q (np.ndarray): joint positions (n x 1)
            qdot (np.ndarray): joint velocities (n x 1)
        """
        self.q = q
        self.qdot = qdot

    def update_kinematics(self,) -> None:
        """Publish joint states and broadcast tf frames
        """
        #######################################################################
        # TODO: Publish the joint states (self.q, self.qdot)as a JointState message
        # Note: there is a -pi/2 offset in the second joint
        self.publish_joint_states()

        #######################################################################
        # TODO: Plug in the numerical joint states to the functions T(q) in the model
        # to get the numerical transformation matrices
        # T_ee_w
        q_num = np.asarray(self.q, dtype=float).flatten()
        self.T_ee_w = np.array(self.model.T_ee_w_fn(*q_num), dtype=float)

        #######################################################################
        # TODO: Broadcast the transformation matrices as tf frames
        # T_ee_w
        stamp = self.node.get_clock().now().to_msg()
        self.br.sendTransform(ros_utils.matrix_to_transform(self.T_ee_w, 'world', 'ee', stamp))

        #######################################################################

    def update_differential_kinematics(self, dt: float) -> None:
        """Update the differential kinematics of the robot with the given joint states

        Args:
            dt (float): time step
        """
        q_num = np.asarray(self.q, dtype=float).flatten()
        qdot_num = np.asarray(self.qdot, dtype=float).flatten()

        ########################################################################
        # TODO: Calculate the end-effector twist from Jacobian and publish as a
        # geometry_msgs/Twist message

        # Calculate end-effector Jacobian in the world frame J_ee_w
        J_ee_w = np.array(self.model.J_ee_w_fn(*q_num), dtype=float)

        # Calculate the end-effector Twist in the world frame V_ee_w = [omega; v]
        V_ee_w = J_ee_w @ qdot_num

        # Publish the end-effector Twist as a geometry_msgs/Twist message
        self.ee_vel_from_J_pub.publish(self.vec_to_twist(V_ee_w))

        ########################################################################
        # TODO: Calculate the end-effector linear velocity from numerical
        # differentiation of the position and publish as a geometry_msgs/Vector3
        # message

        # End-effector position
        self.x_ee_w = self.T_ee_w[0:3, 3].copy()

        # Numerical differentiation (skipped in the first step, no previous position yet)
        if self.x_ee_w_prev is not None and dt > 0.0:
            v_ee_w_num = (self.x_ee_w - self.x_ee_w_prev) / dt

            # Publish the end-effector linear velocity as a geometry_msgs/Vector3 message
            self.ee_vel_from_num_diff_pub.publish(self.vec_to_vector3(v_ee_w_num))

        # Save the current end-effector position for the next iteration
        self.x_ee_w_prev = self.x_ee_w

        ########################################################################
        # Manipulability analysis
        # TODO: plug in the linear part of the Jacobian for manipulability analysis
        self.manipulatbility_analysis(J_ee_w[3:6, :])


    def manipulatbility_analysis(self, J: np.ndarray):
        # 1. manipulability index w = sqrt(det(J J^T)), linear part of J (3 x 3)
        A = J @ J.T
        # max() guards against tiny negative values from round-off at singularities
        w = np.sqrt(max(np.linalg.det(A), 0.0))
        self.manipulability_pub.publish(Float64(data=float(w)))

        # 2. SVD: columns of U = principal axes, singular values S = axis lengths
        # Note: if do svd of A, then U is same, but scaling is sqrt(S[i])
        U, S, _ = np.linalg.svd(J)
        # RViz rejects a scale of 0 (singular configuration), keep a small minimum
        S = np.maximum(S, 1e-3)

        # 3. sphere marker at the end-effector, rotated by U and scaled by S
        self.ellipoid_marker.header.stamp = self.node.get_clock().now().to_msg()

        self.ellipoid_marker.pose.position.x = float(self.x_ee_w[0])
        self.ellipoid_marker.pose.position.y = float(self.x_ee_w[1])
        self.ellipoid_marker.pose.position.z = float(self.x_ee_w[2])

        # U can be a reflection (det = -1), flip one axis to get a proper rotation
        if np.linalg.det(U) < 0:
            U[:, 2] *= -1
        q = Rotation.from_matrix(U).as_quat()   # [x, y, z, w]
        self.ellipoid_marker.pose.orientation.x = q[0]
        self.ellipoid_marker.pose.orientation.y = q[1]
        self.ellipoid_marker.pose.orientation.z = q[2]
        self.ellipoid_marker.pose.orientation.w = q[3]

        self.ellipoid_marker.scale.x = S[0]
        self.ellipoid_marker.scale.y = S[1]
        self.ellipoid_marker.scale.z = S[2]

        self.marker_pub.publish(self.ellipoid_marker)


    def publish_joint_states(self):
        """ Publish the joint states as a JointState message
        """
        self.joint_msg.header.stamp = self.node.get_clock().now().to_msg()
        # model zero = upright arm (Fig. 4); URDF zero = arm horizontal, wrist forward
        q = np.zeros(6)
        q[0:3] = np.asarray(self.q, dtype=float).flatten()
        q[1] -= np.pi/2      # shoulder offset
        q[3] = -np.pi/2      # fixed wrist_1, so the wrist points up as in Fig. 4
        qdot = np.zeros(6)
        qdot[0:3] = np.asarray(self.qdot, dtype=float).flatten()
        self.joint_msg.position = q.tolist()
        self.joint_msg.velocity = qdot.tolist()
        self.joint_states_pub.publish(self.joint_msg)

    @staticmethod
    def vec_to_vector3(v: np.ndarray) -> Vector3:
        return Vector3(x=float(v[0]), y=float(v[1]), z=float(v[2]))

    def vec_to_twist(self, V: np.ndarray) -> Twist:
        """ twist V = [omega; v] -> Twist message """
        msg = Twist()
        msg.angular = self.vec_to_vector3(V[0:3])
        msg.linear = self.vec_to_vector3(V[3:6])
        return msg
