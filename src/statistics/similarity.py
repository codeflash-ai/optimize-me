from typing import List, Optional, Tuple, Union

import numpy as np


Matrix = Union[List[List[float]], List[np.ndarray], np.ndarray]
Vector = Union[List[float], np.ndarray]


def cosine_similarity(X: Matrix, Y: Matrix) -> np.ndarray:
    if len(X) == 0 or len(Y) == 0:
        return np.array([])
    # Convert both X and Y to float arrays using np.asarray for possible efficiency and memory savings
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    if X.shape[1] != Y.shape[1]:
        raise ValueError(
            f"Number of columns in X and Y must be the same. X has shape {X.shape} "
            f"and Y has shape {Y.shape}."
        )
    # Use 'keepdims=True' to allow for later broadcasting, and avoid explicit outer product shape
    X_norm = np.linalg.norm(X, axis=1, keepdims=True)
    Y_norm = np.linalg.norm(Y, axis=1, keepdims=True)
    # Compute denominator directly for efficiency
    denom = X_norm @ Y_norm.T
    # Handle division by zero in-place to avoid NaNs/Infs
    with np.errstate(divide="ignore", invalid="ignore"):
        similarity = np.dot(X, Y.T) / denom
        np.copyto(similarity, 0.0, where=~np.isfinite(similarity))
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
    flat_scores = (
        score_array.flatten()
    )  # Use flatten() to match original behavior exactly
    sorted_idxs = flat_scores.argsort()[
        ::-1
    ]  # Use full argsort to match original ordering
    top_k = top_k or len(sorted_idxs)
    top_idxs = sorted_idxs[:top_k]
    score_threshold = score_threshold or -1.0
    top_idxs = top_idxs[flat_scores[top_idxs] > score_threshold]
    ret_idxs = [(x // score_array.shape[1], x % score_array.shape[1]) for x in top_idxs]
    scores = flat_scores[top_idxs].tolist()
    return ret_idxs, scores
