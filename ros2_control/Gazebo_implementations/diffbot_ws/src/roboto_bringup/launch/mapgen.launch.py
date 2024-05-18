from launch import LaunchDescription
from launch_ros.actions import Node
import os
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory, get_package_share_path

def generate_launch_description():

    rviz_config_path = os.path.join(get_package_share_path('roboto_bringup'),'rviz_config', 'genmap.rviz')

    acks_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('roboto_bringup'),
                     'launch/diffcont.launch.py')))
    
    delayed_diff = TimerAction(period=10.0, actions=[acks_launch])
    

    nav2_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('nav2_bringup'),
                     'launch/navigation_launch.py')), launch_arguments={'use_sim_time': 'True'}.items())
    delayed_nav2 = TimerAction(period=4.0, actions=[nav2_launch])

    slam2_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('slam_toolbox'),
                     'launch/online_async_launch.py')), launch_arguments={'use_sim_time': 'True'}.items())
    delayed_slam2 = TimerAction(period=6.0, actions=[slam2_launch])

    initialize_rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d',rviz_config_path],
        parameters=[{'use_sim_time': True}])
    delayed_initialize_rviz = TimerAction(period=8.0, actions=[initialize_rviz])

    return LaunchDescription([
        delayed_initialize_rviz,
        delayed_diff,
        delayed_nav2,
        delayed_slam2,
        
    ])