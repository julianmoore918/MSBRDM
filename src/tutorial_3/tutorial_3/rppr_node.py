#!/usr/bin/env python3
"""
RPPR Node
This node updates the forward kinematics and differential kinematics of the
robot with a sinusoidal joint trajectory
"""
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.impl.implementation_singleton import rclpy_implementation as _rclpy

from rppr_model.rppr_model import RPPRModel
from rppr_robot.rppr_robot import RPPRRobot


class RPPRNode(Node):

  def __init__(self):
    super().__init__('rppr_node')

    # initialize model and robot
    self.model = RPPRModel()
    self.robot = RPPRRobot(self.model, node=self)

    self.time_start = self.get_clock().now()
    self.prev_time = self.time_start
    self.timer = self.create_timer(0.01, self.update)

  def update(self):
    time = self.get_clock().now()
    t = (time - self.time_start).nanoseconds * 1e-9
    dt = (time - self.prev_time).nanoseconds * 1e-9
    self.prev_time = time

    # joint trajectories
    q1 = np.pi*np.sin(t/2)
    q2 = 0.04*np.sin(t/2) + 0.04
    q3 = 0.04*np.sin(t/2) + 0.04
    q4 = np.pi/4*np.sin(t/2) - np.pi/4

    q1_dot = np.pi/2*np.cos(t/2)
    q2_dot = 0.04/2*np.cos(t/2)
    q3_dot = 0.04/2*np.cos(t/2)
    q4_dot = np.pi/4/2*np.cos(t/2)

    q = np.array([q1, q2, q3, q4])
    qdot = np.array([q1_dot, q2_dot, q3_dot, q4_dot])

    self.robot.update_kinematics(q, qdot)
    self.robot.update_differential_kinematics(dt)


def main(args=None):
  rclpy.init(args=args)
  node = RPPRNode()
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


################################################################################
# TODO: Answer to the question b.3.2
