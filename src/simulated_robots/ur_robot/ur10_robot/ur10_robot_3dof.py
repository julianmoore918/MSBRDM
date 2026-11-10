import rclpy
import numpy as np
from ur10_model.ur10_model_3dof import UR10Model3DOF
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster

from visualization_msgs.msg import Marker
from tf_transformations import quaternion_from_matrix


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
        self.joint_states_pub = None
        
        self.br = TransformBroadcaster()
         
        #######################################################################
        # TODO: Define the end-effector velocity publishers
        # Type: geometry_msgs/Twist
        self.ee_vel_from_J_pub = None
        # Type: geometry_msgs/Vector3
        self.ee_vel_from_num_diff_pub = None
        
        #######################################################################
        # ellispoid marker publisher
        self.marker_pub = node.create_publisher(Marker, "/manipulability_ellipsoid", 10)
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
        self.x_ee_w = np.zeros((3, 1))
        self.x_ee_w_prev = self.x_ee_w

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
        self.joint_states_pub.publish(...)

        #######################################################################
        # TODO: Plug in the numerical joint states to the functions T(q) in the model
        # to get the numerical transformation matrices
        # T_ee_w
        self.T_ee_w = np.eye(4)

        #######################################################################
        # TODO: Broadcast the transformation matrices as tf frames
        # T_ee_w
        self.br.sendTransform(...)

        #######################################################################

    def update_differential_kinematics(self, dt: float) -> None:
        """Update the differential kinematics of the robot with the given joint states

        Args:
            dt (float): time step
        """
        
        ########################################################################
        # TODO: Calculate the end-effector twist from Jacobian and publish as a
        # geometry_msgs/Twist message

        # Calculate end-effector Jacobian in the world frame J_ee_w
        J_ee_w = np.zeros((6, self.model.nq))
        
        # Calculate the end-effector Twist in the world frame V_ee_w
        V_ee_w = np.zeros((6, 1))

        # Publish the end-effector Twist as a geometry_msgs/Twist message
        self.ee_vel_from_J_pub.publish(...)
        
        ########################################################################
        # TODO: Calculate the end-effector linear velocity from numerical
        # differentiation of the position and publish as a geometry_msgs/Vector3
        # message

        # End-effector position
        self.x_ee_w = np.zeros((3, 1))

        # Numerical differentiation
        v_ee_w_num = np.zeros((3, 1))

        # Save the current end-effector position for the next iteration
        self.x_ee_w_prev = None

        # Publish the end-effector linear velocity as a geometry_msgs/Vector3 message
        self.ee_vel_from_num_diff_pub.publish(...)

        ########################################################################
        # Manipulability analysis
        # TODO: plug in the linear part of the Jacobian for manipulability analysis
        self.manipulatbility_analysis()
        

    def manipulatbility_analysis(self, J: np.ndarray):
        A = J @ J.T
        w = np.sqrt(np.linalg.det(A))

        # Note: if do svd of A, then U is same, but scaling is sqrt(S[i])
        U, S, _ = np.linalg.svd(J)
        
        self.ellipoid_marker.pose.position.x = self.x_ee_w[0]
        self.ellipoid_marker.pose.position.y = self.x_ee_w[1]
        self.ellipoid_marker.pose.position.z = self.x_ee_w[2]

        T_U = np.eye(4)
        T_U[0:3, 0:3] = U
        q = quaternion_from_matrix(T_U)
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
        q = self.q.copy()
        q[1] -= np.pi/2
        self.joint_msg.position = q
        self.joint_msg.velocity = self.qdot
        self.joint_states_pub.publish(self.joint_msg)


