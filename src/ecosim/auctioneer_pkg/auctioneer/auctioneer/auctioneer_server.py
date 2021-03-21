
import rclpy
from rclpy.node import Node

from rclpy.clock import Clock, ROSClock
from rclpy.time import Time
from rclpy.time_source import TimeSource
from builtin_interfaces.msg import Time
from rclpy.parameter import Parameter

import rosgraph_msgs.msg
from rclpy.exceptions import ParameterNotDeclaredException
from rcl_interfaces.msg import ParameterType

# from std_msgs.msg import String
from datetime import datetime

class SimTimePublisher(Node):

    def __init__(self):
        super().__init__('simtime_publisher')
        self.publisher_ = self.create_publisher(rosgraph_msgs.msg.Clock, '/clock', 10)

        self.declare_parameter('sim_horizon_start_time', '2021-02-26T00:00:00')
        self.declare_parameter('sim_horizon_end_time', '2021-02-27T00:00:00')
        self.declare_parameter('sim_interval_sweep_duration', 1800) #seconds
        self.declare_parameter('sim_interval_sweep_pace', 2) # seconds

        self.sim_horizon_start_time = self.get_parameter('sim_horizon_start_time').get_parameter_value().string_value
        self.sim_horizon_end_time = self.get_parameter('sim_horizon_end_time').get_parameter_value().string_value
        self.sim_interval_sweep_duration = self.get_parameter('sim_interval_sweep_duration').get_parameter_value().integer_value
        self.sim_interval_sweep_pace = self.get_parameter('sim_interval_sweep_pace').get_parameter_value().integer_value

        
        timer_period = self.sim_interval_sweep_pace  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):

        # self.sim_horizon_start_time = self.get_parameter('sim_horizon_start_time').get_parameter_value().string_value
        self.sim_horizon_end_time = self.get_parameter('sim_horizon_end_time').get_parameter_value().string_value
        self.sim_interval_sweep_duration = self.get_parameter('sim_interval_sweep_duration').get_parameter_value().integer_value
        self.sim_interval_sweep_pace = self.get_parameter('sim_interval_sweep_pace').get_parameter_value().integer_value

        horizon_start_time = datetime.fromisoformat(self.sim_horizon_start_time)

        epoch = datetime.utcfromtimestamp(0)

        # message = Clock().now().to_msg()

        time_msg = rosgraph_msgs.msg.Clock()
        time_msg.clock.sec = self.i
        time_msg.clock.sec = int((horizon_start_time - epoch).total_seconds() )+ self.i
        # time_msg.clock.sec = self.i

        # print((horizon_start_time - epoch).total_seconds()) 




        self.publisher_.publish(time_msg)
        self.get_logger().info('Publishing Time for : "%s"' % time_msg)
        # self.get_logger().info('horizon start is  : "%s"' % self.sim_horizon_start_time)
        # self.get_logger().info('interval duration is  : "%s"' % self.sim_interval_sweep_duration)


        self.i +=  self.sim_interval_sweep_duration
            # cycle_count += 10



def main(args=None):
    rclpy.init(args=args)

    publisher = SimTimePublisher()

    rclpy.spin(publisher)


    # time_source = TimeSource(node=publisher)
    #     # ROSClock is a specialization of Clock with ROS time methods.
    # time_source.attach_clock(ROSClock())

    publisher.set_parameters(
            [Parameter('use_sim_time', Parameter.Type.BOOL, True)])
    



    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
