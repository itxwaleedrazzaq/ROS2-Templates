import rclpy
from rclpy.node import Node
from custom_actions.action import CustomAction
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
import time


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
        self.action_client.send_goal_async(goal,feedback_callback=self.goal_feedback_callback).add_done_callback(self.goal_response_callback)

    ####### This is to send a cancel request but this is just to checkyou modify according to need ############
        #self.cancel_timer = self.create_timer(0.5, self.cancel_timer_callback)
    
    def cancel_timer_callback(self):
        self.get_logger().info('Cancel Request')
        self.goal_handle.cancel_goal_async()
        self.cancel_timer.cancel()
    ####################################################################

    def goal_feedback_callback(self,feedback_msg):
        number = feedback_msg.feedback.current_number
        self.get_logger().info('Got Feedback in Client Side from Server : ' + str(number))
    
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
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal is Succeeded from Server')
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info('Goal is Aborted from Server')
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn('Goal is Cancelled from Server')
        self.get_logger().info(str(result.reached_number))


    
def main(args=None):
    rclpy.init(args=args)
    node = SampleCustomActionClient()
    node.send_goal(6,1.0)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()