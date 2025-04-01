#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
import math

class WheelEncoderReader:
    def __init__(self):
        # Khởi tạo node ROS
        rospy.init_node('wheel_encoder_reader', anonymous=True)

        # Thông số bánh xe (giả định)
        self.wheel_radius = 0.015423  # Bán kính bánh xe (m), từ URDF: diameter=0.030846
        self.pulses_per_revolution = 360  # Số xung trên mỗi vòng quay (giả định, thay đổi nếu có encoder thực tế)

        # Biến lưu trữ dữ liệu
        self.left_pos = 0.0  # Vị trí góc (rad) của bánh trái
        self.right_pos = 0.0
        self.font_pos = 0.0
        self.left_vel = 0.0  # Vận tốc góc (rad/s) của bánh trái
        self.right_vel = 0.0
        self.font_vel = 0.0

        # Subscriber cho topic /joint_states
        rospy.Subscriber('/joint_states', JointState, self.joint_state_callback)

    def joint_state_callback(self, msg):
        # Lấy dữ liệu từ topic /joint_states
        try:
            # Tìm chỉ số của các khớp bánh xe trong message
            left_idx = msg.name.index('left_wheel_joint')
            right_idx = msg.name.index('right_wheel_joint')
            font_idx = msg.name.index('font_wheel_joint')

            # Cập nhật vị trí và vận tốc
            self.left_pos = msg.position[left_idx]
            self.right_pos = msg.position[right_idx]
            self.font_pos = msg.position[font_idx]
            self.left_vel = msg.velocity[left_idx]
            self.right_vel = msg.velocity[right_idx]
            self.font_vel = msg.velocity[font_idx]

        except ValueError as e:
            rospy.logwarn(f"Không tìm thấy một số khớp trong /joint_states: {e}")

    def calculate_pulses(self, position):
        # Tính số xung từ vị trí góc (rad)
        revolutions = position / (2 * math.pi)  # Số vòng quay
        pulses = revolutions * self.pulses_per_revolution  # Số xung
        return int(pulses)  # Làm tròn về số nguyên

    def run(self):
        rate = rospy.Rate(0.2)  # 10 Hz
        rospy.loginfo("Đang đọc dữ liệu encoder từ các bánh xe...")

        while not rospy.is_shutdown():
            # Tính số xung cho từng bánh
            left_pulses = self.calculate_pulses(self.left_pos)
            right_pulses = self.calculate_pulses(self.right_pos)
            font_pulses = self.calculate_pulses(self.font_pos)

            # Tính quãng đường di chuyển (m) từ vị trí góc
            left_distance = self.left_pos * self.wheel_radius
            right_distance = self.right_pos * self.wheel_radius
            font_distance = self.font_pos * self.wheel_radius

            # Hiển thị thông tin
            rospy.loginfo("=== Dữ liệu Encoder ===")
            rospy.loginfo(f"Left Wheel: Pulses={left_pulses}, Pos={self.left_pos:.3f} rad, Vel={self.left_vel:.3f} rad/s, Distance={left_distance:.3f} m")
            rospy.loginfo(f"Right Wheel: Pulses={right_pulses}, Pos={self.right_pos:.3f} rad, Vel={self.right_vel:.3f} rad/s, Distance={right_distance:.3f} m")
            rospy.loginfo(f"font Wheel: Pulses={font_pulses}, Pos={self.font_pos:.3f} rad, Vel={self.font_vel:.3f} rad/s, Distance={font_distance:.3f} m")
            rate.sleep()
if __name__ == '__main__':
    try:
        encoder_reader = WheelEncoderReader()
        encoder_reader.run()
    except rospy.ROSInterruptException:
        pass