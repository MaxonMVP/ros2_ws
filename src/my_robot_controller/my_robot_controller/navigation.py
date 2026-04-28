#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
import tf_transformations
import math
from tf2_ros import Buffer, TransformListener

class TurtleNavigationNode(Node):
    def __init__(self):
        super().__init__("navigation")
        self.get_logger().info("Navigation Node started")

        self.goal_poses = [  # Define goal positions and orientations

            {'x': 2.93, 'y': 0.3, 'yaw': 80},
            {'x': 0.163, 'y': 5.122, 'yaw': 140},
            {'x': -2.93, 'y': 1.7, 'yaw': 60},

        ]

        self.current_goal_index = 0
        self.navigation_active = False

        # TF2 Setup
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Publishers
        self.initial_pose_publisher = self.create_publisher(
            PoseWithCovarianceStamped, "/initialpose", 10)
        self.goal_pose_publisher = self.create_publisher(
            PoseStamped, "/goal_pose", 10)

        # Subscriber (используем одометрию как таймер для проверки позиции)
        self.odom_listener = self.create_subscription(
            Odometry, "/odom", self.control_loop, 10)

        # Таймер для старта
        self.timer = self.create_timer(2.0, self.init_robot)

    def init_robot(self):
        self.timer.cancel()
        self.publish_initial_pose()
        self.get_logger().info("Initial pose sent. Starting in 3s...")
        self.start_timer = self.create_timer(3.0, self.start_nav)

    def start_nav(self):
        self.start_timer.cancel()
        self.navigation_active = True
        self.publish_goal()

    def publish_initial_pose(self):
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = 0.0001
        msg.pose.pose.position.y = 0.0001
        q = tf_transformations.quaternion_from_euler(0, 0, math.radians(11.422))
        msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w = q
        self.initial_pose_publisher.publish(msg)

    def control_loop(self, msg):
        if not self.navigation_active:
            return

        try:
            # Получаем позицию из TF (map -> base_link)
            t = self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
            cur_x = t.transform.translation.x
            cur_y = t.transform.translation.y
            
            goal = self.goal_poses[self.current_goal_index]
            dist = math.sqrt((cur_x - goal['x'])**2 + (cur_y - goal['y'])**2)

            # Логируем раз в секунду
            if self.get_clock().now().nanoseconds % 1000000000 < 100000000:
                self.get_logger().info(f"Goal {self.current_goal_index + 1} | Dist: {dist:.2f}m")

            # Если приехали
            if dist < 0.45:
                self.get_logger().info(f"Reached goal {self.current_goal_index + 1}")
                self.go_to_next_goal()

        except Exception as e:
            # Не спамим ошибками TF, пока он грузится
            pass

    def go_to_next_goal(self):
        if self.current_goal_index < len(self.goal_poses) - 1:
            self.current_goal_index += 1
            self.publish_goal()
        else:
            self.get_logger().info("ALL GOALS COMPLETED!")
            self.navigation_active = False

    def publish_goal(self):
        goal = self.goal_poses[self.current_goal_index]
        msg = PoseStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = goal['x']
        msg.pose.position.y = goal['y']
        q = tf_transformations.quaternion_from_euler(0, 0, math.radians(goal['yaw']))
        msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w = q
        
        self.goal_pose_publisher.publish(msg)
        self.get_logger().info(f"Heading to goal {self.current_goal_index + 1}")

def main(args=None):
    rclpy.init(args=args)
    node = TurtleNavigationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
