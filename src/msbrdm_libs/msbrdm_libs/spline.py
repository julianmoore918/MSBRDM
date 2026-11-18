import numpy as np


def polynomial_5th_order(xi: float, xf: float, ti: float, tf: float) -> np.ndarray:
    """Calculate the coefficients of a 5th-order polynomial trajectory of a 1D spline

    Args:
        xi (float): start position
        xf (float): end position
        ti (float): start time
        tf (float): end time

    Returns:
        np.ndarray: vector of coefficients of the 5th-order polynomial
    """

    def rows(t):
        return [[1, t, t**2,   t**3,    t**4,    t**5],     # position
                [0, 1, 2*t, 3*t**2,  4*t**3,  5*t**4],      # velocity
                [0, 0, 2,   6*t,    12*t**2, 20*t**3]]      # acceleration
    A = np.array(rows(ti) + rows(tf), dtype=float)
    b = np.array([xi, 0.0, 0.0, xf, 0.0, 0.0])
    a = np.linalg.solve(A, b)
    return a

class LinearSplineTrajectory:
    def __init__(self, x_init: np.ndarray, x_final: np.ndarray, duration: float) -> None:
        """Initialize a linear spline trajectory by calculating the coefficients 
        of a 5th-order polynomial for all three linear axes

        Args:
            x_init (np.ndarray): start position [x, y, z]
            x_final (np.ndarray): end position [x, y, z]
            duration (float): duration of the trajectory
        """
        # TODO: calculate the coefficients of the 5th-order polynomial for all three axes

        self.coeffs = np.zeros((3, 6))
        for i in range(3):
            self.coeffs[i] = polynomial_5th_order(x_init[i], x_final[i], 0.0, duration)
        self.duration = duration


    def update(self, t: float) -> np.ndarray:
        """ Update the desired trajectory at time t

        Args:
            t (float): timestamp

        Returns:
            np.ndarray: x_des, v_des, a_des
        """
        x_des = np.zeros(3)
        v_des = np.zeros(3)
        a_des = np.zeros(3)

        # TODO: calculate the desired position, velocity, and acceleration at time t
        # with the coefficients

        t = np.clip(t, 0.0, self.duration)        
        T   = np.array([1, t, t**2, t**3, t**4, t**5])
        dT  = np.array([0, 1, 2*t, 3*t**2, 4*t**3, 5*t**4])
        ddT = np.array([0, 0, 2, 6*t, 12*t**2, 20*t**3])
        x_des = self.coeffs @ T               
        v_des = self.coeffs @ dT
        a_des = self.coeffs @ ddT
        return x_des, v_des, a_des
