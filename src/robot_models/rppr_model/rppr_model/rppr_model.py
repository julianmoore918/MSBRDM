import sympy as sym
import numpy as np

import msbrdm_libs.forward_kinematics as FK
from msbrdm_libs.jacobians import *


class RPPRModel():
    """ Symbolic analysis of the RPPR robot model, and generation of substitute
    functions for numerical updates
    """
    def __init__(self, pure_symbolic: bool = False) -> None:
        self.config_joints(nq=4)
        self.config_params()
        self.kinematics(pure_symbolic=pure_symbolic)
        self.jacobians(pure_symbolic=pure_symbolic)

    def config_joints(self, nq: int) -> None:
        """Define symbolic variables for robot joints

        Args:
            nq (int): number of joints
        """
        # number of joints
        self.nq = nq
        # define joint symbols
        self.q = sym.symbols('q(0:'+str(self.nq)+')')
        self.qdot = sym.symbols('q(0:'+str(self.nq)+')dot')
        self.qddot = sym.symbols('q(0:'+str(self.nq)+')ddot')

    def config_params(self) -> None:
        """ Initialize robot parameters
        """
        # save robot parameters as a dictionary
        self.params_dict = {'L1': 0.3, 'L2': 0.34, 'L3': 0.583, 'L4': 0.08,
                            'L5': 0.08, 'L6': 0.115, 'L7': 0.082, 'L8': 0.108,
                            'L9': 0.123, 'L10': 0.167, 'L11': 0.028, 'L12': 0.05,
                            'c': 0.32, 'd': 0.32, 'theta1': np.pi/4., 'theta2': np.pi/6.,
                            'q2_offset': 0.12, 'q3_offset': 0.12}
        # convert dict to list of tuples for later substitution
        self.params_list = [(k, v) for k, v in self.params_dict.items()]

    def kinematics(self, pure_symbolic: bool = False) -> None:
        """ Symbolic analysis of forward kinematics

        Args:
            pure_symbolic (bool, optional): If true, use symbolic form for robot
            parameters (for generality, e.g. reuse UR5 model for UR10);
            If false, directy use numeric values (for faster compulation).
            Defaults to False.
        """
        ########################################################################
        # Robot Parameters
        ########################################################################
        if pure_symbolic:
            # define symbolic variables for robot parameters
            L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12 = sym.symbols(
                'L1:13')
            c, theta1, theta2 = sym.symbols('c theta1 theta2')
            q2_offset, q3_offset = sym.symbols('q2_offset q3_offset')
        else:
            # get numeric values for robot parameters
            L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12 = [self.params_dict[k] for k in [
                'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11', 'L12']]
            c, theta1, theta2 = [self.params_dict[k]
                                 for k in ['c', 'theta1', 'theta2']]
            q2_offset, q3_offset = [self.params_dict[k]
                                    for k in ['q2_offset', 'q3_offset']]

        # TODO: Define more intermediate variables here
        # e.g. L13 = L5 + L6 ...
        L13 = L9*sym.cos(theta2)
        L14 = (L10+L11)*sym.sin(theta1)
        L15 = (L10+L11)*sym.cos(theta1)
        L16 = L9*sym.sin(theta2)
        L17 = L10/sym.cos(theta1)

        q_1 = sym.Matrix([0, -(L4), 0])

        q_2 = sym.Matrix([-(L5),
                          -(L4),
                          0])#

        q_3 = sym.Matrix([-(L5 + q2_offset + L6),
                        -(L4),
                        -(L7)])

        q_4  = sym.Matrix([-(L5 + q2_offset + L6),
                        -(L4 + L13),
                        -(L7 + q3_offset + L8 + L16)])

        q_ee = q_4 + sym.Matrix([L15 + L12 + c/2, 0, L14])

        cm1 = sym.Matrix([-L5, -L4, 0])
        cm2 = sym.Matrix([-(L5 + q2_offset), -L4, -L7/2])   # cm2 not dimensioned in Fig. 1, read off
        cm3 = q_4 + sym.Matrix([L17, 0, 0])
        cm4 = q_ee

        ########################################################################
        # Base transformation
        ########################################################################
        # TODO: Define the transformation matrix of the base frame (0) w.r.t. world frame (w)
        # in a sym.Matrix type
        self.T_0_w = sym.eye(4)
        self.T_0_w = sym.Matrix([[sym.cos(0), -sym.sin(0), 0, L1],
                                 [sym.sin(0), sym.cos(0), 0, L2],
                                 [0, 0, 1, L3],
                                 [0, 0, 0, 1]])
        
        ########################################################################
        # Screw Axes
        ########################################################################
        # TODO: Define the screw axes of the robot in a sym.Matrix type
        # S: [w, v].T (6 x n)
        omega_list = sym.zeros(3, self.nq)
        v_list = sym.zeros(3, self.nq)

        # joint 1: revolute about y through origin of {0}
        omega_list[:, 0] = sym.Matrix([0, 1, 0])
        v_list[:, 0] = -omega_list[:, 0].cross(sym.Matrix([0, 0, 0]))

        # joint 2: prismatic along -x  (omega stays 0)
        v_list[:, 1] = sym.Matrix([-1, 0, 0])

        # joint 3: prismatic along -z  (omega stays 0)
        v_list[:, 2] = sym.Matrix([0, 0, -1])

        # joint 4: revolute about tilted axis through point q_4
        omega_list[:, 3] = sym.Matrix([sym.cos(theta1), 0, sym.sin(theta1)])
        v_list[:, 3] = -omega_list[:, 3].cross(q_4)

        # stack: rows 0-2 omega, rows 3-5 v
        SList = sym.zeros(6, self.nq)
        SList[0:3, :] = omega_list
        SList[3:6, :] = v_list
        self.SList = SList



        #######################################################################
        # Home configuration
        #######################################################################
        # TODO: Define the home transformation M of the end-effector
        # Note: you can choose any rotation you like
        self.M_ee_0 = sym.eye(4)
        self.M_ee_0[0:3, 3] = q_ee

        # TODO: Define the home transformations of each center of mass
        # Note: you can choose any rotation you like
        self.M_cm1_0 = sym.eye(4)
        self.M_cm1_0[0:3, 3] = q_1
        self.M_cm2_0 = sym.eye(4)
        self.M_cm2_0[0:3, 3] = q_2
        self.M_cm3_0 = sym.eye(4)
        self.M_cm3_0[0:3, 3] = q_3
        self.M_cm4_0 = sym.eye(4)
        self.M_cm4_0[0:3, 3] = q_4
        # Alternative: you can also define them as a list of transformations for
        # loop calculation 
        cm_points = [cm1, cm2, cm3, cm4]
        self.M_cms_0 = []
        for p in cm_points:
            M = sym.eye(4)
            M[0:3, 3] = p
            self.M_cms_0.append(M)
            
        ########################################################################
        # Forward Kinematics
        ########################################################################
        # TODO: Call the fuction implemented in msbrdm_libs/forward_kinematics.py
        # to compute the end-effector frame and the center of mass frames

        self.T_ee_0 = sym.eye(4)
        self.T_ee_0 = FK.forward_kinematics(SList, self.M_ee_0, sym.Matrix(self.q))
        self.T_cm1_0 = sym.eye(4)
        self.T_cm1_0 = FK.forward_kinematics(SList, self.M_cm1_0, sym.Matrix(self.q))
        self.T_cm2_0 = sym.eye(4)
        self.T_cm2_0 = FK.forward_kinematics(SList, self.M_cm2_0, sym.Matrix(self.q))
        self.T_cm3_0 = sym.eye(4)
        self.T_cm3_0 = FK.forward_kinematics(SList, self.M_cm3_0, sym.Matrix(self.q))
        self.T_cm4_0 = sym.eye(4)
        self.T_cm4_0 = FK.forward_kinematics(SList, self.M_cm4_0, sym.Matrix(self.q))
        # Alternative: loop calculation with a list of transformations
        q_vec = sym.Matrix(self.q)
        self.T_cms_0 = []
        for i in range(len(self.M_cms_0)):
            # cm of link i+1 only moves with joints 1..i+1
            self.T_cms_0.append(FK.forward_kinematics(SList[:, :i+1], self.M_cms_0[i], q_vec[:i+1, :]))



        # TODO: Calculate the end-effector transforamations in the world frame
        self.T_ee_w = sym.eye(4)
        self.T_ee_w = self.T_0_w @ self.T_ee_0

        if pure_symbolic:
            # save the pure symbolic expressions
            self.Tsym_ee_0 = self.T_ee_0.copy()
            self.Tsym_ee_w = self.T_ee_w.copy()
            self.Tsym_cms_0 = self.T_cms_0.copy()
            # substitute symbolic parameters with numeric values before generate functions
            self.T_ee_0 = self.T_ee_0.subs(self.params_list)
            self.T_ee_w = self.T_ee_w.subs(self.params_list)
            for i in range(len(self.T_cms_0)):
                self.T_cms_0[i] = self.T_cms_0[i].subs(self.params_list)

        ########################################################################
        # Generate functions
        ########################################################################
        # TODO: Generate transformation functions of joint poisition T(q) for
        # numerical updates, use sym.lambdify() function

        self.T_ee_w_fn = sym.lambdify(self.q, self.T_ee_w, 'numpy')
        self.T_cms_0_fn = [sym.lambdify(self.q, T, 'numpy') for T in self.T_cms_0]

    def jacobians(self, pure_symbolic: bool = False) -> None:
        """ Symbolic jacobians of the end-effector and the centers of mass in {0} """
        q_vec = sym.Matrix(self.q)
        # poses without numeric substitution if pure_symbolic
        T_ee_0 = self.Tsym_ee_0 if pure_symbolic else self.T_ee_0
        T_cms_0 = self.Tsym_cms_0 if pure_symbolic else self.T_cms_0

        # end-effector: all joints
        self.J_ee_0 = body_jacobian_space_aligned(self.SList, q_vec, T_ee_0)

        # cm_i only moves with joints 1..i, remaining columns stay zero
        self.J_cms_0 = []
        for i in range(self.nq):
            J = sym.zeros(6, self.nq)
            J[:, :i+1] = body_jacobian_space_aligned(self.SList[:, :i+1], q_vec[:i+1, :], T_cms_0[i])
            self.J_cms_0.append(J)

        if pure_symbolic:
            self.Jsym_ee_0 = self.J_ee_0.copy()
            self.Jsym_cms_0 = [J.copy() for J in self.J_cms_0]
            self.J_ee_0 = self.J_ee_0.subs(self.params_list)
            self.J_cms_0 = [J.subs(self.params_list) for J in self.J_cms_0]

        self.J_ee_0_fn = sym.lambdify(self.q, self.J_ee_0, 'numpy')
        self.J_cms_0_fn = [sym.lambdify(self.q, J, 'numpy') for J in self.J_cms_0]




def main():
    model = RPPRModel(pure_symbolic=True)

    ############################################################################
    # Print out expressions
    ############################################################################

    # Pure symbolic
    print("Tsym_ee_0: ", model.Tsym_ee_0, "\n")
    print("Tsym_ee_w: ", model.Tsym_ee_w, "\n")
    print("Tsym_cm1_0: ", model.Tsym_cms_0[0], "\n")
    print("Tsym_cm2_0: ", model.Tsym_cms_0[1], "\n")
    print("Tsym_cm3_0: ", model.Tsym_cms_0[2], "\n")
    print("Tsym_cm4_0: ", model.Tsym_cms_0[3], "\n")

    # Partially symbolic (only function of joint states)
    print("T_ee_0: ", model.T_ee_0, "\n")
    print("T_ee_w: ", model.T_ee_w, "\n")
    print("T_cm1_0: ", model.T_cms_0[0], "\n")
    print("T_cm2_0: ", model.T_cms_0[1], "\n")
    print("T_cm3_0: ", model.T_cms_0[2], "\n")
    print("T_cm4_0: ", model.T_cms_0[3], "\n")

if __name__ == '__main__':
    main()
