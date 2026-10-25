#!/usr/bin/env python
import numpy as np
from tutorial_1.rotation import Rzyx, invHT, R2EulerA


def main():

    ################################################################################
    # Figure 3 dimensions [m]
    L1 = 0.300
    L2 = 0.340
    L3 = 0.583
    L4 = 0.080
    L5 = 0.080
    L6 = 0.115
    L7 = 0.082
    L8 = 0.108
    L9 = 0.123
    theta1 = np.pi/4
    theta2 = np.pi/6

    slider = 0.110    # length of the red slider blocks (q2, q3)
    r_tube = 0.008    # tube radius, L6 is measured to the outer edge of the tube
    s_q4 = 0.0423     # q4 housing offset along the tilted q4 axis

    ################################################################################
    # Absolute transforms Hi_0 of each joint frame (z = joint axis)

    # Base: top of the column, rotated 180 deg so the arm points along -x_w
    Hb_0 = np.eye(4)
    Hb_0[0:3, 3] = [L1, L2, L3]
    Hb_0[0:3, 0:3] = Rzyx(np.pi, 0, 0)

    # q1: on the q1 shaft, z along -y_w
    H1_0 = np.eye(4)
    H1_0[0:3, 3] = [L1, L2 - L4, L3]
    H1_0[0:3, 0:3] = Rzyx(np.pi, 0, -np.pi/2)

    # q2: start of the horizontal slider, L5 from q1, z along -x_w (pitch = 90 deg)
    H2_0 = np.eye(4)
    H2_0[0:3, 3] = H1_0[0:3, 3] + [-L5, 0, 0]
    H2_0[0:3, 0:3] = Rzyx(0, np.pi/2, np.pi)

    # q3: start of the vertical slider, L7 below the arm, z along -z_w
    H3_0 = np.eye(4)
    H3_0[0:3, 3] = H2_0[0:3, 3] + [-(slider + L6 - r_tube), 0, -L7]
    H3_0[0:3, 0:3] = Rzyx(-np.pi/2, 0, np.pi)

    # q4: L8 below the slider to the bend, L9 along the tube (theta2),
    # then s_q4 along the q4 axis tilted by theta1
    H4_0 = np.eye(4)
    H4_0[0:3, 3] = (H3_0[0:3, 3] + [0, 0, -(slider + L8)]
                    + [L9*np.sin(theta2), -L9*np.cos(theta2), 0]
                    + s_q4*np.array([np.cos(theta1), 0, np.sin(theta1)]))
    H4_0[0:3, 0:3] = Rzyx(np.pi/2, 0, theta1)

    HT_list = []
    HT_list.append(np.eye(4))
    HT_list.append(Hb_0)
    HT_list.append(H1_0)
    HT_list.append(H2_0)
    HT_list.append(H3_0)
    HT_list.append(H4_0)

    names = ['base_link_joint', 'q1_joint', 'q2_joint', 'q3_joint', 'q4_joint']

    ################################################################################
    # Relative transforms Hi_(i-1) = inv(H(i-1)_0) @ Hi_0 -> URDF origin
    # R2EulerA returns (phi, theta, psi) = (yaw z, pitch y, roll x)
    # URDF rpy is "roll pitch yaw", so the order is reversed

    for i, name in enumerate(names):
        Hrel = invHT(HT_list[i]) @ HT_list[i + 1]
        t = Hrel[0:3, 3]
        phi, theta, psi = R2EulerA(Hrel[0:3, 0:3])
        print(f'{name:16s} xyz="{t[0]:.4f} {t[1]:.4f} {t[2]:.4f}"'
              f'  rpy="{psi:.4f} {theta:.4f} {phi:.4f}"')


if __name__ == '__main__':
    main()
