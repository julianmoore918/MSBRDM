#!/usr/bin/env python
import numpy as np
import tutorial_1.plot as plot
from tutorial_1.rotation import R2EulerA,RotX, RotY, RotZ, Rzyx,invHT
import matplotlib.pyplot as plt


def main():

    ################################################################################
    # Question 1: Manually computed Homogeneous Transformations
    # TODO:
    # By simple inspection obtain manually the absolute homogeneous transformations
    # Ti_0 for each corner of the cage with respect to the coordinate frame O_0

    T1_0 = np.eye(4)
    T1_0[0:3, 3] = [-0.5, -0.3, -0.4]
    T1_0[0:3, 0:3] = Rzyx(0, 0, 0)

    T2_0 = np.eye(4)
    T2_0[0:3, 3] = [0.5, -0.3, -0.4]
    T2_0[0:3, 0:3] = Rzyx(np.pi/2, 0, 0)

    T3_0 = np.eye(4)
    T3_0[0:3, 3] = [0.5, 0.3, -0.4]
    T3_0[0:3, 0:3] = Rzyx(-np.pi/2, 0, np.pi)

    T4_0 = np.eye(4)
    T4_0[0:3, 3] = [-0.5, 0.3, -0.4]
    T4_0[0:3, 0:3] = Rzyx(-np.pi/2, 0, 0)

    T5_0 = np.eye(4)
    T5_0[0:3, 3] = [-0.5, -0.3, 0.4]
    T5_0[0:3, 0:3] = Rzyx(0, 0, 0)

    T6_0 = np.eye(4)
    T6_0[0:3, 3] = [0.5, -0.3, 0.4]
    T6_0[0:3, 0:3] = Rzyx(0, -np.pi, 0)

    T7_0 = np.eye(4)
    T7_0[0:3, 3] = [0.5, 0.3, 0.4]
    T7_0[0:3, 0:3] = Rzyx(np.pi/2, -np.pi, 0)   

    T8_0 = np.eye(4)
    T8_0[0:3, 3] = [-0.5, 0.3, 0.4]
    T8_0[0:3, 0:3] = Rzyx(np.pi, -np.pi, 0) 

    HT_list_1 = []
    HT_list_1.append(np.eye(4))
    HT_list_1.append(T1_0)
    HT_list_1.append(T2_0)
    HT_list_1.append(T3_0)
    HT_list_1.append(T4_0)
    HT_list_1.append(T5_0)
    HT_list_1.append(T6_0)
    HT_list_1.append(T7_0)
    HT_list_1.append(T8_0)


    ################################################################################
    # Question 2: Left handed frames
    # TODO:
    # The rotation matrix of some frames in the previous figure can not be
    # obtained using a sequence of basic rotations. Please explain why
    # (elaborate your answer using for example the definition of SE(3)),
    # mark the origin of these frames with a magenta circle and
    # propose the proper coordinate frames to fix this problem.

    #H_5 cant just be rotated since it is a left handed frame, so we need to rotate it and then mirror it to make it right handed.

    # Plot the cage
    fig_1 = plt.figure()
    ax = fig_1.add_subplot(111, projection='3d')
    ax.set_title("Cage with Left handed O3 and O7 (in Magenta)")

    plot.cage(ax, HT_list_1)
    for T in (T3_0, T5_0):
        ax.plot(*T[0:3, 3], 'mo', markersize=10)

    # Explanation:

    #Every elementary rotation R_x, R_y, R_z has det = +1. Since det(AB) = det(A)*det(B), any composition of rotations also has det = +1. This is the closure property of SO(3) = {R | RRᵀ = I, det R = +1}.
    #The frames O3 and O5 have det(R) = −1. They are left-handed (z ≠ x × y), so R ∉ SO(3). It is an improper rotation, which includes a reflection. Therefore H = [[R, t], [0, 1]] ∉ SE(3), which requires R ∈ SO(3). No sequence of basic rotations can produce these frames; a reflection such as diag(1, 1, −1) is needed.

    ################################################################################
    # Question 3: Right Hand Frames
    # TODO:
    # Replace the coordinate frames found in the above question with the
    # suitable coordinate frames, respecting the figure convention;
    # then compute the associated absolute homogeneous transformations Hi_0

    H1_0 = T1_0.copy()

    H2_0 = T2_0.copy() 

    F = np.diag([1, 1, -1])
    #to flip z-axis
    T3_0 = np.eye(4)
    T3_0[0:3, 3] = [0.5, 0.3, -0.4]
    T3_0[0:3, 0:3] = Rzyx(-np.pi/2, 0, np.pi) @ F
    H3_0 = T3_0.copy()

    H4_0 = T4_0.copy()

    T5_0 = np.eye(4)
    T5_0[0:3, 3] = [-0.5, -0.3, 0.4]
    T5_0[0:3, 0:3] = Rzyx(0, 0, 0) @ F
    H5_0 = T5_0.copy()

    H6_0 = T6_0.copy()
    H7_0 = T7_0.copy()
    H8_0 = T8_0.copy()

    HT_list_2 = []
    HT_list_2.append(np.eye(4))
    HT_list_2.append(H1_0)
    HT_list_2.append(H2_0)
    HT_list_2.append(H3_0)
    HT_list_2.append(H4_0)
    HT_list_2.append(H5_0)
    HT_list_2.append(H6_0)
    HT_list_2.append(H7_0)
    HT_list_2.append(H8_0)

    fig_2 = plt.figure()
    ax = fig_2.add_subplot(111, projection='3d')
    ax.set_title("Correct Cage")

    plot.cage(ax, HT_list_2)

    ################################################################################
    # Question 4: Rotation matrices and translation vectors
    # TODO:
    # Extract the rotation matrices and translation vectors from each HT:

    # Ri_0 = H[0:3, 0:3] (rotation block), ti_0 = H[0:3, 3] (translation)
    # R_list[i] / t_list[i] belong to frame O_i (index 0 = base frame O_0)
    R_list = []
    t_list = []
    for i, H in enumerate(HT_list_2):
        Ri_0 = H[0:3, 0:3]
        ti_0 = H[0:3, 3]
        R_list.append(Ri_0)
        t_list.append(ti_0)
        print(f"R{i}_0 =\n{np.round(Ri_0, 3)}\nt{i}_0 = {np.round(ti_0, 3)}\n")

    ################################################################################
    # Question 5: Simple Euler angles without considering singularities
    # TODO:
    # Represent each rotation matrix as a set of Euler angles (roll-pitch-yaw)

    # phi = roll (z), theta = pitch (y), psi = yaw (x); R = Rz(phi) Ry(theta) Rx(psi)
    euler_list = []
    for i, Ri_0 in enumerate(R_list):
        phi_i, theta_i, psi_i = R2EulerA(Ri_0)
        euler_list.append((phi_i, theta_i, psi_i))
        print(f"O{i}: phi = {np.degrees(phi_i):7.1f} deg, "
              f"theta = {np.degrees(theta_i):7.1f} deg, "
              f"psi = {np.degrees(psi_i):7.1f} deg")


    ################################################################################
    # Question 6: Relative Homogeneous Transformations (manually Generated)
    # TODO:
    # Compute manually the the relative transformations between the corners of
    # the cage

    H1_0 = H1_0                     

    H2_1 = np.eye(4)                
    H2_1[0:3, 3] = [1, 0, 0]
    H2_1[0:3, 0:3] = Rzyx(np.pi/2, 0, 0)

    H3_2 = np.eye(4)                 
    H3_2[0:3, 3] = [0.6, 0, 0]
    H3_2[0:3, 0:3] = Rzyx(np.pi/2, 0, 0)

    H4_3 = np.eye(4)                 
    H4_3[0:3, 3] = [1, 0, 0]
    H4_3[0:3, 0:3] = Rzyx(np.pi/2, 0, 0)

    H5_4 = np.eye(4)                 
    H5_4[0:3, 3] = [0.6, 0, 0.8]
    H5_4[0:3, 0:3] = Rzyx(np.pi, 0, np.pi)

    H6_5 = np.eye(4)                
    H6_5[0:3, 3] = [0, 1, 0]
    H6_5[0:3, 0:3] = Rzyx(-np.pi/2, 0, 0)

    H7_6 = np.eye(4)                
    H7_6[0:3, 3] = [0, 0.6, 0]
    H7_6[0:3, 0:3] = Rzyx(-np.pi/2, 0, 0)

    H8_7 = np.eye(4)               
    H8_7[0:3, 3] = [0, 1, 0]
    H8_7[0:3, 0:3] = Rzyx(-np.pi/2, 0, 0)

    ################################################################################
    # Question 7: Absolute Transfomations using the relative transformations
    # TODO:
    # Compute again the absolute Homogeneous Transformations of each coordinate
    # frame using the relative transformations and compare them with the
    # absolute transformations computed manually in the first item.

    # Hi_0 = H(i-1)_0 @ Hi_(i-1)  (chain the relative transforms, eq. (25))
    # H1_0 is already the relative transform O0 -> O1
    H2_0 = H1_0 @ H2_1
    H3_0 = H2_0 @ H3_2
    H4_0 = H3_0 @ H4_3
    H5_0 = H4_0 @ H5_4
    H6_0 = H5_0 @ H6_5
    H7_0 = H6_0 @ H7_6
    H8_0 = H7_0 @ H8_7

    # Compare with the manually computed absolute transforms (HT_list_2, Q3)
    HT_rel = [np.eye(4), H1_0, H2_0, H3_0, H4_0, H5_0, H6_0, H7_0, H8_0]
    for i, (H_manual, H_chain) in enumerate(zip(HT_list_2, HT_rel)):
        print(f"O{i}: manual == chained? {np.allclose(H_manual, H_chain)}")


    HT_list_3 = []
    HT_list_3.append(np.eye(4))
    HT_list_3.append(H1_0)
    HT_list_3.append(H2_0)
    HT_list_3.append(H3_0)
    HT_list_3.append(H4_0)
    HT_list_3.append(H5_0)
    HT_list_3.append(H6_0)
    HT_list_3.append(H7_0)
    HT_list_3.append(H8_0)

    fig_3 = plt.figure()
    ax = fig_3.add_subplot(111, projection='3d')
    ax.set_title("Correct Cage with relative HT")
    plot.cage(ax, HT_list_3)

    ################################################################################
    plt.show()


if __name__ == '__main__':
    main()
