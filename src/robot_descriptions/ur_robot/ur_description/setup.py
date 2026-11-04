from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'ur_description'

data_files = [
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml', 'CHANGELOG.rst']),
    ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ('share/' + package_name + '/urdf', glob('urdf/*.xacro')),
    ('share/' + package_name + '/cfg', glob('cfg/*')),
]

# meshes contain sub-directories (ur3/ur5/ur10 x visual/collision).
# data_files copies each file into the target directory, so one entry per
# directory is required to keep the sub-directory layout intact.
for root, _, files in os.walk('meshes'):
    if not files:
        continue
    rel_root = os.path.relpath(root, 'meshes')
    target = 'share/' + package_name + '/meshes'
    if rel_root != '.':
        target += '/' + rel_root
    data_files.append((target, [os.path.join(root, file) for file in files]))

setup(
    name=package_name,
    version='1.2.7',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Miguel Prada Sarasola',
    maintainer_email='miguel.prada@tecnalia.com',
    description='URDF description for Universal UR5/10 robot arms',
    license='BSD',
)
