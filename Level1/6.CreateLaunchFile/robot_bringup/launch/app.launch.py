from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    sample_pub_node = Node(
        package='pkg_name',
        executable='node_name'
    )
    ld.add_action(sample_pub_node)
    return ld