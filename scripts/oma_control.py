#!/usr/bin/env python3

import rospy
import threading
from std_msgs.msg import Float64
import sys
import tty
import termios

class OmniArmControl:
    def __init__(self):
        rospy.init_node('omni_arm_control', anonymous=True)

        # Publisher cho robot di chuyển
        self.pub_left = rospy.Publisher('/left_wheel_velocity_controller/command', Float64, queue_size=10)
        self.pub_right = rospy.Publisher('/right_wheel_velocity_controller/command', Float64, queue_size=10)
        self.pub_font = rospy.Publisher('/font_wheel_velocity_controller/command', Float64, queue_size=10)

        # Publisher cho tay máy
        self.arm1_pub = rospy.Publisher('/arm_1_joint_controller/command', Float64, queue_size=10)
        self.arm2_pub = rospy.Publisher('/arm_2_joint_controller/command', Float64, queue_size=10)
        
        self.max_speed = 10.0
        self.left_speed = 0.0
        self.right_speed = 0.0
        self.font_speed = 0.0

        # Biến lưu vị trí tay máy
        self.pos1 = 0.0
        self.pos2 = 0.0

        # Khởi chạy luồng nhập cho tay máy
        self.arm_thread = threading.Thread(target=self.move_arm)
        self.arm_thread.daemon = True
        self.arm_thread.start()

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

    def move_arm(self):
        rospy.sleep(1)  # Đợi ROS khởi động
        while not rospy.is_shutdown():
            try:
                self.pos1 = float(input("Nhập vị trí cho arm1 (-1.5 đến 1.5 rad): "))
                self.pos2 = float(input("Nhập vị trí cho arm2 (-1.5 đến 1.5 rad): "))
                self.arm1_pub.publish(self.pos1)
                self.arm2_pub.publish(self.pos2)
            except ValueError:
                rospy.logwarn("Vui lòng nhập số hợp lệ.")

    def run(self):
        rospy.loginfo("Điều khiển robot omni 3 bánh và tay máy:")
        rospy.loginfo("w: Tiến, s: Lùi, a: Trái, d: Phải, q: Xoay trái, e: Xoay phải")
        rospy.loginfo("x: Dừng và thoát")

        while not rospy.is_shutdown():
            key = self.get_key()
            self.left_speed, self.right_speed, self.font_speed = 0, 0, 0
            
            if key == 'w':
                self.left_speed = self.max_speed
                self.right_speed = -self.max_speed
            elif key == 's':
                self.left_speed = -self.max_speed
                self.right_speed = self.max_speed
            elif key == 'a':
                self.left_speed = self.max_speed
                self.right_speed = self.max_speed
                self.font_speed = -self.max_speed
            elif key == 'd':
                self.left_speed = -self.max_speed
                self.right_speed = -self.max_speed
                self.font_speed = self.max_speed
            elif key == 'q':
                self.left_speed = -self.max_speed
                self.right_speed = self.max_speed
                self.font_speed = self.max_speed
            elif key == 'e':
                self.left_speed = self.max_speed
                self.right_speed = -self.max_speed
                self.font_speed = -self.max_speed
            elif key in ['z', 'x']:
                self.left_speed = self.right_speed = self.font_speed = 0.0
                self.pub_left.publish(self.left_speed)
                self.pub_right.publish(self.right_speed)
                self.pub_font.publish(self.font_speed)
                rospy.loginfo("Dừng robot")
                if key == 'x':
                    rospy.loginfo("Thoát chương trình")
                    break

            self.pub_left.publish(self.left_speed)
            self.pub_right.publish(self.right_speed)
            self.pub_font.publish(self.font_speed)
            rospy.loginfo(f"Left: {self.left_speed:.2f}, Right: {self.right_speed:.2f}, font: {self.font_speed:.2f}")
            rospy.sleep(0.1)

if __name__ == '__main__':
    try:
        controller = OmniArmControl()
        controller.run()
    except rospy.ROSInterruptException:
        pass
