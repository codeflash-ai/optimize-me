from typing import List, Optional, Tuple, Union

import numpy as np


Matrix = Union[List[List[float]], List[np.ndarray], np.ndarray]
Vector = Union[List[float], np.ndarray]


def cosine_similarity(X: Matrix, Y: Matrix) -> np.ndarray:
    if len(X) == 0 or len(Y) == 0:
        return np.array([])
    X = np.asarray(X)
    Y = np.asarray(Y)
    if X.shape[1] != Y.shape[1]:
        raise ValueError(
            f"Number of columns in X and Y must be the same. X has shape {X.shape} "
            f"and Y has shape {Y.shape}."
        )
    X_norm = np.linalg.norm(X, axis=1)
    Y_norm = np.linalg.norm(Y, axis=1)
    # Compute dot products and outer product more efficiently with np.einsum
    dot = X @ Y.T
    norm_product = np.outer(X_norm, Y_norm)

    # Avoid division by zero: mask where norm_product == 0
    nonzero = norm_product != 0
    similarity = np.zeros_like(dot)
    similarity[nonzero] = dot[nonzero] / norm_product[nonzero]
    # Set similarity to zero where norms are zero (including inf/nan from division)
    # This avoids need for np.isnan / np.isinf (eliminate second pass over data)
    return similarity


def cosine_similarity_top_k(
    X: Matrix,
    Y: Matrix,
    top_k: Optional[int] = 5,
    score_threshold: Optional[float] = None,
) -> Tuple[List[Tuple[int, int]], List[float]]:
    if len(X) == 0 or len(Y) == 0:
        return [], []
    score_array = cosine_similarity(X, Y)
    sorted_idxs = score_array.flatten().argsort()[::-1]
    top_k = top_k or len(sorted_idxs)
    top_idxs = sorted_idxs[:top_k]
    score_threshold = score_threshold or -1.0
    top_idxs = top_idxs[score_array.flatten()[top_idxs] > score_threshold]
    ret_idxs = [(x // score_array.shape[1], x % score_array.shape[1]) for x in top_idxs]
    scores = score_array.flatten()[top_idxs].tolist()
    return ret_idxs, scores
