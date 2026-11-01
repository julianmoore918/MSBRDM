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

        T_ee_w = np.array(self.model.T_ee_w_fn(*q_num), dtype=float)
        T_cm1_0, T_cm2_0, T_cm3_0, T_cm4_0 = [
            np.array(fn(*q_num), dtype=float) for fn in self.model.T_cms_0_fn]

        #######################################################################
        # TODO: Broadcast the transformation matrices as tf frames
        # T_ee_w, T_cm1_0, T_cm2_0, T_cm3_0, T_cm4_0
        # self.br.sendTransform(...)

        stamp = self.node.get_clock().now().to_msg()
        transforms = [
            ros_utils.matrix_to_transform(self.T_0_w, 'world', 'frame_0', stamp),
            ros_utils.matrix_to_transform(T_ee_w, 'world', 'ee', stamp),
        ]
        for i, T in enumerate([T_cm1_0, T_cm2_0, T_cm3_0, T_cm4_0]):
            transforms.append(ros_utils.matrix_to_transform(T, 'frame_0', f'cm{i+1}', stamp))
        self.br.sendTransform(transforms)

