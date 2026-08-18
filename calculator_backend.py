"""
calculator_backend.py

Backend logic for the NumPy Maths Calculator GUI.

The GUI (gui_calculator.py) imports this module and calls these functions.
Parsing helpers are already implemented for you. The actual maths functions
are left as TODOs — implement them using numpy, and the GUI will "just work"
since it already calls them and displays whatever they return.

Each function currently raises NotImplementedError; the GUI catches that
and shows a friendly "Not implemented yet" message, so you can run the app
immediately and fill functions in one at a time.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Parsing helpers (already implemented for you)
# ---------------------------------------------------------------------------

def parse_matrix(text: str) -> np.ndarray:
    """
    Convert a block of text into a numpy 2D array.
    Rows are separated by newlines; values within a row by spaces or commas.

    Example input:
        "1 2 3\n4 5 6\n7 8 9"
    """
    rows = [r.strip() for r in text.strip().splitlines() if r.strip()]
    if not rows:
        raise ValueError("No matrix data entered.")
    matrix = []
    for row in rows:
        row = row.replace(",", " ")
        values = [float(v) for v in row.split()]
        matrix.append(values)
    return np.array(matrix)


def parse_vector(text: str) -> np.ndarray:
    """
    Convert text into a 1D numpy array.
    Values may be separated by spaces, commas, or newlines.
    """
    text = text.replace(",", " ").replace("\n", " ")
    values = [float(v) for v in text.split()]
    if not values:
        raise ValueError("No values entered.")
    return np.array(values)


# ---------------------------------------------------------------------------
# 1. Basic calculator
# ---------------------------------------------------------------------------

def evaluate_expression(expression: str):

    solution = eval(expression)
    return solution
    raise NotImplementedError("evaluate_expression is not implemented yet")


# ---------------------------------------------------------------------------
# 2. Matrix operations
# ---------------------------------------------------------------------------

def matrix_add(a: np.ndarray, b: np.ndarray):
    return(a + b)
    raise NotImplementedError("matrix_add is not implemented yet")


def matrix_subtract(a: np.ndarray, b: np.ndarray):
    return(a-b)
    raise NotImplementedError("matrix_subtract is not implemented yet")


def matrix_multiply(a: np.ndarray, b: np.ndarray):
    return(a @ b)
    raise NotImplementedError("matrix_multiply is not implemented yet")


def matrix_transpose(a: np.ndarray):
    return np.transpose(a)
    raise NotImplementedError("matrix_transpose is not implemented yet")


def matrix_inverse(a: np.ndarray):
    return np.invert(a)
    raise NotImplementedError("matrix_inverse is not implemented yet")


def matrix_determinant(a: np.ndarray):
    np.linalg.det(a)
    raise NotImplementedError("matrix_determinant is not implemented yet")


def matrix_eigen(a: np.ndarray):
    return np.linalg.eig(a)
    raise NotImplementedError("matrix_eigen is not implemented yet")


# ---------------------------------------------------------------------------
# 3. Statistics
# ---------------------------------------------------------------------------

def stats_summary(data: np.ndarray):
    """
    Should return a dict, e.g.:
        {
            "mean": ..., "median": ..., "std": ..., "var": ...,
            "min": ..., "max": ..., "sum": ..., "count": ...
        }
    The GUI will print each key/value pair on its own line automatically.
    """
    raise NotImplementedError("stats_summary is not implemented yet")


# ---------------------------------------------------------------------------
# 4. Linear algebra / equation solving
# ---------------------------------------------------------------------------

def solve_linear_system(a: np.ndarray, b: np.ndarray):
    """Solve Ax = b for x and return it."""
    raise NotImplementedError("solve_linear_system is not implemented yet")


# ---------------------------------------------------------------------------
# 5. Functions (trig, log, exponential, powers, etc.)
# ---------------------------------------------------------------------------

def apply_function(name: str, value: float, use_degrees: bool = False):
    """
    `name` will be one of:
        'sin', 'cos', 'tan', 'exp', 'log', 'log10', 'sqrt', 'square', 'cbrt'

    `use_degrees` is True if the user ticked the "Use degrees" box
    (relevant for sin/cos/tan only — remember to convert with np.radians).
    """
    raise NotImplementedError("apply_function is not implemented yet")

# to add a GraphTab that uses matplotlib
