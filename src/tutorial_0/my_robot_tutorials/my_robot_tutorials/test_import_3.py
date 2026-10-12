#!/usr/bin/env python3

import rclpy

from my_python_libs.python_lib_1 import say_it_works
from my_python_libs.python_lib_2 import libpy2

from my_other_python_libs.other_python_lib_1 import say_it_again
from my_other_python_libs.other_python_lib_2 import libpy3


def main(args=None):
    rclpy.init(args=args)  # pass args so ROS can parse --ros-args
    node = rclpy.create_node('test_node')

    # Declare parameters with defaults
    node.declare_parameter('arg1', 2)
    node.declare_parameter('arg2', 3)

    arg1 = node.get_parameter('arg1').value
    arg2 = node.get_parameter('arg2').value

    say_it_works()
    lib2instance = libpy2(arg1, arg2)
    lib2instance.say_it_too(node)
    lib2instance.calculate(node)
    say_it_again()
    lib3instance = libpy3(arg1, arg2)
    lib3instance.say_it_too(node)
    lib3instance.calculate(node)
    print("End of script")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()