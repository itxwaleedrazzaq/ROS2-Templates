import rclpy
from rclpy.node import Node
from custom_msgs_srvs.msg import CustomMsgs

class CustomMsgSubscriber(Node):
    def __init__(self):
        super().__init__('sampleSubscriber')
        self.subscriber = self.create_subscription(CustomMsgs,'custom_message',self.subscriber_callback,10)
    
    def subscriber_callback(self,msg):
        self.get_logger().info(str(msg.int_var))
    

def main(args=None):
    rclpy.init(args=args)
    node = CustomMsgSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()