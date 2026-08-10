import numpy as np

def parse_matrix(text: str) -> np.ndarray:

# converts a block of text into a numpy 2D array

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

  # converts text into a 1D numpy array
    text = text.replace(",", " ").replace("\n", " ")
    values = [float(v) for v in text.split()]
    if not values:
        raise ValueError("No values entered.")
    return np.array(values)
