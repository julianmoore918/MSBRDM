import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def load_zeros(zeros_path):
    with open(zeros_path, 'r', encoding='utf-8') as zeros_file:
        data = yaml.safe_load(zeros_file) or {}

    # ROS 2 format: unwrap '/**' -> 'ros__parameters'
    if '/**' in data:
        data = data.get('/**') or {}
    if 'ros__parameters' in data:
        data = data.get('ros__parameters') or {}

    zeros = data.get('zeros')
    if not isinstance(zeros, dict) or not zeros:
        raise RuntimeError(
            f"No 'zeros' entries found in {zeros_path}. Expected "
            "'/**: ros__parameters: zeros: {joint_name: value}'.")

    return {f'zeros.{joint}': float(value) for joint, value in zeros.items()}

def generate_launch_description():
    package_dir = get_package_share_directory('ursa_apps')
    urdf_path = os.path.join(
        package_dir, 'launch', 'configs', 'robot', 'ur10_robot.urdf.xacro')
    zeros_path = os.path.join(
        package_dir, 'launch', 'configs', 'robot', 'ur10_zeros.yaml')
    rviz_config_path = os.path.join(
        package_dir, 'launch', 'configs', 'robot_ur10.rviz')

    # ROS 1: <rosparam command="load" file=".../ur10_zeros.yaml"/>
    zeros_params = load_zeros(zeros_path)

    def start_nodes(context, *args, **kwargs):
        load_robot_description = context.perform_substitution(
            LaunchConfiguration('load_robot_description')).strip().lower() == 'true'
        gui = context.perform_substitution(LaunchConfiguration('gui')).strip().lower() == 'true'
        # The name of the parameter under which the URDF is loaded
        robot_description_name = context.perform_substitution(
            LaunchConfiguration('robot_description'))
        # ROS 1: <rosparam param="source_list">$(arg list)</rosparam>
        source_list = yaml.safe_load(
            context.perform_substitution(LaunchConfiguration('list'))) or []

        nodes = []

        # joint state publisher: rate, source topics and home position (zeros)
        joint_state_params = {'rate': 50}
        if source_list:  # an empty list has no inferable type in ROS 2
            joint_state_params['source_list'] = source_list

        if gui:
            # ROS 1: joint_state_publisher_gui node
            # (name: joint_state_publisher_msd3dof_gui)
            nodes.append(Node(
                package='joint_state_publisher_gui',
                executable='joint_state_publisher_gui',
                name='joint_state_publisher_msd3dof_gui',
                parameters=[joint_state_params, zeros_params],
            ))
        else:
            nodes.append(Node(
                package='joint_state_publisher',
                executable='joint_state_publisher',
                name='joint_state_publisher',
                parameters=[joint_state_params, zeros_params],
            ))

        # robot_description (only when the URDF is loaded by this launch file)
        robot_description_params = []
        if load_robot_description:
            # ROS 1: xacro '$(find ursa_apps)/launch/configs/robot/ur10_robot.urdf.xacro' \
            #          prefix:=$(arg robot_prefix)_ limited:=$(arg joint_limited)
            robot_description = ParameterValue(
                Command([
                    'xacro ', urdf_path,
                    ' prefix:=', LaunchConfiguration('robot_prefix'), '_',
                    ' limited:=', LaunchConfiguration('joint_limited'),
                ]),
                value_type=str)
            robot_description_params = [{robot_description_name: robot_description}]

        # robotstate (ROS 2 name of the old 'rate' parameter: publish_frequency)
        nodes.append(Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'publish_frequency': 50.0}] + robot_description_params,
        ))

        nodes.append(Node(
            package='rviz2',
            executable='rviz2',
            name='rviz',
            arguments=['-d', rviz_config_path],
            parameters=robot_description_params,
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
            default_value=['[', LaunchConfiguration('robot_prefix'), '_joint_states]'],
            description='List of topics to subscribe for the joint states'),
        # The name of the parameter under which the URDF is loaded
        DeclareLaunchArgument(
            'robot_description',
            default_value='robot_description',
            description='The name of the parameter under which the URDF is loaded'),

        OpaqueFunction(function=start_nodes),
    ])