import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts #this is a builtin servoce
from functools import partial


class ExampleClient(Node):
    def __init__(self):
        super().__init__('ExampleServer')
        self.client_add_two_ints(7,6)

    def client_add_two_ints(self,a,b):
        client = self.create_client(AddTwoInts,'add_two_ints')
        while not client.wait_for_service(1.0):
            self.get_logger().warn('WAITING for Client')
        
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_add_two_ints,a=a,b=b))
    
    def callback_add_two_ints(self,future,a,b):
        try:
            response = future.result()
            self.get_logger().info('Performing addition and result is' + str(response))
        except Exception as e:
            self.get_logger().error('Serivice Call failed')


def main(args=None):
    rclpy.init(args=args)
    node = ExampleClient()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()