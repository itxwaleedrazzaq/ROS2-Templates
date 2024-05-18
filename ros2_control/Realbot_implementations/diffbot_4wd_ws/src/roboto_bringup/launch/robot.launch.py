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



package_name = 'roboto_bringup'

def generate_launch_description():

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('roboto_bringup'))
    xacro_file = os.path.join(pkg_path,'roboto_description','main.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file).toxml()

    rviz_config_path = os.path.join(get_package_share_path('roboto_bringup'),
                                    'rviz_config', 'roboto_config.rviz')
    
    # Create a robot_state_publisher node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_config}]
    )

    node_joint_state_publisher = Node(
       package='joint_state_publisher',
       executable='joint_state_publisher',
       name='joint_state_publisher'
   )
    
    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])

    odom_to_base_node = Node(
            package='tf2_ros',
            namespace = 'scan_to_map',
            executable='static_transform_publisher',
            arguments= ["0", "0", "0", "0", "0", "0", "base_link", "odom"]
        )

    controller_params_file = os.path.join(get_package_share_directory(package_name),'config','myparameter.yaml')

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description':robot_description},controller_params_file]
        
    )

    delayed_controller_manager = TimerAction(period=2.0, actions=[controller_manager])

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[diff_drive_spawner],
        )
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_broad_spawner],
        )
    )

    sonar_to_lidar_node = Node(
        package="roboto_processing",
        executable="sonar_to_lidar",
    )


    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )



    # Launch!
    return LaunchDescription([
        node_robot_state_publisher,
        #odom_to_base_node,
        node_joint_state_publisher,
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        sonar_to_lidar_node,
        rviz2_node
    ])