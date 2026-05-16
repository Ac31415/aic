from setuptools import find_packages, setup

package_name = 'smolVLA_short_all_aic_gazebo_dataset_policy_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    # package_data={'smolVLA_short_all_aic_gazebo_dataset_policy_node': ['py.typed', 'pretrained_model/*']},
    package_data={'smolVLA_short_all_aic_gazebo_dataset_policy_node': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ac31415',
    maintainer_email='wcheng3@fau.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
