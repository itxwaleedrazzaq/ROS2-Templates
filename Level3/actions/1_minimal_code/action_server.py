import rclpy
from rclpy.node import Node
from custom_actions.action import CustomAction
from rclpy.action import ActionServer,GoalResponse
from rclpy.action.server import ServerGoalHandle, CancelResponse
import time
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup


class SampleCustomActionServer(Node):
    def __init__(self):
        super().__init__('custom_action_server') 
        self.count_until_server  = ActionServer(self,
                                        CustomAction,
                                        'count_until',
                                        execute_callback=self.execute_callback,)
        self.get_logger().info('Action server has started')
    

    def execute_callback(self, goal_handle:ServerGoalHandle):
        #get request from the goal
        target = goal_handle.request.target_number
        period = goal_handle.request.period

        # Execute the action while send feedback
        self.get_logger().info('Executing the goal')
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
            self.get_logger().info(str(counter))
            time.sleep(period)

        #once action is done set the goal_handlr to final state
        goal_handle.succeed()

        # send the result
        result.reached_number = counter
        return result

        
def main(args=None):
    rclpy.init(args=args)
    node = SampleCustomActionServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()