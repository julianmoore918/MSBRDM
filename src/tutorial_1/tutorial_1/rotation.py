import numpy as np


def R2EulerA(R: np.ndarray) -> tuple:
    # Roll-pitch-yaw (x-y-z, fixed frame), eq. (13a-d)
    # PDF uses 1-based R(i,j) -> numpy R[i-1, j-1]

    d = np.sqrt(max(0.0, 1 - R[2, 0]**2))       # (13a), positive root

    phi_d = np.arctan2(R[1, 0], R[0, 0])        # (13c) roll  about z
    theta_d = np.arctan2(-R[2, 0], d)           # (13b) pitch about y
    psi_d = np.arctan2(R[2, 1], R[2, 2])        # (13d) yaw   about x

    return phi_d, theta_d, psi_d


def RotX(alphaX: float) -> np.ndarray:
    # TODO: Fill with the proper rotation matrix

    c, s = np.cos(alphaX), np.sin(alphaX)

    R = np.array([[1, 0,  0],
                  [0, c, -s],
                  [0, s,  c]])

    return R


def RotY(betaY: float) -> np.ndarray:
    # TODO: Fill with the proper rotation matrix

    c, s = np.cos(betaY), np.sin(betaY)

    R = np.array([[c, 0, s],
                  [0, 1, 0],
                  [-s, 0, c]])

    return R


def RotZ(gammaZ: float) -> np.ndarray:
    # TODO: Fill with the proper rotation matrix

    c, s = np.cos(gammaZ), np.sin(gammaZ)

    R = np.array([[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]])

    return R

def Rzyx(phi: float, theta: float, psi: float) -> np.ndarray:
    # Roll-pitch-yaw, eq. (10): R = Rz(phi) @ Ry(theta) @ Rx(psi)
    return RotZ(phi) @ RotY(theta) @ RotX(psi)

def invHT(HT: np.array) -> np.ndarray:
    # TODO: Fill with the proper inverse transformation (from the course)
    # Do not use the inv function of numpy !
    R = HT[0:3, 0:3]
    t = HT[0:3, 3]
    
    iHT = np.eye(4)
    iHT[:3, :3] = R.T
    iHT[:3, 3] = -R.T @ t

    return iHT
