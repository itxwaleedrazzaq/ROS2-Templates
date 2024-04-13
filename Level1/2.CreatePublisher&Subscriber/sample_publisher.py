import rclpy
from rclpy.node import Node
from std_msgs.msg import String #data type

class SamplePublisher(Node):
    def __init__(self):
        super().__init__('sample_publisher') #sample publisher
        self.publisher = self.create_publisher(String,'message',10)
        self.timer = self.create_timer(0.5,self.publisher_callback)

    def publisher_callback(self):
        msg = String()
        msg.data = 'Test publisher'
        self.get_logger().info('Publishing')
        self.publisher.publish(msg)
    

def main(args=None):
    rclpy.init(args=args)
    node = SamplePublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()