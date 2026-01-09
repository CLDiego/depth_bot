import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():
    # Get the package directory
    depth_bot_dir = get_package_share_directory('depth_both')

    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(depth_bot_dir, 'launch', 'rsp.launch.py')
        ), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        )
    )

    spawn_depth_bot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[ '-topic', 'robot_description',
                    '-entity', 'depth_bot',
        ],
        output='screen'
    )

    return LaunchDescription([
        rsp_launch,
        gazebo_launch,
        spawn_depth_bot,
    ])

    