import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    controller_config = os.path.join(get_package_share_directory('ackermann_bringup'),'config', 'acks_param.yaml')
    xacro_file = os.path.join(get_package_share_directory('ackermann_bringup'),'urdf','main.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {"robot_description": robot_description_config.toxml()}

    node_gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ackermann_bringup'), 'launch', 'gazebo.launch.py')]))

    node_controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, controller_config])
    delayed_controller_manager = TimerAction(period=14.0, actions=[node_controller_manager])

    
    node_cont_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["acks_cont", "joint_broad"])

    delayed_acks_spawners = TimerAction(period=20.0, actions=[node_cont_spawner])

       
    return LaunchDescription([
        node_gazebo,
        delayed_controller_manager,
        delayed_acks_spawners,
    ])