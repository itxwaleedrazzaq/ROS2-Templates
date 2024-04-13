import rclpy
from rclpy.node import Node
from functools import partial
from custom_msgs_srvs.srv import CustomSrvs


class CustomSrvClient(Node):
    def __init__(self):
        super().__init__('CustomSrvClient')
        self.client_RectArea(7.0,6.1)

    def client_RectArea(self,length,width):
        client = self.create_client(CustomSrvs,'RectangleArea')
        while not client.wait_for_service(1.0):
            self.get_logger().warn('WAITING for Server')
        
        request = CustomSrvs.Request()
        request.length = length
        request.width = width
        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_RectArea,length=length,width=width))
    
    def callback_RectArea(self,future,length,width):
        try:
            response = future.result()
            self.get_logger().info('Performing addition and result is ' + str(response.area))
        except Exception as e:
            self.get_logger().error('Service Call failed')


def main(args=None):
    rclpy.init(args=args)
    node = CustomSrvClient()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()