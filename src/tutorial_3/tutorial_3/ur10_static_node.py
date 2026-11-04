#!/usr/bin/env python3
"""
UR10 Static Node
This node subscribes to joint states from the GUI and updates the forward
kinematics of the robot
"""
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.impl.implementation_singleton import rclpy_implementation as _rclpy
from sensor_msgs.msg import JointState

from ur10_model.ur10_model_3dof import UR10Model3DOF
from ur10_robot.ur10_robot_3dof import UR10Robot3DOF


class UR10StaticNode(Node):

  def __init__(self):
    super().__init__('ur10_static_node')

    # latest joint states from the GUI
    self.latest_q = None
    self.joint_states_sub = self.create_subscription(
      JointState, '/joint_states', self.joint_states_callback, 10)

    # initialize model and robot
    self.model = UR10Model3DOF()
    self.robot = UR10Robot3DOF(self.model, q_init=np.array([0, -np.pi/2, 0]),
                               node=self)

    self.prev_time = self.get_clock().now()
    self.timer = self.create_timer(0.01, self.update)

  def joint_states_callback(self, msg: JointState):
    self.latest_q = np.array(msg.position)

  def update(self):
    q_full = self.latest_q
    # wait for the first joint state message from the GUI
    if q_full is None:
      return

    time = self.get_clock().now()
    dt = (time - self.prev_time).nanoseconds * 1e-9
    self.prev_time = time

    q = q_full[0:3]
    q[1] += np.pi/2
    qdot = np.zeros(self.model.nq)

    # update forward kinematics
    self.robot.set_kinematics(q, qdot)
    self.robot.update_kinematics()
    self.robot.update_differential_kinematics(dt)


def main(args=None):
  rclpy.init(args=args)
  node = UR10StaticNode()
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
