#!/usr/bin/env python3
"""
RPPR Static Node
This node subscribes to joint states from the GUI and updates the forward
kinematics of the robot
"""
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.impl.implementation_singleton import rclpy_implementation as _rclpy
from sensor_msgs.msg import JointState

from rppr_model.rppr_model import RPPRModel
from rppr_robot.rppr_robot import RPPRRobot


class RPPRStaticNode(Node):

  def __init__(self):
    super().__init__('rppr_static_node')

    # latest joint states from the GUI
    self.latest_q = None
    self.joint_states_sub = self.create_subscription(
      JointState, '/joint_states', self.joint_states_callback, 10)

    # initialize model and robot
    self.model = RPPRModel()
    self.robot = RPPRRobot(self.model, node=self)

    self.timer = self.create_timer(0.01, self.update)

  def joint_states_callback(self, msg: JointState):
    self.latest_q = np.array(msg.position)

  def update(self):
    q = self.latest_q
    # wait for the first joint state message from the GUI
    if q is None:
      return
    qdot = np.zeros(self.model.nq)
    # update forward kinematics
    self.robot.update_kinematics(q, qdot)


def main(args=None):
  rclpy.init(args=args)
  node = RPPRStaticNode()
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
