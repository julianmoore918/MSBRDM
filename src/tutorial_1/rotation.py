import numpy as np


def R2EulerA(R: np.ndarray) -> tuple:
    # TODO: Fill with the proper rotation Euler angles computation

    phi_d = 0
    theta_d = 0
    psi_d = 0

    return phi_d, theta_d, psi_d


def RotX(alphaX: float) -> np.ndarray:
    # TODO: Fill with the proper rotation matrix

    R = np.eye(3)

    return R


def RotY(betaY: float) -> np.ndarray:
    # TODO: Fill with the proper rotation matrix

    R = np.eye(3)

    return R


def RotZ(gammaZ: float) -> np.ndarray:
    # TODO: Fill with the proper rotation matrix

    R = np.eye(3)

    return R


def invHT(HT: np.array) -> np.ndarray:
    # TODO: Fill with the proper inverse transformation (from the course)
    # Do not use the inv function of numpy !
    
    iHT = np.eye(4)

    return iHT
