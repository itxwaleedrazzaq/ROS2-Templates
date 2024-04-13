import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SampleSubscriber(Node):
    def __init__(self):
        super().__init__('sampleSubscriber')
        self.subscriber = self.create_subscription(String,'message',self.subscriber_callback,10)
    
    def subscriber_callback(self,msg):
        self.get_logger().info(msg.data)
    

def main(args=None):
    rclpy.init(args=args)
    node = SampleSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()