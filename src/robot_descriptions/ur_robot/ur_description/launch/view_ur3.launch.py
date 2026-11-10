"""Displays the UR3 robot in rviz2.

Migrated from the ROS 1 launch file ``view_ur3.launch``.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package_dir = get_package_share_directory('ur_description')
    upload_launch = os.path.join(package_dir, 'launch', 'ur3_upload.launch.py')
    rviz_config_path = os.path.join(package_dir, 'cfg', 'view_robot.rviz')
    urdf_path = os.path.join(package_dir, 'urdf', 'ur3_robot.urdf.xacro')
    urdf_limited_path = os.path.join(
        package_dir, 'urdf', 'ur3_joint_limited_robot.urdf.xacro')

    def start_viewer_nodes(context, *args, **kwargs):
        limited = context.perform_substitution(LaunchConfiguration('limited'))
        transmission_hw_interface = context.perform_substitution(
            LaunchConfiguration('transmission_hw_interface'))

        xacro_file = urdf_limited_path if limited.strip().lower() == 'true' else urdf_path

        robot_description = ParameterValue(
            Command(['xacro ', xacro_file,
                     ' transmission_hw_interface:=', transmission_hw_interface]),
            value_type=str)

        return [
            # ROS 1: joint_state_publisher node with use_gui:=true
            Node(
                package='joint_state_publisher_gui',
                executable='joint_state_publisher_gui',
                name='joint_state_publisher',
            ),
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz',
                arguments=['-d', rviz_config_path],
                parameters=[{'robot_description': robot_description}],
                # ROS 1: this node had required="true"
                # (no direct equivalent in ROS 2 launch)
            ),
        ]

    return LaunchDescription([
        # Sets the robot_description parameter and starts robot_state_publisher
        IncludeLaunchDescription(PythonLaunchDescriptionSource(upload_launch)),
        OpaqueFunction(function=start_viewer_nodes),
    ])
