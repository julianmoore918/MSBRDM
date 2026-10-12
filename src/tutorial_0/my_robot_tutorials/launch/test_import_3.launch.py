from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

print("*******************************")
print("You can do scripting stuff here")
print("*******************************")

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('arg1', default_value='2'),
        DeclareLaunchArgument('arg2', default_value='3'),
        Node(
            package='my_robot_tutorials',
            executable='test_import_3',
            name='test_import_3',
            output='screen',
            parameters=[{
                'arg1': ParameterValue(LaunchConfiguration('arg1'), value_type=int),
                'arg2': ParameterValue(LaunchConfiguration('arg2'), value_type=int),
            }],
        ),
    ])