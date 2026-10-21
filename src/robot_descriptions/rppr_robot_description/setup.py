from setuptools import find_packages, setup

package_name = 'rppr_robot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        #ToDo: declare all the needed files to be installed
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your name',
    maintainer_email='your@email',
    description='The robot description package',
    license='TUM',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        #ToDo: declare entry points if needed.
        ],
    },
)
