from setuptools import setup

package_name = 'ur_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=['ur10_robot'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='devel',
    maintainer_email='devel@todo.todo',
    description='The ur_robot package',
    license='TODO',
    tests_require=['pytest'],
)
