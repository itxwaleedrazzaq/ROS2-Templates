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
        self.goal_queue = []  #policy3:queue maker
        self.goal_handle_: ServerGoalHandle = None #policy maker
        self.goal_lock = threading.Lock()
        self.count_until_server  = ActionServer(self,
                                        CustomAction,
                                        'count_until',
                                        goal_callback= self.goal_callback,
                                        handle_accepted_callback=self.handle_accepted_callback,      #for policy3
                                        cancel_callback=self.cancel_callback,
                                        execute_callback=self.execute_callback,
                                        callback_group=ReentrantCallbackGroup())
        self.get_logger().info('Action server has started')
    
    def goal_callback(self,goal_request:CustomAction.Goal):
        self.get_logger().info('Receiving Goal - Server side')
        # policy1: refuse new goal if current still active
        # with self.goal_lock:
        #     if self.goal_handle_ is not None and self.goal_handle_.is_active:
        #         self.get_logger().error('Previous Goal is already exectuing: Rejecting new goal')
        #         return GoalResponse.REJECT

        #valideate request
        if goal_request.target_number <= 0:
            self.get_logger().info('Rejecting Goal - Server side')
            return GoalResponse.REJECT
        else:
            self.get_logger().info('Goal is validated and accepted - Server side')
            
            #policy2: Preempt new goal
            # if self.goal_handle_ is not None and self.goal_handle_.is_active:
            #     self.get_logger().info('Abort Current goal and Accept new goal')
            #     self.goal_handle_.abort()
            return GoalResponse.ACCEPT
    
    #policy3: Queue goal #########################3
    def handle_accepted_callback(self,goal_handle:ServerGoalHandle):
        if self.goal_handle_ is not None:
            self.goal_queue.append(goal_handle)
        else:
            goal_handle.execute()
    
    def process_next_goal_in_queue(self):
        with self.goal_lock:
            if len(self.goal_queue)>0:
                self.goal_queue.pop(0).execute()
            else:
                self.goal_handle_ = None
    ####################################################
        
    def cancel_callback(self,goal_handle:ServerGoalHandle):
        self.get_logger().warn('Received Cancel Request from Server')
        return CancelResponse.ACCEPT  #or Reject

    def execute_callback(self, goal_handle: ServerGoalHandle):
        with self.goal_lock:
            self.goal_handle_ = goal_handle  # Set current goal handle

        # Get request from the goal
        self.get_logger().info('Receiving the goal')
        target = goal_handle.request.target_number
        period = goal_handle.request.period

        # Execute the action while sending feedback
        self.get_logger().info('Executing the action and sending feedback to client')
        feedback = CustomAction.Feedback()
        result = CustomAction.Result()
        counter = 0
        for i in range(target):
            if not goal_handle.is_active:
                self.process_next_goal_in_queue()  # Process next goal in queue if any
                result.reached_number = counter
                return result
            if goal_handle.is_cancel_requested:
                self.get_logger().warn('Received Cancel Request from Client - Canceling Goal')
                goal_handle.canceled()
                result.reached_number = counter
                return result
            counter += 1
            feedback.current_number = counter
            goal_handle.publish_feedback(feedback)
            time.sleep(period)

        # Once action is done, set the goal handle to final state
        goal_handle.succeed()

        # Process next goal in queue if any
        self.process_next_goal_in_queue()

        # Send the result
        result.reached_number = counter
        return result




        
def main(args=None):
    rclpy.init(args=args)
    node = SampleCustomActionServer()
    rclpy.spin(node,MultiThreadedExecutor())
    rclpy.shutdown()


if __name__ == '__main__':
    main()