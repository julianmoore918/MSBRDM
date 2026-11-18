import numpy as np
from rclpy.node import Node
from rclpy.time import Time, Duration

from msbrdm_libs.spline import LinearSplineTrajectory
from ur10_model.ur10_model_3dof import UR10Model3DOF

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path


class UR10KinematicController3DOF:
    def __init__(self, model: UR10Model3DOF, q_init: np.ndarray = np.zeros((3, 1))) -> None:
        """Kinematic controller for the UR10 robot with 3 DOF

        Args:
            model (UR10Model3DOF): robot model
            q_init (np.ndarray, optional): initial joint positions. Defaults to np.zeros(3).
        """
        self.model = model
        self.q = q_init

        # TODO: calculate the initial end-effector position in {w}
        self.x = np.zeros(3)

        #######################################################################
        # Initializations
        # end-effector goal position in {w}
        self.x_goal = np.zeros(3)
        # trajectory duration (default: 10s)
        self.duration = 10.0
        # singularity threshold
        self.w_threshold = 0.0

        self.trajectory = None
        self.start_time = None

        #######################################################################
        # (Optional) TODO: Publish the trajectory as nav_msgs/Path for visualization
        self.path_pub = None

    def set_goal_abs(self, x_goal):
        """Set goal position with absolute coordinates in {w}

        Args:
            x_goal (_type_): absolute goal position in {w}
        """
        # TODO: set member variable self.x_goal
        pass

    def set_goal_rel(self, x_goal):
        """Set goal position with relative coordinates in {w}

        Args:
            x_goal (_type_): relative goal position in {w}
        """
        # TODO: set member variable self.x_goal
        pass
    
    def set_duration(self, duration: float):
        """Set the duration of the trajectory

        Args:
            duration (float): duration
        """
        # TODO: set member variable self.duration
        pass

    def set_w_threshold(self, threshold: float):
        """Set the threshold for manipulability index

        Args:
            threshold (float): threshold value
        """
        # TODO: set member variable self.w_threshold
        pass

    def start(self):
        # TODO: generate the trajectory with the initial start and goal position
        # as the type of LinearSplineTrajectory
        self.trajectory

        # save the start time
        self.start_time

        # Optional: publish the trajectory for visualization
        
    def update(self, joint_states: np.ndarray,
               time: Time, dt: Duration) -> None:
        """ Update the controller

        Args:
            joint_states (np.ndarray): current joint states from robot feedback [q, qdot, qddot] (3 x n)
            time (rospy.Time): current ros time
            dt (rospy.Duration): time interval

        Returns:
            np.ndarray: controller output u
        """
        # retrieve joint positions and velocities
        self.q = joint_states[0, :]
        self.qdot = joint_states[1, :]

        ########################################################################
        # TODO: Implement the kinematic controller

        # end-effector position

        # end-effector jacobian
        
        # extract jacobian for linear velocity only

        # compute the manipulability index
        
        # get desired cartesian states from the trajectory
        
        # implement the kinematic controller

        return u
    
