"""Loads the UR3 robot description into the parameter server.

Migrated from the ROS 1 launch file ``ur3_upload.launch``.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package_dir = get_package_share_directory('ur_description')
    urdf_path = os.path.join(package_dir, 'urdf', 'ur3_robot.urdf.xacro')
    urdf_limited_path = os.path.join(
        package_dir, 'urdf', 'ur3_joint_limited_robot.urdf.xacro')

    def start_robot_state_publisher(context, *args, **kwargs):
        limited = context.perform_substitution(LaunchConfiguration('limited'))
        transmission_hw_interface = context.perform_substitution(
            LaunchConfiguration('transmission_hw_interface'))

        xacro_file = urdf_limited_path if limited.strip().lower() == 'true' else urdf_path

        robot_description = ParameterValue(
            Command(['xacro ', xacro_file,
                     ' transmission_hw_interface:=', transmission_hw_interface]),
            value_type=str)

        return [
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                parameters=[{'robot_description': robot_description}],
            ),
        ]

    return LaunchDescription([
        DeclareLaunchArgument(
            'limited',
            default_value='false',
            description='If true, limits joint range [-PI, PI] on all joints.'),
        DeclareLaunchArgument(
            'transmission_hw_interface',
            default_value='hardware_interface/PositionJointInterface'),
        OpaqueFunction(function=start_robot_state_publisher),
    ])
