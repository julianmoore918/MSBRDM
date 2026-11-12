
from rclpy.node import Node
import numpy as np
from rppr_model.rppr_model import RPPRModel
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
import msbrdm_libs.ros_utils as ros_utils 
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Twist


class RPPRRobot():
    """ A simulated RPPR robot that visualizes joint states and updates 
    transformations with the model
    """

    def __init__(self, model: RPPRModel, q_init: np.ndarray = None,
                 node: Node = None) -> None:
        # initialization
        self.model = model
        self.node = node

        # publishers for the velocity check
        self.ee_vel_J_pub = self.node.create_publisher(Twist, '/ee_vel_from_J', 10)
        self.ee_vel_num_pub = self.node.create_publisher(Vector3, '/ee_vel_from_num_diff', 10)
        self.cm2_vel_J_pub = self.node.create_publisher(Twist, '/cm2_vel_from_J', 10)
        self.cm2_vel_num_pub = self.node.create_publisher(Vector3, '/cm2_vel_from_num_diff', 10)
        # positions of the previous step for numerical differentiation
        self.x_ee_prev = None
        self.x_cm2_prev = None


        # joint states: [q, qdot, qddot] (n x 3)
        self.joint_states = np.zeros((self.model.nq, 3))
        if q_init is not None:
            self.joint_states[:, 0] = q_init
        # Note: q, qdot, qddot hold the same reference of joint_states
        # they can be accessed both as a whole and separately
        self.q = self.joint_states[:, 0].reshape(self.model.nq, 1)
        self.qdot = self.joint_states[:, 1].reshape(self.model.nq, 1)
        self.qddot = self.joint_states[:, 2].reshape(self.model.nq, 1)

        #######################################################################
        # TODO: Initialize the joint states publisher
        self.joint_states_pub = self.node.create_publisher(JointState, 'joint_states', 10)
        self.joint_names = ['q1_joint', 'q2_joint', 'q3_joint', 'q4_joint']

        #######################################################################
        # TODO: Create a TransformBroadcaster
        self.br = TransformBroadcaster(self.node)

         # constant base transformation {0} w.r.t. world, as numeric 4x4 array
        self.T_0_w = np.array(self.model.T_0_w.subs(self.model.params_list), dtype=float)

    def update_kinematics(self, q: np.ndarray, qdot: np.ndarray) -> None:
        """Update the forward kinematics of the robot with the given joint states

        Args:
            q (np.ndarray): joint positions (n x 1)
            qdot (np.ndarray): joint velocities (n x 1)
        """
        self.q = q
        self.qdot = qdot
        
        #######################################################################
        # TODO: Publish the joint states as a JointState message

        msg = JointState()
        msg.header.stamp = self.node.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = np.asarray(q, dtype=float).flatten().tolist()
        msg.velocity = np.asarray(qdot, dtype=float).flatten().tolist()
        self.joint_states_pub.publish(msg)

        #######################################################################
        # TODO: Plug in the numerical joint states to the forward kinematics 
        # functions in the model (*_fn) to get the numerical 
        # transformation matrices: T_ee_w, T_cm1_0, T_cm2_0, T_cm3_0, T_cm4_0
        # e.g. T = T_fn(*q)

        q_num = np.asarray(q, dtype=float).flatten()          # [q0, q1, q2, q3]

        self.T_ee_w = np.array(self.model.T_ee_w_fn(*q_num), dtype=float)
        self.T_cms_0 = [np.array(fn(*q_num), dtype=float) for fn in self.model.T_cms_0_fn]

        #######################################################################
        # TODO: Broadcast the transformation matrices as tf frames
        # T_ee_w, T_cm1_0, T_cm2_0, T_cm3_0, T_cm4_0
        # self.br.sendTransform(...)

        stamp = self.node.get_clock().now().to_msg()
        transforms = [
            ros_utils.matrix_to_transform(self.T_0_w, 'world', 'frame_0', stamp),
            ros_utils.matrix_to_transform(self.T_ee_w, 'world', 'ee', stamp),
        ]
        for i, T in enumerate(self.T_cms_0):
            transforms.append(ros_utils.matrix_to_transform(T, 'frame_0', f'cm{i+1}', stamp))
        self.br.sendTransform(transforms)

    def update_differential_kinematics(self, dt: float) -> None:
        """Update the differential kinematics of the robot and verify velocities

        Args:
            dt (float): time step
            """
        q_num = np.asarray(self.q, dtype=float).flatten()
        qdot_num = np.asarray(self.qdot, dtype=float).flatten()

        # 1. ee twist in world frame from the Jacobian: wJ_ee = blockdiag(R_0w, R_0w) * 0J_ee
        R_0w = self.T_0_w[0:3, 0:3]
        Ad_R = np.zeros((6, 6))
        Ad_R[0:3, 0:3] = R_0w
        Ad_R[3:6, 3:6] = R_0w
        J_ee_w = Ad_R @ np.array(self.model.J_ee_0_fn(*q_num), dtype=float)
        self.ee_vel_J_pub.publish(self.vec_to_twist(J_ee_w @ qdot_num))

        # 2. ee linear velocity by numerical differentiation of the world position
        x_ee = self.T_ee_w[0:3, 3].copy()
        if self.x_ee_prev is not None and dt > 0.0:
            self.ee_vel_num_pub.publish(self.vec_to_vector3((x_ee - self.x_ee_prev) / dt))
        self.x_ee_prev = x_ee

        # 3. same for cm2, both in frame {0}
        J_cm2_0 = np.array(self.model.J_cms_0_fn[1](*q_num), dtype=float)
        self.cm2_vel_J_pub.publish(self.vec_to_twist(J_cm2_0 @ qdot_num))

        x_cm2 = self.T_cms_0[1][0:3, 3].copy()
        if self.x_cm2_prev is not None and dt > 0.0:
            self.cm2_vel_num_pub.publish(self.vec_to_vector3((x_cm2 - self.x_cm2_prev) / dt))
        self.x_cm2_prev = x_cm2

    @staticmethod
    def vec_to_vector3(v: np.ndarray) -> Vector3:
        return Vector3(x=float(v[0]), y=float(v[1]), z=float(v[2]))

    def vec_to_twist(self, V: np.ndarray) -> Twist:
        """ twist V = [omega; v] -> Twist message """
        msg = Twist()
        msg.angular = self.vec_to_vector3(V[0:3])
        msg.linear = self.vec_to_vector3(V[3:6])
        return msg





