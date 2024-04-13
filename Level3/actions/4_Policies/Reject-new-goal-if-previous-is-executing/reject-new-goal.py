#This code will reject the new goal if previous goal is already exectuing
import rclpy
from rclpy.node import Node
from custom_actions.action import CustomAction
from rclpy.action import ActionServer,GoalResponse
from rclpy.action.server import ServerGoalHandle, CancelResponse
import time
import threading
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup


class SampleCustomActionServer(Node):
    def __init__(self):
        super().__init__('custom_action_server') 
        self.goal_handle_: ServerGoalHandle = None #policy maker
        self.goal_lock = threading.Lock()
        self.count_until_server  = ActionServer(self,
                                        CustomAction,
                                        'count_until',
                                        goal_callback= self.goal_callback,
                                        cancel_callback=self.cancel_callback,
                                        execute_callback=self.execute_callback,
                                        callback_group=ReentrantCallbackGroup())
        self.get_logger().info('Action server has started')
    
    def goal_callback(self,goal_request:CustomAction.Goal):
        self.get_logger().info('Receiving Goal - Server side')
        # policy: refuse new goal if current still active
        with self.goal_lock:
            if self.goal_handle_ is not None and self.goal_handle_.is_active:
                self.get_logger().error('Previous Goal is already exectuing: Rejecting new goal')
                return GoalResponse.REJECT

        #valideate request
        if goal_request.target_number <= 0:
            self.get_logger().info('Rejecting Goal - Server side')
            return GoalResponse.REJECT
        else:
            self.get_logger().info('Goal is validated and accepted - Server side')
            return GoalResponse.ACCEPT
        
    def cancel_callback(self,goal_handle:ServerGoalHandle):
        self.get_logger().warn('Received Cancel Request from Server')
        return CancelResponse.ACCEPT  #or Reject

    def execute_callback(self, goal_handle:ServerGoalHandle):
        with self.goal_lock:
            self.goal_handle_ = goal_handle  #this is done so that we can use it as attribute for full class
        #get request from the goal
        self.get_logger().info('Receiving the goal')
        target = goal_handle.request.target_number
        period = goal_handle.request.period

        # Execute the action while send feedback
        self.get_logger().info('Exceuting the action and sending feedback to client')
        feedback = CustomAction.Feedback()  #making feedback object
        result = CustomAction.Result()  #result in actions
        counter = 0
        for i in range(target):
            #check if cancel request is done by client
            if goal_handle.is_cancel_requested:
                self.get_logger().warn('Received Cancel Request from Client - Canceling Goal')
                goal_handle.canceled()
                result.reached_number = counter
                return result
            counter += 1
            feedback.current_number = counter #adding value to feedback variable in custim actions
            goal_handle.publish_feedback(feedback)  #sending feedback to client
            #self.get_logger().info(str(counter))
            time.sleep(period)

        #once action is done set the goal_handlr to final state
        goal_handle.succeed()

        # send the result
        result.reached_number = counter
        return result



        
def main(args=None):
    rclpy.init(args=args)
    node = SampleCustomActionServer()
    rclpy.spin(node,MultiThreadedExecutor())
    rclpy.shutdown()


if __name__ == '__main__':
    main()