import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command


def generate_launch_description():
    # UR10 description (xacro) from the ur_description package
    xacro_file = os.path.join(get_package_share_directory('ur_description'),
                              'urdf', 'ur10_robot.urdf.xacro')
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)

    rviz_config = os.path.join(get_package_share_directory('tutorial_4'),
                               'rviz', 'ur10_kinematic_control.rviz')

    return LaunchDescription([
        # 1. samples the workspace, publishes the point clouds and shows the
        #    robot in the configuration with maximum manipulability
        Node(package='tutorial_4', executable='ur10_kinematic_control_node',
             name='ur10_kinematic_control_node', output='screen'),
        # 2. shows the robot meshes from the URDF
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             name='robot_state_publisher', output='screen',
             parameters=[{'robot_description': robot_description}]),
        # 3. visualization
        Node(package='rviz2', executable='rviz2', name='rviz2', output='screen',
             arguments=['-d', rviz_config]),
    ])