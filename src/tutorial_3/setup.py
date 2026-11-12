import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'tutorial_3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='julian',
    maintainer_email='julian.moore@tum.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'rppr_node = tutorial_3.rppr_node:main',
            'ur10_node = tutorial_3.ur10_node:main',
            'ur10_static_node = tutorial_3.ur10_static_node:main',

        ],
    },
)
