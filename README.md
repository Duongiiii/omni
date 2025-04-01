file urdf được tách ra làm nhiều file xacro trong xacro/model

file cấu hình được tạo bởi các file xacro khác nhau được gọi trong my_robot.xacro

file xacro/gazebo: mô tả thiết kế của hệ thống và các transmission, plugin

file bản vẽ các thành phần của robot chứa bản vẽ dạng .stl trong foder mesh

foder launch chứa file launch để chạy gazebo và rviz

foder scripts: chứa file *.py để điều khiển robot và hiển thị encoder

foder rviz: chứa các file rviz , trong bài sử dụng myrobot.rviz

foder config: chứa các file *.yaml

pkg: My_robot

Chạy gazebo: gazebo_xacro.launch

Chạy rviz: display_xacro.launch

Chạy điều khiển tay máy: keyboard_arm_control.py

Chạy điều khiển xe: control.py

Chạy encoder: eoncoder_print.py

Video điều khiển: https://youtu.be/kyE8ZJcU9cQ
