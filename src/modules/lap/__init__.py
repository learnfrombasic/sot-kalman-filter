"""
┌─────────────────────────┐
│ Implement LAP algorithm │
│                         │
└─────────────────────────┘
"""

import numpy as np
from scipy.optimize import linear_sum_assignment


def lap(cost_matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    row, col = linear_sum_assignment(cost_matrix)
    return row, col
