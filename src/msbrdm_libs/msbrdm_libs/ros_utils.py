import numpy as np
from scipy.spatial.transform import Rotation
from geometry_msgs.msg import TransformStamped


def matrix_to_transform(T: np.ndarray, parent: str, child: str, stamp) -> TransformStamped:
    """Convert a 4x4 homogeneous transformation into a TransformStamped message"""
    T = np.asarray(T, dtype=float)
    q = Rotation.from_matrix(T[0:3, 0:3]).as_quat()   # [x, y, z, w]
    msg = TransformStamped()
    msg.header.stamp = stamp
    msg.header.frame_id = parent
    msg.child_frame_id = child
    msg.transform.translation.x, msg.transform.translation.y, msg.transform.translation.z = map(float, T[0:3, 3])
    msg.transform.rotation.x, msg.transform.rotation.y, msg.transform.rotation.z, msg.transform.rotation.w = map(float, q)
    return msg
