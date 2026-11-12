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
