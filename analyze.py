import glob
import rosbag2_py
from rclpy.serialization import deserialize_message
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def read_bag(path):
    reader = rosbag2_py.SequentialReader()
    reader.open(
        rosbag2_py.StorageOptions(uri=path, storage_id='sqlite3'),
        rosbag2_py.ConverterOptions('', '')
    )
    cmd_vel, odom = [], []
    while reader.has_next():
        topic, data, t = reader.read_next()
        if topic == '/cmd_vel':
            cmd_vel.append((t, deserialize_message(data, Twist)))
        elif topic == '/odom':
            odom.append((t, deserialize_message(data, Odometry)))
    return cmd_vel, odom

def is_forged(m):
    return abs(m.linear.x - 0.5) < 1e-6 and abs(m.angular.z - 0.5) < 1e-6

def final_xy(odom):
    p = odom[-1][1].pose.pose.position
    return p.x, p.y

baseline_cmd, baseline_odom = read_bag('baseline_run')
bx, by = final_xy(baseline_odom)

shares, deviations = [], []
for path in sorted(glob.glob('rogue_run_*')):
    cmd_vel, odom = read_bag(path)
    n_total = len(cmd_vel)
    n_forged = sum(1 for _, m in cmd_vel if is_forged(m))
    share = n_forged / n_total if n_total else 0.0
    rx, ry = final_xy(odom)
    dev = ((rx - bx) ** 2 + (ry - by) ** 2) ** 0.5
    shares.append(share)
    deviations.append(dev)
    print(f'{path}: n_cmd_vel={n_total}, attacker_share={share:.1%}, deviation={dev:.2f} m')

n = len(shares)
mean_share = sum(shares) / n
std_share = (sum((s - mean_share) ** 2 for s in shares) / n) ** 0.5
mean_dev = sum(deviations) / n
std_dev = (sum((d - mean_dev) ** 2 for d in deviations) / n) ** 0.5

print()
print(f'SUMMARY (n={n} runs):')
print(f'  attacker message share: {mean_share:.1%} ± {std_share:.1%}')
print(f'  position deviation from baseline: {mean_dev:.2f} ± {std_dev:.2f} m')
