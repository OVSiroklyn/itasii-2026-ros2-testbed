# ITASII-2026 — ROS 2 / SROS 2 testbed artifacts

Artifacts supporting "Cybersecurity of ROS 2-Based Robotic Systems: Experimental
Analysis of Attacks and SROS 2 Protection" (ITASII-2026).

## Versions
- ROS 2 Humble Hawksbill
- sros2 0.10.9
- ros-humble-fastrtps 2.6.12 (Fast-RTPS/Fast DDS)
- rmw_fastrtps_cpp 6.2.10
- rosidl_typesupport_fastrtps 2.2.4

## Simulator
Started with: ros2 launch turtlebot3_gazebo empty_world.launch.py

## SROS 2 policy
See keystore_policy/governance.xml and keystore_policy/permissions.xml
(signed .p7s artifacts and private keys are intentionally excluded).

## Attacks
See attack_commands.sh for the ARP-spoofing (machine C) and rogue-node
(machine D) commands used against machines A (robot) and B (operator).

## Analysis
analyze.py processes ros2 bag record output (/cmd_vel, /odom) to compute
the attacker-message share and trajectory deviation reported in Table 2.

## Performance overhead benchmark

10 runs per configuration (default vs SROS 2 Enforce), /cmd_vel at 10 Hz for
20 s each, CPU load of gzserver and the publishing process sampled with
pidstat every 1 s.

### Default configuration
Gazebo must already be running: ros2 launch turtlebot3_gazebo empty_world.launch.py

    cd data
    for i in 01 02 03 04 05 06 07 08 09 10; do
      GZ_PID=$(pgrep -f gzserver | head -1)
      ros2 bag record /cmd_vel -o overhead_default_$i < /dev/null > bag_log_default_$i.txt 2>&1 & BAG_PID=$!
      ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.2, y: 0.0, z: 0.0}}' < /dev/null > pub_log_default_$i.txt 2>&1 & PUB_PID=$!
      pidstat -p $GZ_PID 1 20 > cpu_gzserver_default_$i.txt &
      pidstat -p $PUB_PID 1 20 > cpu_teleop_default_$i.txt
      kill $BAG_PID $PUB_PID 2>/dev/null
      sleep 5
    done

### SROS 2, Enforce
Restart Gazebo in the same terminal with:

    export ROS_SECURITY_KEYSTORE=~/sros2_demo/keystore
    export ROS_SECURITY_ENABLE=true
    export ROS_SECURITY_STRATEGY=Enforce
    export ROS_SECURITY_ENCLAVE_OVERRIDE=/gazebo
    ros2 launch turtlebot3_gazebo empty_world.launch.py

Then, in the measurement terminal (same four exports, enclave override needed
for the ad-hoc bag-record/publisher nodes too):

    cd data
    for i in 01 02 03 04 05 06 07 08 09 10; do
      GZ_PID=$(pgrep -f gzserver | head -1)
      ros2 bag record /cmd_vel -o overhead_sros2_$i < /dev/null > bag_log_sros2_$i.txt 2>&1 & BAG_PID=$!
      ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.2, y: 0.0, z: 0.0}}' < /dev/null > pub_log_sros2_$i.txt 2>&1 & PUB_PID=$!
      pidstat -p $GZ_PID 1 20 > cpu_gzserver_sros2_$i.txt &
      pidstat -p $PUB_PID 1 20 > cpu_teleop_sros2_$i.txt
      kill $BAG_PID $PUB_PID 2>/dev/null
      sleep 5
    done

To disable SROS 2 again afterward:

    unset ROS_SECURITY_ENABLE ROS_SECURITY_STRATEGY ROS_SECURITY_KEYSTORE ROS_SECURITY_ENCLAVE_OVERRIDE
