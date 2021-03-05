import rclpy
from rclpy.node import Node

# from rclpy.time import Time
from rclpy.clock import Clock, ROSClock

from builtin_interfaces.msg import Time
import rosgraph_msgs.msg
from rclpy.parameter import Parameter
from rclpy.time_source import TimeSource

import time
# clock = ROSClock()


class TimeSubscriber(Node):

    def __init__(self):
        super().__init__('time_subscriber')
        self.subscription = self.create_subscription(
            rosgraph_msgs.msg.Clock,                                             
            '/clock',
            self.listener_callback,
            10
        )
        self.subscription

    def listener_callback(self, msg):
        time.sleep(1)
        clock = self.get_clock()

        msg2 = clock.now().seconds_nanoseconds()
    
        self.get_logger().info('I heard time as: "%s"' % str(msg2[0]) ) # CHANGE
        self.get_logger().info('I heard message as: "%s"' % str(msg) ) # CHANGE

        mssg=  str(msg)
        self.get_logger().info( mssg)



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = TimeSubscriber()



    # time_source = TimeSource(node=minimal_subscriber)
    # time_source.attach_clock(clock)
    minimal_subscriber._time_source.ros_time_is_active = True

    minimal_subscriber.set_parameters(
            [Parameter('use_sim_time', Parameter.Type.BOOL, True)])
    
    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()