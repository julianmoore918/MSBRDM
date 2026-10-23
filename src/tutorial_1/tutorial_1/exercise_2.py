import numpy as np
import matplotlib.pyplot as plt
from tutorial_1.rotation import RotX, RotY, RotZ, Rzyx, invHT
import tutorial_1.plot as plot


def main():

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
    H1_0 = H3_0 @ invHT(H3_1)

    H2_0 = np.eye(4)
    H2_0 = H3_0 @ invHT(H3_1) @ H2_1

    H4_0 = np.eye(4)
    H4_0 = H3_0 @ H4_3

    H5_0 = np.eye(4)
    H5_0 = H2_0 @ H5_2

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
    H3_2[0:3, 3] = [0,0,L]
    H3_2[0:3, 0:3] = Rzyx(np.pi/2, 0,np.pi)

    H5_4 = np.eye(4)
    H5_4[0:3, 3] = [L, 0, 0]
    H5_4[0:3, 0:3] = Rzyx(0, -np.pi/2, 0)

    ################################################################################
    # Question 3: Relative Homogeneous Transformations
    # TODO:
    # Compute the transforms H5_1, H3_5 and H4_2 using at least three different
    # sequences of homogeneous transforms for each of them. You are free to
    # chose whatever sequence you believe is right.

    H5_1 = np.eye(4)
    H5_1 = H2_1 @ H5_2
    H5_1 = invHT(H1_0) @ H5_0
    H5_1 = H3_1 @ H4_3 @ H5_4

    H3_5 = np.eye(4)
    H3_5 = invHT(H5_2) @ H3_2                
    H3_5 = invHT(H5_0) @ H3_0                
    H3_5 = invHT(H5_4) @ invHT(H4_3)        


    H4_2 = np.eye(4)
    H4_2 = H3_2 @ H4_3                        
    H4_2 = invHT(H2_0) @ H4_0                 
    H4_2 = H5_2 @ invHT(H5_4)                


    ################################################################################
    # Question 4: Transform the whole pentagon including all its coordinate frames
    # TODO: Complete the transformation sequence HS1 and HS2

    HS1 = np.eye(4)
    HS1[0:3, 0:3] = Rzyx(np.pi/4, -np.pi/6, np.pi/2) 
    HS1[0:3, 3] = [2, 0.75, 0.75]

    HS2 = np.eye(4)
    HS2[0:3, 0:3] = Rzyx(np.pi/6, np.pi/4, np.pi/2)
    HS2[0:3, 3] = [2, -0.75, 0.75]

    HT_list_S1 = [HS1]
    HT_list_S2 = [HS2]
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

    # HS1 rotates about the CURRENT (moving) axes x0 -> y0' -> z0'', so the
    # rotations are post-multiplied: R1 = Rx(90) @ Ry(45) @ Rz(30).
    # HS2 rotates about the FIXED axes x0 -> y0 -> z0, so the rotations are
    # pre-multiplied: R2 = Rz(30) @ Ry(45) @ Rx(90).
    # Rotation matrices do not commute, so with the same three angles R1 != R2
    # and the two pentagons end up with different orientations. R1 can also be
    # written as a fixed-axes rotation, but with other angles (45, -30, 90 deg).
    # The translations are both along the fixed axes; they only differ in the
    # sign of y (+0.75 vs -0.75), which places the pentagons on opposite sides.
    #
    # Implementation: for cleaner code I added the helper function
    # Rzyx(phi, theta, psi) = RotZ(phi) @ RotY(theta) @ RotX(psi) to
    # rotation.py (roll-pitch-yaw, eq. (10)). It directly gives the fixed-axes
    # sequence HS2 = Rzyx(30, 45, 90 deg). HS1 (current axes) has the reverse
    # order Rx @ Ry @ Rz, so with Rzyx it needs the equivalent fixed-axes
    # angles Rzyx(45, -30, 90 deg) (obtained with R2EulerA and checked to give
    # the same matrix as RotX(90) @ RotY(45) @ RotZ(30)).
    #
    # Aspect ratio: yes, preserved. HS1, HS2 are in SE(3) (R in SO(3), last
    # row [0 0 0 1]), i.e. rigid transformations:
    #   |(R p1 + t) - (R p2 + t)| = |R (p1 - p2)| = |p1 - p2|
    # Distances and angles are kept, so all sides stay L = 1 and the pentagon
    # stays regular - it is only moved and rotated.

    ################################################################################
    # Question 5: Copy HS2
    # Replace its last row by [a,b,c,d] where a,b,c and d are real numbers.
    # For each Hi_0, extract the corresponding position vector and transform it
    # using the non-homogeneous transformation.
    # Plot the vertices in a new figure using the provided plot function.
    # Do this for three different vectors [a,b,c,d].

    HS3 = HS2.copy()

    # Explanation:
    # A last row [a b c d] makes HS3 a projective (non-SE(3)) transform:
    # HS3 [p; 1] = [R p + t; w], w = a*x + b*y + c*z + d. After dividing by w:
    # - a=b=c=0: uniform scaling by 1/d (shape kept, size changes).
    # - a,b,c != 0: w differs per vertex -> perspective distortion,
    #   aspect ratio not preserved.
    # - a only: no effect, since all vertices have x = 0.

    ################################################################################
    plt.show()


if __name__ == '__main__':
    main()
