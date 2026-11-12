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

    rviz_config = os.path.join(get_package_share_directory('tutorial_3'), 'rviz', 'ur10.rviz')

    return LaunchDescription([
        # 1. GUI sliders for the joints, starting in the upright pose of Fig. 4
        #    (wrist_1 at -pi/2 as the robot class publishes it, do not move the wrist sliders)
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             name='joint_state_publisher_gui', output='screen',
             parameters=[{'zeros.shoulder_lift_joint': -1.5708,
                          'zeros.wrist_1_joint': -1.5708}]),
        # 2. models the robot: reads /joint_states, broadcasts ee, publishes velocities
        Node(package='tutorial_3', executable='ur10_static_node',
             name='ur10_static_node', output='screen'),
        # 3. shows the robot meshes from the URDF
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             name='robot_state_publisher', output='screen',
             parameters=[{'robot_description': robot_description}]),
        # 4. visualization
        Node(package='rviz2', executable='rviz2', name='rviz2', output='screen',
             arguments=['-d', rviz_config]),
    ])
