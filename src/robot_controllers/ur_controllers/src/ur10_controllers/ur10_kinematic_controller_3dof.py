import numpy as np
from rclpy.node import Node
from rclpy.time import Time, Duration

from msbrdm_libs.spline import LinearSplineTrajectory
from ur10_model.ur10_model_3dof import UR10Model3DOF

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path


class UR10KinematicController3DOF:
    def __init__(self, model: UR10Model3DOF, q_init: np.ndarray = np.zeros((3, 1)), node: Node = None) -> None:
        """Kinematic controller for the UR10 robot with 3 DOF

        Args:
            model (UR10Model3DOF): robot model
            q_init (np.ndarray, optional): initial joint positions. Defaults to np.zeros(3).
        """
        self.model = model
        self.node = node
        self.q = q_init

        # TODO: calculate the initial end-effector position in {w}
        self.x = np.array(self.model.T_ee_w_fn(*self.q), dtype=float)[0:3, 3]

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
        self.path_msg = None
        if self.node is not None:
            self.path_pub = self.node.create_publisher(Path, '/trajectory', 10)

    def set_goal_abs(self, x_goal):
        """Set goal position with absolute coordinates in {w}

        Args:
            x_goal (_type_): absolute goal position in {w}
        """
        # TODO: set member variable self.x_goal
        self.x_goal = np.asarray(x_goal, dtype=float)

    def set_goal_rel(self, x_goal):
        """Set goal position with relative coordinates in {w}

        Args:
            x_goal (_type_): relative goal position in {w}
        """
        # TODO: set member variable self.x_goal
        self.x_goal = self.x + np.asarray(x_goal, dtype=float)
    
    def set_duration(self, duration: float):
        """Set the duration of the trajectory

        Args:
            duration (float): duration
        """
        # TODO: set member variable self.duration
        self.duration = duration

    def set_w_threshold(self, threshold: float):
        """Set the threshold for manipulability index

        Args:
            threshold (float): threshold value
        """
        # TODO: set member variable self.w_threshold
        self.w_threshold = threshold

    def start(self):
        # TODO: generate the trajectory with the initial start and goal position
        # as the type of LinearSplineTrajectory
        self.trajectory = LinearSplineTrajectory(self.x, self.x_goal, self.duration)

        # save the start time
        self.start_time = None

        # Optional: publish the trajectory for visualization
        if self.path_pub is not None:
            self.path_msg = Path()
            self.path_msg.header.frame_id = 'world'
            for t in np.linspace(0.0, self.duration, 100):
                x_d, _, _ = self.trajectory.update(t)
                pose = PoseStamped()
                pose.header.frame_id = 'world'
                pose.pose.position.x = float(x_d[0])
                pose.pose.position.y = float(x_d[1])
                pose.pose.position.z = float(x_d[2])
                pose.pose.orientation.w = 1.0
                self.path_msg.poses.append(pose)
        
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
        self.x = np.asarray(self.model.T_ee_w_fn(*self.q), dtype=float)[0:3, 3]
        # end-effector jacobian
        J = np.array(self.model.J_ee_0_fn(*self.q), dtype=float)
        # extract jacobian for linear velocity only
        J_v = J[3:6, :]
        # compute the manipulability index
        w = np.sqrt(max(np.linalg.det(J_v @ J_v.T), 0.0))
        # get desired cartesian states from the trajectory
        if self.start_time is None:
            self.start_time = time
        t = (time - self.start_time).nanoseconds * 1e-9
        x_d, v_d, _ = self.trajectory.update(t)
        # implement the kinematic controller
        # Instead of stopping: Damped Least Squares (DLS) inverse
        #   u = J_v^T (J_v J_v^T + lambda^2 I)^-1 (v_d + K (x_d - x))
        # The damping term lambda^2 I keeps the matrix invertible even at a
        # singularity, so the joint velocities stay bounded. In the singular
        # direction the robot simply stops moving, while all other directions
        # are still controlled. For an unreachable goal the robot therefore gets
        # as close as possible instead of freezing.
        # lambda is only increased near singularities (e.g. when w < w_threshold),
        # so normal tracking stays exact. Trade-off: a small position error there.

        if w < self.w_threshold:
            print(f'[controller] near singularity (w = {w:.4f}), stopping')
            u = np.zeros(3)
        else:
            self.K = 5.0 * np.eye(3)
            u = np.linalg.solve(J_v, v_d + self.K @ (x_d - self.x))

        if self.path_msg is not None:
            self.path_msg.header.stamp = time.to_msg()
            self.path_pub.publish(self.path_msg)


        return u
    
