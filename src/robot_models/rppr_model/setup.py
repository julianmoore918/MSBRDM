from setuptools import find_packages, setup

package_name = 'rppr_model'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='swl',
    maintainer_email='swl@todo.todo',
    description='The rppr_model package',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'rppr_model = rppr_model.rppr_model:main',
    ],
},
)
