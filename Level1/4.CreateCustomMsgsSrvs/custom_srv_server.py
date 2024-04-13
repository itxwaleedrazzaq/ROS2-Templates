import rclpy
from rclpy.node import Node
from custom_msgs_srvs.srv import CustomSrvs


class CustomSrvServer(Node):
    def __init__(self):
        super().__init__('CustomSrvServer')
        self.service = self.create_service(CustomSrvs,'RectangleArea',self.callback_Compute)
        self.get_logger().info('Custom SERVER  has been started')

    def callback_Compute(self,request,response):
        response.area = (request.length + request.width)/2
        return response

def main(args=None):
    rclpy.init(args=args)
    node = CustomSrvServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()