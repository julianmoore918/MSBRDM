import sympy as sym
import numpy as np

from msbrdm_libs.forward_kinematics import *
from msbrdm_libs.jacobians import *


class UR10Model3DOF:
    def __init__(self, pure_symbolic: bool = False) -> None:
        self.pure_symbolic = pure_symbolic
        self.config_joints(nq=3)
        self.config_params()
        self.kinematics()
        self.jacobians()


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
        self.params_dict = {'L1': 0.128, 'L2': 0.6127, 'L3': 0.5716, 
                            'L4': 0.1157, 'L5': 0.1639, 'L6': 0.0922}
        # convert dict to list of tuples for later substitution
        self.params_list = [(k, v) for k, v in self.params_dict.items()]

    def kinematics(self) -> None:
        """Symbolic analysis of forward kinematics
        """
        ########################################################################
        # Robot parameters
        ########################################################################
        if self.pure_symbolic:
            L1, L2, L3, L4, L5, L6 = sym.symbols('L1:7')
        else:
            L1, L2, L3, L4, L5, L6 = [self.params_dict[k] for k in [
                'L1', 'L2', 'L3', 'L4', 'L5', 'L6']]
            

        ########################################################################
        # Base transformation
        ########################################################################
        # TODO: Define the transformation matrix of the base frame (0) w.r.t. world frame (w)
        # {0} sits at the bottom of the base, z up along q1, y along the q2/q3 arrows
        # (to the left in Fig. 4). The URDF attaches base_link to the world without
        # offset, so {0} and {w} coincide.
        self.T_0_w = sym.eye(4)

        ########################################################################
        # Screw axes
        ########################################################################
        # TODO: Treat the {0} frame as spatial frame. Define the screw axes of
        # the robot in a sym.Matrix type
        # S: [w, v].T (6 x n), revolute joints: v = -w x q_point
        omega_list = sym.zeros(3, self.nq)
        v_list = sym.zeros(3, self.nq)


        # points on the joint axes in the home configuration (arm upright, Fig. 4)
        q_1 = sym.Matrix([0, 0, 0])             # base axis
        q_2 = sym.Matrix([0, 0, L1])            # shoulder, L1 above the base
        q_3 = sym.Matrix([0, 0, L1 + L2])       # elbow, L2 above the shoulder

        # joint 1: revolute about z (vertical base axis)
        omega_list[:, 0] = sym.Matrix([0, 0, 1])
        v_list[:, 0] = -omega_list[:, 0].cross(q_1)

        # joint 2: revolute about y (shoulder)
        omega_list[:, 1] = sym.Matrix([0, 1, 0])
        v_list[:, 1] = -omega_list[:, 1].cross(q_2)

        # joint 3: revolute about y (elbow), parallel to joint 2
        omega_list[:, 2] = sym.Matrix([0, 1, 0])
        v_list[:, 2] = -omega_list[:, 2].cross(q_3)

        self.SList = sym.zeros(6, self.nq)
        self.SList[0:3, :] = omega_list
        self.SList[3:6, :] = v_list

        ########################################################################
        # Home Transformation
        ########################################################################
        # TODO: Define the home transformation M of the end-effector
        # Note: you can choose any rotation you like
        # end-effector (red dot in Fig. 4): L5 + L6 sideways along y,
        # L1 + L2 + L3 + L4 above the base; orientation kept aligned with {0}
        self.M_ee_0 = sym.eye(4)
        self.M_ee_0[0:3, 3] = sym.Matrix([0, L5 + L6, L1 + L2 + L3 + L4])

        ########################################################################
        # Forward kinematics
        ########################################################################
        # TODO: Call the fuction implemented in msbrdm_libs/forward_kinematics.py
        # to compute the end-effector frame in {0}
        self.T_ee_0 = forward_kinematics(self.SList, self.M_ee_0, sym.Matrix(self.q))

        # TODO: Calculate the end-effector transforamations in the world frame
        self.T_ee_w = self.T_0_w * self.T_ee_0

        if self.pure_symbolic:
            self.Tsym_ee_0 = self.T_ee_0.copy()
            self.Tsym_ee_w = self.T_ee_w.copy()
            self.T_ee_0 = self.T_ee_0.subs(self.params_list)
            self.T_ee_w = self.T_ee_w.subs(self.params_list)

        ########################################################################
        # Generate functions for numerical evaluation
        ########################################################################
        # TODO: Generate transformation functions of joint poisition T(q) for
        # numerical updates, use sym.lambdify() function
        self.T_ee_0_fn = sym.lambdify(self.q, self.T_ee_0, 'numpy')
        self.T_ee_w_fn = sym.lambdify(self.q, self.T_ee_w, 'numpy')

    def jacobians(self) -> None:
        """Symbolic analysis of Jacobians
        """
        ########################################################################
        # TODO: call the appropriate function in msbrdm_libs/jacobians.py to
        # compute the end-effector jacobian in {0} frame J_ee_0 (6xn)
        # space-aligned body jacobian: velocity of the ee point, expressed in {0}
        # (use the unsubstituted pose so Jsym stays purely symbolic)
        T_ee_0 = self.Tsym_ee_0 if self.pure_symbolic else self.T_ee_0
        self.J_ee_0 = body_jacobian_space_aligned(self.SList, sym.Matrix(self.q), T_ee_0)

        ########################################################################
        # TODO: Rotate the end-effector jacobian in the world frame J_ee_w (6xn)
        # J_ee_w = blockdiag(R_0_w, R_0_w) * J_ee_0
        R_0_w = self.T_0_w[0:3, 0:3]
        rot = sym.zeros(6, 6)
        rot[0:3, 0:3] = R_0_w
        rot[3:6, 3:6] = R_0_w
        self.J_ee_w = rot * self.J_ee_0

        if self.pure_symbolic:
            self.Jsym_ee_0 = self.J_ee_0.copy()
            self.Jsym_ee_w = self.J_ee_w.copy()
            self.J_ee_0 = self.J_ee_0.subs(self.params_list)
            self.J_ee_w = self.J_ee_w.subs(self.params_list)

        ########################################################################
        # TODO: Generate jacobian functions for numerical evaluation
        self.J_ee_0_fn = sym.lambdify(self.q, self.J_ee_0, 'numpy')
        self.J_ee_w_fn = sym.lambdify(self.q, self.J_ee_w, 'numpy')



if __name__ == '__main__':
    model = UR10Model3DOF(pure_symbolic=True)

    print("Tsym_ee_0:\n", model.Tsym_ee_0, "\n")
    print("Tsym_ee_w:\n", model.Tsym_ee_w, "\n")
    print("Jsym_ee_0:\n", model.Jsym_ee_0, "\n")
    print("Jsym_ee_w:\n", model.Jsym_ee_w, "\n")