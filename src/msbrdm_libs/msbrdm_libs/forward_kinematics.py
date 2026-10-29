import sympy as sym


def vec_to_skew(v: sym.Matrix) -> sym.Matrix:
    """Compute the skew-symmetric matrix of a vector

    Args:
        v (sym.Matrix): 3x1 vector

    Returns:
        sym.Matrix: skew-symmetric matrix form of the vector [v]
    """
    # TODO: Implement the skew-symmetric matrix of a vector
    mat = sym.zeros(3, 3)
    return mat

def rodrigues_formula(omega: sym.Matrix, theta: sym.Matrix) -> sym.Matrix:
    """Compute the rotation matrix using Rodrigues' formula

    Args:
        omega (sym.Matrix): rotation axis
        theta (sym.Matrix): rotation angle

    Returns:
        sym.Matrix: rotation matrix
    """
    # TODO: Implement the rotation matrix using Rodrigues' formula
    R = sym.eye(3)
    return R


def exp_matrix(Si: sym.Matrix, qi: sym.Matrix) -> sym.Matrix:
    """Transformation of joint i using the exponential formula: T = exp([Si]*qi)

    Args:
        Si (sym.Matrix): screw axis of joint i
        qi (sym.Matrix): displacement of joint i

    Returns:
        sym.Matrix: transformation matrix
    """
    # TODO: Implement the transformation matrix using the exponential formula
    Ti = sym.eye(4)
    return Ti


def forward_kinematics(SList: sym.Matrix, M: sym.Matrix, q: sym.Matrix) -> sym.Matrix:
    """Product of exponentials for forward kinematics
    T = exp([S1]*q1) * exp([S2]*q2) * ... * exp([Sn]*qn) * M

    Args:
        SList (sym.Matrix): List of screw axes (6 x n)
        M (sym.Matrix): Initial configuration (4x4)
        q (sym.Matrix): joint displacements (n x 1)

    Returns:
        sym.Matrix: _description_
    """
    # TODO: Implement the product of exponentials for forward kinematics
    T = sym.eye(4)
    return T
