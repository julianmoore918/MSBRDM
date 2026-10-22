import numpy as np
import matplotlib.pyplot as plt
from tutorial_1.rotation import RotX, RotY, RotZ, invHT
import tutorial_1.plot as plot

################################################################################
# Provided transform
L = 1

l = L/(2*np.tan(np.pi/5))

H3_0 = np.eye(4)
H3_0[0:3, 3] = [0, L/2, -l]
H3_0[0:3, 0:3] = RotX(-np.pi/10)@RotZ(-np.pi/2)

H4_3 = np.eye(4)
H4_3[0:3, 3] = [L*np.cos(np.pi/10), 0, -L*np.sin(np.pi/10)]
H4_3[0:3, 0:3] = RotY(-3*np.pi/10)

H3_1 = np.eye(4)
H3_1[0:3, 3] = [-(np.sqrt(L**2/4+(l+np.sqrt(l**2+L**2/4))**2))
                * np.cos(3*np.pi/10-np.arctan(L/(2*(l+np.sqrt(l**2+(L**2)/4))))),
                0,
                -(np.sqrt(L**2/4+(l+np.sqrt(l**2+L**2/4))**2))
                * np.sin(3*np.pi/10-np.arctan(L/(2*(l+np.sqrt(l**2+(L**2)/4)))))]
H3_1[0:3, 0:3] = RotY(np.pi/10)

H5_2 = np.eye(4)
H5_2[0:3, 3] = [0, 2*L*np.cos(np.pi/10)*np.sin(3*np.pi/10),
                2*L*np.sin(np.pi/10)*np.sin(3*np.pi/10)]
H5_2[0:3, 0:3] = RotX(np.pi/5)@RotZ(3*np.pi/2)

H2_1 = np.eye(4)
H2_1[0:3, 3] = [-L, 0, 0]
H2_1[0:3, 0:3] = RotZ(np.pi/2)@RotX(-9*np.pi/10)

################################################################################
# Question 1: Manually computed Homogeneous Transformations
# TODO:
# Using the provided transforms, compute the absolute homogeneous
# transformations $\mathbf{H}_0**{i}$ associated with each frame of the
# pentagon. Each transform must be written as a sequence of the previously
# computed transforms.

H1_0 = np.eye(4)
H2_0 = np.eye(4)
H4_0 = np.eye(4)
H5_0 = np.eye(4)

HT_list_1 = []
HT_list_1.append(np.eye(4))
HT_list_1.append(H1_0)
HT_list_1.append(H2_0)
HT_list_1.append(H3_0)
HT_list_1.append(H4_0)
HT_list_1.append(H5_0)

fig_1 = plt.figure()
ax = fig_1.add_subplot(111, projection='3d')
ax.set_title("Original Pentagon")

plot.polygon(ax, HT_list_1, color='blue')

################################################################################
# Question 2: Relative Homogeneous Transformations
# TODO:
# Compute the relative Homogeneous Transformations between each vertex of
# the pentagon.

H3_2 = np.eye(4)
H5_4 = np.eye(4)

################################################################################
# Question 3: Relative Homogeneous Transformations
# TODO:
# Compute the transforms H5_1, H3_5 and H4_2 using at least three different
# sequences of homogeneous transforms for each of them. You are free to
# chose whatever sequence you believe is right.

H5_1 = np.eye(4)
H5_4 = np.eye(4)
H4_2 = np.eye(4)

################################################################################
# Question 4: Transform the whole pentagon including all its coordinate frames
# TODO: Complete the transformation sequence HS1 and HS2

HS1 = np.eye(4)
HS2 = np.eye(4)

HT_list_S1 = [np.eye(4)]
HT_list_S2 = [np.eye(4)]
for i in range(1, len(HT_list_1)):
    HT_list_S1.append(HS1@HT_list_1[i])
    HT_list_S2.append(HS2@HT_list_1[i])

fig_2 = plt.figure()
ax = fig_2.add_subplot(111, projection='3d')
ax.set_title("Rotated Pentagons")

plot.polygon(ax, HT_list_1, color='blue')
plot.polygon(ax, HT_list_S1, color='magenta')
plot.polygon(ax, HT_list_S2, color='cyan')

# Explanation:

################################################################################
# Question 5: Copy HS2
# Replace its last row by [a,b,c,d] where a,b,c and d are real numbers.
# For each Hi_0, extract the corresponding position vector and transform it
# using the non-homogeneous transformation.
# Plot the vertices in a new figure using the provided plot function.
# Do this for three different vectors [a,b,c,d].

HS3 = HS2.copy()

# Explanation:


################################################################################
plt.show()
