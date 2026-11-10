"""Bringup for the UR5 robot in stand alone configuration.

Migrated from the ROS 1 launch file ``bringUR5.launch``.
"""

import os

import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, SetParameter
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package_dir = get_package_share_directory('ursa_apps')
    urdf_path = os.path.join(
        package_dir, 'launch', 'configs', 'robot', 'ur5_robot.urdf.xacro')
    zeros_path = os.path.join(
        package_dir, 'launch', 'configs', 'robot', 'ur5_zeros.yaml')
    rviz_config_path = os.path.join(
        package_dir, 'launch', 'configs', 'robot_ur5.rviz')

    # ROS 1: <rosparam command="load" file=".../ur5_zeros.yaml"/>
    with open(zeros_path, 'r', encoding='utf-8') as zeros_file:
        zeros_params = yaml.safe_load(zeros_file)['zeros']

    def start_nodes(context, *args, **kwargs):
        load_robot_description = context.perform_substitution(
            LaunchConfiguration('load_robot_description')).strip().lower() == 'true'
        gui = context.perform_substitution(LaunchConfiguration('gui')).strip().lower() == 'true'
        # The name of the parameter under which the URDF is loaded
        robot_description_name = context.perform_substitution(
            LaunchConfiguration('robot_description'))
        # ROS 1: <rosparam param="source_list">$(arg list)</rosparam>
        source_list = yaml.safe_load(
            context.perform_substitution(LaunchConfiguration('list')))

        nodes = []

        # joinstate
        if gui:
            # ROS 1: joint_state_publisher with use_gui:=$(arg gui)
            nodes.append(Node(
                package='joint_state_publisher_gui',
                executable='joint_state_publisher_gui',
                name='joint_state_publisher',
            ))
        else:
            nodes.append(Node(
                package='joint_state_publisher',
                executable='joint_state_publisher',
                name='joint_state_publisher',
                parameters=[{'source_list': source_list}],
            ))

        # robot_description (only when the URDF is loaded by this launch file)
        robot_description = None
        if load_robot_description:
            # ROS 1: xacro '$(find ursa_apps)/launch/configs/robot/ur5_robot.urdf.xacro' \
            #          prefix:=$(arg robot_prefix)_ limited:=$(arg joint_limited)
            robot_description = ParameterValue(
                Command([
                    'xacro ', urdf_path,
                    ' prefix:=', LaunchConfiguration('robot_prefix'), '_',
                    ' limited:=', LaunchConfiguration('joint_limited'),
                ]),
                value_type=str)

        # robotstate
        nodes.append(Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=([{robot_description_name: robot_description}]
                        if load_robot_description else []),
        ))

        nodes.append(Node(
            package='rviz2',
            executable='rviz2',
            name='rviz',
            arguments=['-d', rviz_config_path],
            parameters=([{robot_description_name: robot_description}]
                        if load_robot_description else []),
        ))

        return nodes

    return LaunchDescription([
        DeclareLaunchArgument(
            'load_robot_description',
            default_value='true',
            description='Load the robot description (URDF)'),
        DeclareLaunchArgument(
            'joint_limited',
            default_value='false',
            description='If true, limits joint range [-PI, PI] on all joints.'),
        DeclareLaunchArgument(
            'robot_prefix',
            default_value='ursa',
            description='Prefix for the robot links and joints'),
        DeclareLaunchArgument(
            'gui',
            default_value='false',
            description='If true, use the GUI version of the joint state publisher'),
        DeclareLaunchArgument(
            'list',
            default_value='[' + LaunchConfiguration('robot_prefix') + '_joint_states]',
            description='List of topics to subscribe for the joint states'),
        # The name of the parameter under which the URDF is loaded
        DeclareLaunchArgument(
            'robot_description',
            default_value='robot_description',
            description='The name of the parameter under which the URDF is loaded'),

        # loading the Home position for the UR5 robot
        SetParameter('zeros', value=zeros_params),

        OpaqueFunction(function=start_nodes),
    ])
