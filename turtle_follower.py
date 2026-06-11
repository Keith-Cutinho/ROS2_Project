import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


class TurtleFollower(Node):

    def __init__(self):
        super().__init__('turtle_follower')

        self.leader_pose = None
        self.follower_pose = None

         # for the leader turtle subcriber 
        self.create_subscription(Pose, '/turtle1/pose', self.leader_callback, 10)
        
        #for the follower turtle subscription 
        self.create_subscription(Pose, '/turtle2/pose', self.follower_callback, 10)

        # Publisher will send  velocity commands to turtle2
        self.pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)

        # Timer - runs control loop 10 times per second
        self.create_timer(0.1, self.control_loop)

        print('Follower node has started.')

    def leader_callback(self, msg):
        self.leader_pose = msg

    def follower_callback(self, msg):
        self.follower_pose = msg

    def control_loop(self):

        if self.leader_pose is None or self.follower_pose is None:
            return

        lx = self.leader_pose.x
        ly = self.leader_pose.y
        fx = self.follower_pose.x
        fy = self.follower_pose.y
        ftheta = self.follower_pose.theta

        # Calculate distance between turtle2 and turtle1
        distance = math.sqrt((lx - fx)**2 + (ly - fy)**2)

        # If close enough stop moving
        if distance < 1.0:
            self.pub.publish(Twist())
            return

        # Calculate angle from turtle2 toward turtle1
        angle_to_leader = math.atan2(ly - fy, lx - fx)

        # How much turtle2 needs to rotate
        angle_error = angle_to_leader - ftheta

        # Normalize to [-pi, +pi] so turtle turns the short way
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        msg = Twist()

        msg.linear.x = 2.0

        msg.angular.z = 4.0 * (angle_error / abs(angle_error)) if angle_error != 0 else 0.0

        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
