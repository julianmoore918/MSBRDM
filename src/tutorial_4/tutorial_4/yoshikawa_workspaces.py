#!/usr/bin/env python3
import struct
import numpy as np
import pandas as pd
import colorcet as cc

import rclpy
from rclpy.node import Node
from rclpy.impl.implementation_singleton import rclpy_implementation as _rclpy
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import sensor_msgs_py.point_cloud2 as pc2

from ur10_model.ur10_model_3dof import UR10Model3DOF
from ur10_robot.ur10_robot_3dof import UR10Robot3DOF


class ManipulabilityVisualizer(Node):

    def __init__(self):
        super().__init__('manipulability_visualizer_node')

        self.singularity_cloud_pub = self.create_publisher(PointCloud2, '/singularity_points', 10)
        self.workspace_cloud_pub = self.create_publisher(PointCloud2, '/workspace_points', 10)

        # initialize model and robot
        model = UR10Model3DOF()
        self.robot = UR10Robot3DOF(model, node=self)

        # TODO: set the threshold for singularity
        self.threshold = 

        # colormap
        self.cmap = cc.rainbow_bgyrm_35_85_c69

        num_samples = 5000
        self.get_logger().info('Generating manipulability samples...')

        df = pd.DataFrame(columns=['point.x', 'point.y', 'point.z', 'w'])
        w_max = 0
        q_max = np.zeros(3)

        for i in range(num_samples):
            # generate random joint configuration
            q = np.random.uniform(-np.pi, np.pi, 3)
            # TODO: calculate the end-effector position x_ee_w from the model
            x =

            # TODO: calculate the end-effector Jacobian J_ee_w from the model
            J = 

            # TODO: calculate the manipulability index with the linear part of Jacobian
            w =

            # TODO: save the maximum manipulability index and the corresponding joint configuration
            w_max
            q_max

            # save the position and manipulability index into the dataframe
            df.loc[i] = [x[0], x[1], x[2], w]

        self.q_max = q_max

        # TODO: print out the maximum manipulability index and the corresponding joint configuration
        

        # create the point clouds
        self.singularity_cloud, self.workspace_cloud = self.create_clouds(df)

        # publish at 1 Hz, as in the ROS 1 version
        self.timer = self.create_timer(1.0, self.update)

    def create_clouds(self, df):
        # retrieve end-effector positions and manipulability indices from dataframe
        pt = np.array(df[['point.x', 'point.y', 'point.z']])
        w = np.array(df['w'])

        # TODO: calculate the max value of manipulability index
        wmax = np.max(w)

        # list of singularity points and workspace points
        singularity_points = []
        workspace_points = []

        # point cloud fields (ROS 2 messages take keyword args only)
        fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
            PointField(name='rgba', offset=12, datatype=PointField.UINT32, count=1),
        ]

        for i in range(len(w)):
            # TODO: calculate the color index (0-255) based on the manipulability index (0-wmax)
            color_index =
            # TODO: retrieve the RGB values from the colormap with the color index,
            # and convert the values to 0-255 range intergers
            r, g, b =
            a = 255
            # pack the rbga values into a 32-bit integer format
            rgba = struct.unpack('I', struct.pack('BBBB', b, g, r, a))[0]

            # TODO: create a point with color as the fields [x, y, z, rgba]
            p = []

            # TODO: save the point into either singularity_points or workspace_points
            # based on the manipulability index
            

        # TODO: create point clouds with the fields and points using pc2.create_cloud()
        
        return singularity_cloud, workspace_cloud

    def publish(self):
        #TODO: update the timestamp of the point clouds, and update the point clouds


    def update(self):
        # publish the point clouds
        self.publish()

        # visualize the robot with the joint configuration with maximum manipulability index
        self.robot.set_kinematics(self.q_max, qdot=np.zeros(3))
        self.robot.update_kinematics()
        self.robot.update_differential_kinematics(1.0)


def main(args=None):
    rclpy.init(args=args)
    node = ManipulabilityVisualizer()
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
