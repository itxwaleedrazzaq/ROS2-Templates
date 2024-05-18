#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import LaserScan,Range
from geometry_msgs.msg import *
import numpy as np
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
import time
from itertools import count
import math
from std_msgs.msg import Int32
 
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from sensor_msgs.msg import LaserScan, Range
import math


class LaserNode(Node):
    def __init__(self):
        super().__init__('sonar_to_lidar')
        qos_profile = QoSProfile(depth=10)
        self.lidar_publisher = self.create_publisher(LaserScan, "/scan", 10)
        self.sonar_subscriber = self.create_subscription(Range, '/pico/range', self.sonar_callback, qos_profile)

    def sonar_callback(self, sonar_msg):
        lidar_msg = LaserScan()
        lidar_msg.header.frame_id = 'base_link'
        lidar_msg.header.stamp = self.get_clock().now().to_msg()
        lidar_msg.range_min = sonar_msg.min_range
        lidar_msg.range_max = sonar_msg.max_range
        lidar_msg.angle_min = -10*math.pi/180
        lidar_msg.angle_max = 10*math.pi/180
        lidar_msg.angle_increment = math.pi/180
        lidar_msg.time_increment = 0.01
        lidar_msg.scan_time = 0.001
        lidar_msg.ranges = [sonar_msg.range]*21
        lidar_msg.intensities = []
        self.lidar_publisher.publish(lidar_msg)

def main(args=None):
    rclpy.init(args=args)
    laser_node = LaserNode()
    rclpy.spin(laser_node)
    laser_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
