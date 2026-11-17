from rclpy.node import Node
from rclpy.time import Time, Duration
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import WrenchStamped
import numpy as np

from ur10_model.ur10_model_3dof import UR10Model3DOF


class UR10Controller():

    def __init__(self, model: UR10Model3DOF, q_init: np.ndarray = np.zeros((3, 1))) -> None:
        self.node = Node('ur10_force_control')
        self.model = model
        self.q = q_init

        ########################################################################
        # ROS connection
        ########################################################################
        # TODO: Subscribe to target position and obstacle position
        self.target_pos_sub = None
        self.obstacle_pos_sub = None

        # Optional: Publish repulsive forces for visualization 
        # (Use the message geometry_msgs/WrenchStamped) )
        self.ee_wrench_pub = None
        self.joint1_wrench_pub = None
        self.joint2_wrench_pub = None
        self.joint3_wrench_pub = None

        ########################################################################
        # Control Gains
        ########################################################################
        # TODO: Tune the control gains here
        self.Kp = np.diag([0, 0, 0])
        self.Kd = np.diag([0, 0, 0])
        
        # positions initialization
        self.target_pos = np.zeros((3, 1))
        self.obstacle_pos = np.zeros((3, 1))

    def update(self, joint_states: np.ndarray, t: Time, dt: Duration) -> np.ndarray:
        tau = self.force_controller(joint_states, dt)
        return tau

    def force_controller(self, joint_states: np.ndarray, dt: Duration) -> np.ndarray:

        q = joint_states[0, :].reshape(-1, 1)
        qdot = joint_states[1, :].reshape(-1, 1)
        qddot = joint_states[2, :].reshape(-1, 1)

         ########################################################################
        # Attractive Force  
        ########################################################################
        # TODO: Calculate the virtual attractive force based on the position error
        # to the target

        # end-effector position

        # position error

        # end-effector Jacobian
        
        # end-effector velocity

        # virtual attractive force Virtual atractive force. 
        # Function using the error in position and a damping in velocity   

        F_att = np.zeros((3, 1))

        ########################################################################
        # Repulsive Forces
        ########################################################################
        # TODO: Calculate the repulsive forces based on the distance to the obstacle
        # from joints 1-3 and the end-effector
        # Hint: You need to add the calculation of the transformations and Jacobians
        # for each joint in your model.

        # cartesian positions of each joint
        x_1_w = np.zeros((3, 1))
        x_2_w = np.zeros((3, 1))
        x_3_w = np.zeros((3, 1))

        # joint Jacobians (linear part)
        J_1_w = np.zeros((3, 3))
        J_2_w = np.zeros((3, 3))
        J_3_w = np.zeros((3, 3))

        # threshold distance
        d_min = 0.5
        # distances of obstacle to joints and ee w.r.t. world frame
        d1_w = np.zeros((3, 1))
        d1_norm = 0
        d2_w = np.zeros((3, 1))
        d2_norm = 0
        d3_w = np.zeros((3, 1))
        d3_norm = 0
        d4_w = np.zeros((3, 1))
        d4_norm = 0

        # directions of repulsive force 
        d1_dir = np.zeros((3, 1))
        d2_dir = np.zeros((3, 1))
        d3_dir = np.zeros((3, 1))
        d4_dir = np.zeros((3, 1))

        F1_rep = np.zeros((3, 1))
        if d1_norm < d_min:
            # compute repulsive force on joint 1 w.r.t. world frame
            F1_rep = np.zeros((3, 1))
        # Do the same for joint 2, 3 and end-effector


        ########################################################################
        # Optional: Publish repulsive forces for visualization using WrenchStamped msgs
        # Hint: For visualization the forces on each joint / ee, you need to 
        # rotate the forces from world frame back to the body frame
        
        
        ########################################################################
        # Gravity Compensation
        ########################################################################
        # TODO: Calculate the gravity vector
        G = np.zeros((3, 1))


        ########################################################################
        # TODO: Sum all forces with their corresponding Jacobians, and gravity
        tau = np.zeros((3, 1))
        return tau

# TODO: Define callback functions for target and obstacle positions
