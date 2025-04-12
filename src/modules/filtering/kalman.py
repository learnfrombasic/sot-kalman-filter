"""
┌───────────────────────────────────┐
│ Implement Kalman Filter algorithm │
│                                   │
└───────────────────────────────────┘
"""

from typing import Tuple

import numpy as np
from numpy import dot
from numpy.linalg import inv


class KalmanFilter:
    """
    A simple implementation of the discrete-time Kalman Filter
    for linear systems with Gaussian noise.
    """

    def __init__(self, X: np.ndarray, P: np.ndarray, H: np.ndarray, R: np.ndarray):
        """
        Initialize the Kalman Filter.

        Parameters:
        - X (np.ndarray): Initial state estimate.
        - P (np.ndarray): Initial estimate covariance matrix.
        - H (np.ndarray): Observation model matrix.
        - R (np.ndarray): Measurement noise covariance matrix.
        """
        self.X = X
        self.P = P
        self.H = H
        self.R = R

    def predict(
        self, A: np.ndarray, Q: np.ndarray, B: np.ndarray = None, U: np.ndarray = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform the prediction step of the Kalman Filter.

        Parameters:
        - A (np.ndarray): State transition matrix
        - Q (np.ndarray): Process noise covariance
        - B (np.ndarray, optional): Control input matrix
        - U (np.ndarray, optional): Control input

        Returns:
        - Tuple containing:
            - Predicted state estimate (X)
            - Predicted estimate covariance (P)
        """
        if B is None or U is None:
            self.X = dot(A, self.X)
        else:
            self.X = dot(A, self.X) + dot(B, U)

        self.P = dot(A, dot(self.P, A.T)) + Q
        return self.X, self.P

    def update(
        self, Y: np.ndarray
    ) -> Tuple[
        np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, Tuple[float, float]
    ]:
        """
        Perform a Kalman Filter update with a new observation Y.

        Parameters:
        - Y (np.ndarray): New observation vector.

        Returns:
        - Tuple containing:
            - Updated state estimate (X)
            - Updated covariance matrix (P)
            - Kalman gain (K)
            - Innovation mean (IM)
            - Innovation covariance (IS)
            - Likelihood of the observation (LH)
        """
        IM = dot(self.H, self.X)
        IS = self.R + dot(self.H, dot(self.P, self.H.T))
        K = dot(self.P, dot(self.H.T, inv(IS)))
        self.X = self.X + dot(K, (Y - IM))
        self.P = self.P - dot(K, dot(IS, K.T))
        LH = self._gauss_pdf(Y, IM, IS)
        return self.X, self.P, K, IM, IS, LH

    @staticmethod
    def _gauss_pdf(X: np.ndarray, M: np.ndarray, S: np.ndarray) -> Tuple[float, float]:
        """
        Compute the probability density of a multivariate Gaussian.

        Parameters:
        - X (np.ndarray): Input vector or matrix.
        - M (np.ndarray): Mean vector or matrix.
        - S (np.ndarray): Covariance matrix.

        Returns:
        - Tuple containing:
            - Probability density value at X (P)
            - Exponent value before applying exp (E)
        """
        if M.shape[1] == 1:
            DX = X - np.tile(M, X.shape[1])
            E = 0.5 * np.sum(DX * (np.dot(np.linalg.inv(S), DX)), axis=0)
            E = (
                E
                + 0.5 * M.shape[0] * np.log(2 * np.pi)
                + 0.5 * np.log(np.linalg.det(S))
            )
            P = np.exp(-E)
        elif X.shape[1] == 1:
            DX = np.tile(X, M.shape[1]) - M
            E = 0.5 * np.sum(DX * (np.dot(np.linalg.inv(S), DX)), axis=0)
            E = (
                E
                + 0.5 * M.shape[0] * np.log(2 * np.pi)
                + 0.5 * np.log(np.linalg.det(S))
            )
            P = np.exp(-E)
        else:
            DX = X - M
            E = 0.5 * np.dot(DX.T, np.dot(np.linalg.inv(S), DX))
            E = (
                E
                + 0.5 * M.shape[0] * np.log(2 * np.pi)
                + 0.5 * np.log(np.linalg.det(S))
            )
            P = np.exp(-E)
        return float(P[0]), float(E[0])
