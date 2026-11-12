#!/usr/bin/env python3
"""
UR10 Node
This node updates the forward kinematics of the robot with a sinusoidal joint
trajectory
"""
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.impl.implementation_singleton import rclpy_implementation as _rclpy

from ur10_model.ur10_model_3dof import UR10Model3DOF
from ur10_robot.ur10_robot_3dof import UR10Robot3DOF

class UR10Node(Node):

  def __init__(self):
    super().__init__('ur_node')

    # initialize model and robot
    self.model = UR10Model3DOF()
    self.robot = UR10Robot3DOF(self.model, node=self)

    self.time_start = self.get_clock().now()
    self.prev_time = self.time_start
    self.timer = self.create_timer(0.01, self.update)

  def update(self):
    time = self.get_clock().now()
    t = (time - self.time_start).nanoseconds * 1e-9
    dt = (time - self.prev_time).nanoseconds * 1e-9
    self.prev_time = time

    # joint trajectories
    q1 = np.pi*np.sin(t/4)
    q2 = np.pi*np.sin(t/4)
    q3 = np.pi/2*np.sin(t/4)

    # corrected: the template had twice the time derivative of q (pi/2, pi/2, pi/4),
    # d/dt [a*sin(t/4)] = a/4*cos(t/4)
    q1_dot = np.pi/4*np.cos(t/4)
    q2_dot = np.pi/4*np.cos(t/4)
    q3_dot = np.pi/8*np.cos(t/4)

    q = np.array([q1, q2, q3])
    qdot = np.array([q1_dot, q2_dot, q3_dot])

    self.robot.set_kinematics(q, qdot)
    self.robot.update_kinematics()
    self.robot.update_differential_kinematics(dt)

def main(args=None):
  rclpy.init(args=args)

  node = UR10Node()
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
