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
        self.joint_states_pub = None

        #######################################################################
        # TODO: Create a TransformBroadcaster
        self.br = None

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
        # self.joint_states_pub.publish(...)

        #######################################################################
        # TODO: Plug in the numerical joint states to the forward kinematics 
        # functions in the model (*_fn) to get the numerical 
        # transformation matrices: T_ee_w, T_cm1_0, T_cm2_0, T_cm3_0, T_cm4_0
        # e.g. T = T_fn(*q)
        T_ee_w = np.eye(4)
        T_cm1_0 = np.eye(4)
        T_cm2_0 = np.eye(4)
        T_cm3_0 = np.eye(4)

        #######################################################################
        # TODO: Broadcast the transformation matrices as tf frames
        # T_ee_w, T_cm1_0, T_cm2_0, T_cm3_0, T_cm4_0
        # self.br.sendTransform(...)

