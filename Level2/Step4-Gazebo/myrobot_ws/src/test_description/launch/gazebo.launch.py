import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_path

def generate_launch_description():
    urdf = os.path.join(get_package_share_path('test_description'), 'urdf', 'test.urdf.xacro')
    world = os.path.join(get_package_share_path('test_description'), 'worlds', 'test.world')  # Update with your world file path
    robot_description = ParameterValue(Command(['xacro ', urdf]), value_type=str)
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    rviz_config_path = os.path.join(get_package_share_path('test_description'),'rviz_config', 'test.rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', world],  # Add the world argument
            output='screen'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time,
                         'robot_description': robot_description}],
            arguments=[urdf]),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='my_robot',
            output='screen',
            arguments=["-topic", "/robot_description", "-entity", "my_robot"]),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='gazebo_world',
            output='screen',
            arguments=["-topic", "/gazebo/world", "-entity", "gazebo", "-file", world]),
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=['-d', rviz_config_path]),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui")
    ])
