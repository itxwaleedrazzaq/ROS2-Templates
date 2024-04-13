import rclpy
from rclpy.node import Node
from custom_msgs_srvs.msg import CustomMsgs

class SamplePublisher(Node):
    def __init__(self):
        super().__init__('sample_publisher') #sample publisher
        self.publisher = self.create_publisher(CustomMsgs,'message',10)
        self.timer = self.create_timer(0.5,self.publisher_callback)

    def publisher_callback(self):
        msg = CustomMsgs()
        msg.int_var = 45
        msg.str_var = 'sample text'
        msg.bool_var = False
        self.get_logger().info('Publishing')
        self.publisher.publish(msg)
    

def main(args=None):
    rclpy.init(args=args)
    node = SamplePublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()