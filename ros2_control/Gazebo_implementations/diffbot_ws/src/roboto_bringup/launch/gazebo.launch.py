import os
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_path,get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    urdf_path = os.path.join(get_package_share_path('roboto_bringup'),'roboto_description', 'main.urdf.xacro')
    world = os.path.join(get_package_share_path('roboto_bringup'), 'worlds', 'my.world')  # Update with your world file path
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': True}])

    node_joint_state_publisher = Node(
       package='joint_state_publisher',
       executable='joint_state_publisher',
       parameters=[{'use_sim_time': True}])
    
    node_gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'world': world}.items(),)
    
    node_spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'diffdrive_gazebo_bot'],output='screen')


    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher,
        node_gazebo,
        node_spawn_entity,
    ])

