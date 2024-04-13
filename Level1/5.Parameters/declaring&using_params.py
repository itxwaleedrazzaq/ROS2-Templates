import rclpy
from rclpy.node import Node

class SampleParameter(Node):
    def __init__(self):
        super().__init__('sample_parameter') #sample 

        #declaring parameters with initial value
        self.declare_parameter('reset_value',10)
        #using the declared parameter
        self.reset_value = self.get_parameter('reset_value').value

        self.counter = 0
        self.timer = self.create_timer(0.5,self.counter_callback)

    def counter_callback(self):
        self.get_logger().info(str(self.counter))
        self.counter+=1
        if self.counter >= 10:
            self.counter=0
    

def main(args=None):
    rclpy.init(args=args)
    node = SampleParameter()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()