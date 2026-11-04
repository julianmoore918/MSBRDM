from setuptools import find_packages, setup

package_name = 'ur_model'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    package_data={
        'ur10_model': ['*.pkl'],
    },
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='devel',
    maintainer_email='devel@todo.todo',
    description='The ur_model package',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'ur10_model = ur10_model.ur10_model_3dof:main',
    ],
},
)
