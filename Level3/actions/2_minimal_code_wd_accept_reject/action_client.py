import rclpy
from rclpy.node import Node
from custom_actions.action import CustomAction
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus


class SampleCustomActionClient(Node):
    def __init__(self):
        super().__init__('sample_custom_action_client') #sample node
        self.action_client = ActionClient(self,CustomAction,'count_until')

    def send_goal(self,target_number,period):
        #wait for server
        self.action_client.wait_for_server()
        #create a goal
        goal = CustomAction.Goal()
        goal.target_number = target_number
        goal.period = period

        #send the goal and receive feedback
        self.get_logger().info('Sending Goal')
        self.action_client.send_goal_async(goal).add_done_callback(self.goal_response_callback)


    def goal_response_callback(self,future):
        #get result
        self.goal_handle : ClientGoalHandle = future.result()
        if self.goal_handle.accepted:
            self.get_logger().info('Goal is validated hence accepted - client side')
            self.goal_handle.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().warn('Goal is not validated hence rejected - client side')
    
    def goal_result_callback(self,future):
        #checking goal status machine
        result = future.result().result
        self.get_logger().info(str(result.reached_number))


    
def main(args=None):
    rclpy.init(args=args)
    node = SampleCustomActionClient()
    node.send_goal(-5,0.1)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()