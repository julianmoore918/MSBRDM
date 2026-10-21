#!/usr/bin/env python
import numpy as np
import tutorial_1.plot as plot
from tutorial_1.rotation import R2EulerA
import matplotlib.pyplot as plt


################################################################################
# Question 1: Manually computed Homogeneous Transformations
# TODO:
# By simple inspection obtain manually the absolute homogeneous transformations
# Ti_0 for each corner of the cage with respect to the coordinate frame O_0

T1_0 = np.eye(4)
T2_0 = np.eye(4)
T3_0 = np.eye(4)
T4_0 = np.eye(4)
T5_0 = np.eye(4)
T6_0 = np.eye(4)
T7_0 = np.eye(4)
T8_0 = np.eye(4)

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

# Plot the cage
fig_1 = plt.figure()
ax = fig_1.add_subplot(111, projection='3d')
ax.set_title("Cage with Left handed Oi and ... and ... (in Magenta)")

plot.cage(ax, HT_list_1)

# ax.plot(x, y, z, 'mo', markersize=10)

# Explanation:


################################################################################
# Question 3: Right Hand Frames
# TODO:
# Replace the coordinate frames found in the above question with the
# suitable coordinate frames, respecting the figure convention;
# then compute the associated absolute homogeneous transformations Hi_0

H1_0 = np.eye(4)
H2_0 = np.eye(4)
H3_0 = np.eye(4)
H4_0 = np.eye(4)
H5_0 = np.eye(4)
H6_0 = np.eye(4)
H7_0 = np.eye(4)
H8_0 = np.eye(4)

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

# Ri_0 = ...
# pi_0 = ...
# ...

################################################################################
# Question 5: Simple Euler angles without considering singularities
# TODO:
# Represent each rotation matrix as a set of Euler angles (roll-pitch-yaw)

# phi_i, theta_i, psi_i = R2EulerA(Ri_0)
# ...


################################################################################
# Question 6: Relative Homogeneous Transformations (manually Generated)
# TODO:
# Compute manually the the relative transformations between the corners of
# the cage

H1_0 = np.eye(4)
H2_1 = np.eye(4)
H3_2 = np.eye(4)
H4_3 = np.eye(4)
H5_4 = np.eye(4)
H6_5 = np.eye(4)
H7_6 = np.eye(4)
H8_7 = np.eye(4)

################################################################################
# Question 7: Absolute Transfomations using the relative transformations
# TODO:
# Compute again the absolute Homogeneous Transformations of each coordinate
# frame using the relative transformations and compare them with the
# absolute transformations computed manually in the first item.

# Hi_0 = ...


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
