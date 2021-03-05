
FROM ros:foxy

ARG ROS2_WS=/root/dev_ws

RUN mkdir -p ${ROS2_WS}/src

# clone overlay source
ARG ROS2_WS
WORKDIR $ROS2_WS/src

RUN . /opt/ros/foxy/setup.sh && \
ros2 pkg create --build-type ament_python simtime --dependencies rclpy


ARG ROS2_WS
WORKDIR $ROS2_WS/src/simtime




WORKDIR $ROS2_WS/src/simtime/
# ADD ./time_manager/package.xml .
# ADD ./time_manager/setup.py .

ADD ./simtime/ .

WORKDIR $ROS2_WS
RUN . /opt/ros/foxy/setup.sh && \
colcon build 

# ARG ROS2_WS
# WORKDIR $ROS2_WS/src/py_pubsub/

# ADD ./py_pubsub/package.xml .
# ADD ./py_pubsub/setup.py .

# ARG ROS2_WS
# WORKDIR $ROS2_WS/

# RUN . /opt/ros/foxy/setup.sh && \
#     apt-get update && rosdep install -i  -y \
#       --from-path src --rosdistro foxy && \
#       colcon build --packages-select py_pubsub
# RUN . install/setup.bash

# CMD [ros2, run, py_pubsub, talker]
  

# RUN apt-get update && apt-get install nano


# ros2 run time_manager time_publisher & ros2 run time_manager listener

# ros2 run simtime simtime_publisher & ros2 param set /simtime_publisher sim_interval_sweep_duration 600
# ros2 param set /simtime_publisher sim_horizon_start_time  '2021-03-26T00:00:00'