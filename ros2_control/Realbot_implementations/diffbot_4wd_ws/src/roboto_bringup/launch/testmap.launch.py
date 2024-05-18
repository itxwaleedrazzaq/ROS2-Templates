from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.substitutions import Command
import os
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_path
import sys
from ament_index_python import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch.actions import TimerAction
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
from ament_index_python.packages import get_package_share_path

def generate_launch_description():



    share_path = get_package_share_path('roboto_bringup')
    rviz_config_path = os.path.join(get_package_share_path('roboto_bringup'),'rviz_config', 'genmap.rviz')

    map_path = os.path.join(share_path,'maps', 'turtle_map.yaml')
    
    roboto_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('roboto_bringup'),'launch/robot_norviz.launch.py')
    ))
    delayed_turtlebot_gazebo = TimerAction(period=3.0, actions=[roboto_launch])

    nav2 = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('nav2_bringup'),
                     'launch/bringup_launch.py')), launch_arguments={'map':str(map_path),}.items())
    delayed_nav2 = TimerAction(period=3.0, actions=[nav2])



    initialize_rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d',rviz_config_path])
    delayed_initialize_rviz = TimerAction(period=8.0, actions=[initialize_rviz])



    return LaunchDescription([
        delayed_nav2,
        delayed_turtlebot_gazebo,
        delayed_initialize_rviz,
        

        
        
    ])