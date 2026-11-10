#!/usr/bin/env python3
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
        self.controller = UR10KinematicController3DOF(self.model, q_init=q_init)

        # set goal
        x_goal = np.array([0.1, 0.0, 0.5])
        
        # start controller
        self.controller.start()

        self.prev_time = self.get_clock().now()

        # 100 Hz timer
        self.timer = self.create_timer(0.01, self.update)

    def update(self):
        # time
        time = self.get_clock().now()
        dt = time - self.prev_time
        self.prev_time = time

        # TODO: get current joint states from robot
        joint_states =

        # TODO: update controller with current joint states
        u =

        # TODO: feed the control input to the robot by calling the command function

        # TODO: Visualize manipulability ellipsoid
        
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
