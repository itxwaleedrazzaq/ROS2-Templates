import rclpy
from rclpy.node import Node

class SampleNode(Node):
    def __init__(self):
        super().__init__('sample_node') #sample node
        self.counter = 0
        self.timer = self.create_timer(0.5,self.counter_callback)

    def counter_callback(self):
        self.get_logger().info(str(self.counter))
        self.counter+=1
        
def main(args=None):
    rclpy.init(args=args)
    node = SampleNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()