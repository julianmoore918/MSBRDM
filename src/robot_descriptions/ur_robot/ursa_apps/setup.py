from glob import glob
import os
from setuptools import setup

package_name = 'ursa_apps'

setup(
    name=package_name,
    version='0.0.0',
    # no python modules in this package, data only (launch files, configs)
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml', 'README.txt']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/launch/configs',
            [f for f in glob('launch/configs/*') if os.path.isfile(f)]),
        ('share/' + package_name + '/launch/configs/robot',
            [f for f in glob('launch/configs/robot/*') if os.path.isfile(f)]),
    ],
    install_requires=['setuptools', 'pyyaml'],
    zip_safe=True,
    maintainer='Florian Bergner',
    maintainer_email='florian.bergner@tum.de',
    description='Apps for UR robot in stand alone configuration',
    license='BSD',
)
