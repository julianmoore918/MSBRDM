from rclpy.node import Node
from rclpy.time import Time, Duration
from sensor_msgs.msg import JointState
import numpy as np
from enum import Enum

from ur10_model.ur10_model_3dof import UR10Model3DOF


class UR10Controller():
    """ Passitivity-based joint space controller for UR10 Robot (3 DOF)
    """
    
    class State(Enum):
        INIT = 1
        REGULATE = 2
        TRACK_SLOW = 3
        TRACK_FAST = 4
        END = 5

    class Controller(Enum):
        PD = 1
        PD_G = 2
        PID = 3

    def __init__(self, model: UR10Model3DOF, q_init: np.ndarray = np.zeros((3, 1))) -> None:
        self.node = Node('ur10_js_controller')
        self.model = model
        self.q = q_init

        self.state = self.State.INIT
        self.controller = self.Controller.PD
        self.t_start = self.node.get_clock().now()

        ########################################################################
        # ROS Publishers
        ########################################################################
        self.joint_states_des_pub = self.node.create_publisher(
            JointState, "/joint_states_des", 10)
        #TODO: Create a publisher for the Lyapunov function, and one for the steady state error
        

        ########################################################################
        # Control Gains
        ########################################################################
        # TODO: Tune the control gains here
        self.Kp_PD = np.diag([0, 0, 0])
        self.Kd_PD = np.diag([0, 0, 0])

        self.Kp_PDG = np.diag([0, 0, 0])
        self.Kd_PDG = np.diag([0, 0, 0])

        self.Kp_PID = np.diag([0, 0, 0])
        self.Kd_PID = np.diag([0, 0, 0])
        self.Ki_PID = np.diag([0, 0, 0])

        # Initialize control gains
        self.Kp = self.Kp_PD
        self.Kd = self.Kd_PD
        self.Ki = np.zeros((3, 3))

        ########################################################################
        # Time for State Transition
        ########################################################################
        # TODO: Set the time for each state
        self.t_REGULATE = 0
        self.t_TRACK_SLOW = 0
        self.t_TRACK_FAST = 0

    def update(self, joint_states: np.ndarray, t: Time, dt: Duration) -> np.ndarray:
        """Update the controller

        Args:
            joint_states (np.ndarray): joint states from robot feedback [q, qdot, qddot] (3 x n)
            t (rospy.Time): current ros time
            dt (rospy.Duration): time interval

        Returns:
            np.ndarray: torque commands (n x 1)
        """
        # TODO: update state machine

        # TODO: update trajectory

        # TODO: update controller and return torque commands
        tau = np.zeros((self.model.nq, 1))

        return tau

    def state_machine(self, state: Enum, t_elapsed: float):
        """
        State Machine
        Sequence: 
          PD: REGULATE -> TRACK_SLOW -> TRACK_FAST 
          PD_G: REGULATE -> TRACK_SLOW -> TRACK_FAST 
          PID: REGULATE -> TRACK_SLOW -> TRACK_FAST 
        """
        # TODO: update state based on elapsed time, assign controller type and
        # control gains for each state
        # Either return new state or update self.state

    def trajectory(self, state, t) -> np.ndarray:
        """Generate Desired Joint States

        Args:
            state (Enum): state of the state machine
            t (rospy.Time): current ros time

        Returns:
            np.ndarray: desired joint states [q_des, qdot_des, qddot_des] (3 x n)
        """
        # TODO: Implement the desired joint states based on the state machine
        q_des = np.zeros(self.model.nq)
        qdot_des = np.zeros(self.model.nq)
        qddot_des = np.zeros(self.model.nq)
        joint_states_des = np.row_stack((q_des, qdot_des, qddot_des))

        # TODO: Publish Desired Joint States
        # Remember the second joint is offset by -pi/2
        joint_msg = JointState()
        self.joint_states_des_pub.publish(joint_msg)

        return joint_states_des

    ########################################################################
    #                        Joint Space Controller                        #
    ########################################################################

    def joints_space_controller(self, joint_states: np.ndarray, joint_states_des: np.ndarray,
                                controller_type: Enum, dt: Duration) -> np.ndarray:
        """Joint Space Controller

        Args:
            joint_states (np.ndarray): current joint states from robot feedback [q, qdot, qddot] (3 x n)
            joint_states_des (np.ndarray): desired joint states [q_des, qdot_des, qddot_des] (3 x n)
            controller_type (Enum): PD, PD_G, PID
            dt (rospy.Duration): time interval

        Returns:
            np.ndarray: torque commands (n x 1)
        """
        # Rotate the joint states to column vectors for easier calculations
        q = joint_states[0, :].reshape(-1, 1)
        qdot = joint_states[1, :].reshape(-1, 1)
        qddot = joint_states[2, :].reshape(-1, 1)

        q_des = joint_states_des[0, :].reshape(-1, 1)
        qdot_des = joint_states_des[1, :].reshape(-1, 1)
        qddot_des = joint_states_des[2, :].reshape(-1, 1)

        # TODO: Implement the controllers for PD, PD_G, PID
        # hint: use if-else or switch-case to select the controller
        tau = np.zeros((self.model.nq, 1))

        # TODO: Calculate Lyapunov function and publish
        V = 0

        # TODO: Calculate steady state error and publish
        err = np.zeros((self.model.nq, 1))

        return tau
