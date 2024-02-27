from setuptools import find_packages, setup

package_name = 'odometry'
submodule = "odometry/mono_optical_flow_calc"

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
    maintainer='jaidenwlee',
    maintainer_email='jaidenwlee@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "odometry_node = odometry.mono_optical_flow_odom_node:main"
        ],
    },
)
