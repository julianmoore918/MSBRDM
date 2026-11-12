import sympy as sym
from msbrdm_libs.forward_kinematics import vec_to_skew, exp_matrix


def adjoint_mapping(T: sym.Matrix) -> sym.Matrix:
    """Compute the adjoint mapping of a transformation matrix

    Args:
        T (sym.Matrix): Transformation matrix (4x4)

    Returns:
        sym.Matrix: Adjoint mapping of the transformation matrix
    """
    adj_matrix = sym.eye(6)
    adj_matrix[0:3, 0:3] = T[0:3, 0:3]
    adj_matrix[3:6, 3:6] = T[0:3, 0:3]
    R = T[0:3, 0:3]
    p = T[0:3, 3]
    adj_matrix[3:6, 0:3] = vec_to_skew(p) * R
  
    return adj_matrix


def T_inv(T: sym.Matrix) -> sym.Matrix:
    """Invervse of a transformation matrix

    Args:
        T (sym.Matrix): homogeneous transformation matrix (4x4)

    Returns:
        sym.Matrix: inverse homogeneous transformation matrix (4x4)
    """
    T_inv = sym.eye(4)
    R = T[0:3, 0:3]
    p = T[0:3, 3]
    T_inv[0:3, 0:3] = R.T
    T_inv[0:3, 3] = -R.T * p

    return T_inv


def space_jacobian(SList: sym.Matrix, q: sym.Matrix) -> sym.Matrix:
    """Compute the space jacobian matrix

    Args:
        SList (sym.Matrix): List of screw axes (6 x n)
        q (sym.Matrix): Joint positions (n x 1)

    Returns:
        sym.Matrix: Space jacobian matrix (6 x n)
    """
    Js = sym.zeros(6, len(q))
   
    T = sym.eye(4)                                  
    for i in range(SList.shape[1]):
        Js[:, i] = adjoint_mapping(T) * SList[:, i]  
        T = T * exp_matrix(SList[:, i], q[i])      

    return Js


def body_jacobian(SList: sym.Matrix, q: sym.Matrix, T_b_s: sym.Matrix) -> sym.Matrix:
    """Compute body jacobian from space jacobian

    Args:
        SList (sym.Matrix): List of screw axes (6 x n)
        q (sym.Matrix): Joint positions (n x 1)
        T_b_s (sym.Matrix): Transformation matrix of body w.r.t. space frame

    Returns:
        sym.Matrix: body jacobian matrix (6 x n)
    """
    Jb = sym.zeros(6, len(q))

    Jb = adjoint_mapping(T_inv(T_b_s)) * space_jacobian(SList, q)    
 
    return Jb


def body_jacobian_space_aligned(SList: sym.Matrix, q: sym.Matrix, T_b_s: sym.Matrix) -> sym.Matrix:
    """Body jacobian aligned with the space frame

    Args:
        Jb (sym.Matrix): Body jacobian matrix
        T_b_s (sym.Matrix): Transformation matrix of body w.r.t. space frame

    Returns:
        sym.Matrix: body jacobian matrix aligned with the space frame
    """
    Jb_s = sym.zeros(6, len(q))

    R = T_b_s[0:3, 0:3]
    rot = sym.zeros(6, 6)
    rot[0:3, 0:3] = R
    rot[3:6, 3:6] = R
    Jb_s = rot * body_jacobian(SList, q, T_b_s)
    
    return Jb_s
