#!/usr/bin/env python3
from time import time

import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.impl.implementation_singleton import rclpy_implementation as _rclpy

from ur10_model.ur10_model_3dof import UR10Model3DOF
from ur10_robot.ur10_robot_3dof import UR10Robot3DOF
from ur10_controllers.ur10_kinematic_controller_3dof import UR10KinematicController3DOF


class UR10KinematicControlNode(Node):

    def __init__(self):
        super().__init__('ur10_kinematic_control_node')

        # initialize model and robot
        self.model = UR10Model3DOF()
        q_init = np.array([0, 0, np.pi/2])
        self.robot = UR10Robot3DOF(self.model, q_init=q_init, node=self)
        self.controller = UR10KinematicController3DOF(self.model, q_init=q_init, node=self)


        # set goal
        x_goal = np.array([0.9, 0.256, 1.0])
        self.controller.set_goal_abs(x_goal)
        self.controller.set_duration(10.0)
        self.controller.set_w_threshold(0.01)

        # start controller
        self.controller.start()

        self.prev_time = self.get_clock().now()

        # 100 Hz timer
        self.timer = self.create_timer(0.01, self.update)


    def update(self):
        # time
        time = self.get_clock().now()
        dt = time - self.prev_time
        dt_sec = dt.nanoseconds * 1e-9
        self.prev_time = time

        # TODO: get current joint states from robot
        joint_states = self.robot.get_joint_states()

        # TODO: update controller with current joint states
        u = self.controller.update(joint_states, time, dt)

        # TODO: feed the control input to the robot by calling the command function
        self.robot.command_vel_interface(u, dt)

        # TODO: Visualize manipulability ellipsoid 
        self.robot.update_kinematics()
        self.robot.update_differential_kinematics(dt_sec)
         
        
def main(args=None):
    rclpy.init(args=args)
    node = UR10KinematicControlNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException,
            _rclpy.RCLError):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
