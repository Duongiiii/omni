#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

def move_arm():
    rospy.init_node('arm_controller', anonymous=True)
    
    arm1_pub = rospy.Publisher('arm_1_joint_controller/command', Float64, queue_size=10)
    arm2_pub = rospy.Publisher('arm_2_joint_controller/command', Float64, queue_size=10)
    
    rospy.sleep(1)  # Đợi ROS khởi động
    
    rate = rospy.Rate(10)  # 10Hz
    while not rospy.is_shutdown():
        pos1 = input("Nhập vị trí cho arm1 (-1.5 đến 1.5 rad, hoặc nhập 'p' để thoát): ")
        if pos1.lower() == 'p':
            print("Dừng điều khiển.")
            break
        
        pos2 = input("Nhập vị trí cho arm2 (-1.5 đến 1.5 rad, hoặc nhập 'p' để thoát): ")
        if pos2.lower() == 'p':
            print("Dừng điều khiển.")
            break
        
        try:
            pos1 = float(pos1)
            pos2 = float(pos2)
            
            if -1.5 <= pos1 <= 1.5 and -1.5 <= pos2 <= 1.5:
                arm1_pub.publish(Float64(pos1))
                arm2_pub.publish(Float64(pos2))
            else:
                print("Giá trị ngoài phạm vi! Vui lòng nhập lại.")
        except ValueError:
            print("Giá trị không hợp lệ! Vui lòng nhập số hoặc 'p' để thoát.")
        
        rate.sleep()

if __name__ == '__main__':
    try:
        move_arm()
    except rospy.ROSInterruptException:
        pass