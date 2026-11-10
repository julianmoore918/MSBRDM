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

    a = np.zeros(6)
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

        return x_des, v_des, a_des
