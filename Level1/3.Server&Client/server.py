import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts #this is a builtin servoce


class ExampleServer(Node):
    def __init__(self):
        super().__init__('ExampleServer')
        self.service = self.create_service(AddTwoInts,'add_two_ints',self.callback_add_two_ints)
        self.get_logger().info('SERVER  has been started')

    def callback_add_two_ints(self,request,response):
        response.sum = request.a + request.b
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ExampleServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()