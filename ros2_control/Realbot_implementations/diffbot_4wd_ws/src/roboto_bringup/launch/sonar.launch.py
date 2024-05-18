from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.substitutions import Command
import os
from ament_index_python.packages import get_package_share_path
import launch.actions

def generate_launch_description():
    # Docker command
    docker_cmd = launch.actions.ExecuteProcess(
        cmd=[
            "docker", "run", "-it", "--rm", "-v", "/dev:/dev", 
            "--privileged", "--net=host", "microros/micro-ros-agent:humble", 
            "serial", "--dev", "/dev/ttyACM0", "-b", "115200"
        ],
        output='screen'
    )

    # rviz2 node
    rviz_config_path = os.path.join(get_package_share_path('roboto_bringup'),
                                    'rviz_config', 'sonar_config.rviz')
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )

    return LaunchDescription([
        rviz2_node,
        # docker_cmd,
        
    ])
