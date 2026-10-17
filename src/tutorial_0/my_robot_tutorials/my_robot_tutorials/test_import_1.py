#!/usr/bin/env py -3

import rclpy

from my_python_libs.python_lib_1 import say_it_works

def main(args=None):
    rclpy.init()   
    say_it_works()

    print("End of script")

    rclpy.shutdown()

if __name__ == '__main__':
    main()
