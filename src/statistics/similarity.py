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

    # Avoid explicit creation of outer product and broadcasting division,
    # instead use manual vector-wise normalization to save memory
    # (normalize X and Y rows before matrix multiplication when feasible)
    nonzero_X = X_norm != 0
    nonzero_Y = Y_norm != 0
    X_safe = X.astype(np.float64, copy=False)
    Y_safe = Y.astype(np.float64, copy=False)
    # Precompute normed variants only for valid rows
    X_normed = np.zeros_like(X_safe, dtype=np.float64)
    Y_normed = np.zeros_like(Y_safe, dtype=np.float64)
    X_normed[nonzero_X] = X_safe[nonzero_X] / X_norm[nonzero_X, None]
    Y_normed[nonzero_Y] = Y_safe[nonzero_Y] / Y_norm[nonzero_Y, None]
    similarity = np.dot(X_normed, Y_normed.T)
    # Explicitly set similarities to zero for rows with small norm
    if not np.all(nonzero_X) or not np.all(nonzero_Y):
        mask_X = ~nonzero_X
        mask_Y = ~nonzero_Y
        if np.any(mask_X):
            similarity[mask_X, :] = 0.0
        if np.any(mask_Y):
            similarity[:, mask_Y] = 0.0

    # Clean up any remaining nan/inf (highly unlikely after this normalization)
    np.nan_to_num(similarity, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
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
