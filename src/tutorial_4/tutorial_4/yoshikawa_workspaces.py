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
        # 0.1 ≈ 24% of w_max ≈ 0.42; chosen to visualise the near-singular regions
        self.threshold = 0.1

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
            T_ee_w = np.array(self.robot.model.T_ee_w_fn(*q), dtype=float)
            x = T_ee_w[0:3, 3]


            # TODO: calculate the end-effector Jacobian J_ee_w from the model
            J = np.array(self.robot.model.J_ee_w_fn(*q), dtype=float)[3:6, :]

            # TODO: calculate the manipulability index with the linear part of Jacobian
            w = np.sqrt(max(np.linalg.det(J @ J.T), 0.0))

            # TODO: save the maximum manipulability index and the corresponding joint configuration
            if w > w_max:
                w_max = w
                q_max = q

            # save the position and manipulability index into the dataframe
            df.loc[i] = [x[0], x[1], x[2], w]

        self.q_max = q_max

        # TODO: print out the maximum manipulability index and the corresponding joint configuration
        self.get_logger().info(
            f'Maximum manipulability index w_max = {w_max:.4f} at '
            f'q_max = {np.round(q_max, 3)} rad ({np.round(np.degrees(q_max), 1)} deg)')

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
            color_index = int((1.0 - w[i] / wmax) * 255)
            # TODO: retrieve the RGB values from the colormap with the color index,
            # and convert the values to 0-255 range intergers
            r, g, b = (np.array(self.cmap[color_index][0:3]) * 255).astype(int)
            a = 255
            # pack the rbga values into a 32-bit integer format
            rgba = struct.unpack('I', struct.pack('BBBB', b, g, r, a))[0]

            # TODO: create a point with color as the fields [x, y, z, rgba]
            p = []
            p.append(pt[i][0])
            p.append(pt[i][1])
            p.append(pt[i][2])
            p.append(rgba)

            # TODO: save the point into either singularity_points or workspace_points
            # based on the manipulability index
            if w[i] < self.threshold:
                singularity_points.append(p)
            else:
                workspace_points.append(p)
            

        # TODO: create point clouds with the fields and points using pc2.create_cloud()
        singularity_cloud = pc2.create_cloud(Header(frame_id='world'), fields, singularity_points)
        workspace_cloud = pc2.create_cloud(Header(frame_id='world'), fields, workspace_points)
        return singularity_cloud, workspace_cloud

    def publish(self):
        #TODO: update the timestamp of the point clouds, and update the point clouds
        self.singularity_cloud.header.stamp = self.get_clock().now().to_msg()
        self.workspace_cloud.header.stamp = self.get_clock().now().to_msg()
        self.singularity_cloud_pub.publish(self.singularity_cloud)
        self.workspace_cloud_pub.publish(self.workspace_cloud)

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

    # Q6: analytic maximum of the manipulability index
    # With L34 = L3 + L4, the linear Jacobian of the 3-DOF UR10 gives
    #   w = |det(J_v)| = L2 * L34 * |sin(q3)| * |L2 sin(q2) + L34 sin(q2 + q3)|
    # - q1 does not appear: w is the same for every base rotation.
    # - The last factor is the horizontal distance r of the wrist from the base
    #   axis. For a given q3 it is largest (= shoulder-wrist distance
    #   d = sqrt(L2^2 + L34^2 + 2 L2 L34 cos(q3))) when the line from the
    #   shoulder to the wrist is horizontal.
    # - So we maximise f(q3) = sin(q3) * sqrt(a + b cos(q3)) with
    #   a = L2^2 + L34^2, b = 2 L2 L34. Setting df/dq3 = 0 gives
    #   3b c^2 + 2a c - b = 0  ->  c = cos(q3) = (-a + sqrt(a^2 + 3b^2)) / (3b)
    # With L2 = 0.6127, L34 = 0.6873:
    #   cos(q3) = 0.332  ->  q3 = +-70.6 deg,  d = 1.062 m
    #   w_max = L2 * L34 * sin(q3) * d = 0.4218
    # The sampled maximum (~0.42) matches. Being random samples, it is always
    # slightly below the analytic value.


if __name__ == '__main__':
    main()
