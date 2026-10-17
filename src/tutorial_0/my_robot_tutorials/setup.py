from setuptools import find_packages, setup

package_name = 'my_robot_tutorials'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/launch',
                    ['launch/test_import_3.launch.py',
                     'launch/test_import_3.launch.xml',
                     'launch/test_import_3.launch.yaml',]
        ),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rogelio',
    maintainer_email='rogelio.guadarrama@tum.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test_import_1 = my_robot_tutorials.test_import_1:main',
            'test_import_2 = my_robot_tutorials.test_import_2:main',
            'test_import_3 = my_robot_tutorials.test_import_3:main',
        ],
    },
)
