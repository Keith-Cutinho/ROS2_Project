import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios


def get_key():
   
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)        
        
        if key == '\x1b':               
            key += sys.stdin.read(1)    
            key += sys.stdin.read(1)   
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key




KEY_BINDINGS = {
    '\x1b[A': ( 2.0,  0.0),   
    '\x1b[B': (-2.0,  0.0),   
    '\x1b[D': ( 0.0,  2.0),   
    '\x1b[C': ( 0.0, -2.0),   
}




class TeleopTurtle(Node):

    def __init__(self):
        super().__init__('teleop_turtle')

       
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.get_logger().info(
            '\nNode is working \n'
            ' Ctrl+C to quit'
        )
        
        
  

    def run(self):
        
        while rclpy.ok():
            key = get_key()

            if key == '\x03':           
                break

            if key in KEY_BINDINGS:
                linear, angular = KEY_BINDINGS[key]
                msg = Twist()
                msg.linear.x  = linear
                msg.angular.z = angular
                self.publisher_.publish(msg)
                self.get_logger().info(
                    f'Published → linear: {linear}, angular: {angular}'
                   
                )
            else:
                self.get_logger().warn('use arrow keys only')


def main(args=None):
    rclpy.init(args=args)
    node = TeleopTurtle()
    try:
        node.run()
    finally:
        
        stop = Twist()
        node.publisher_.publish(stop)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
