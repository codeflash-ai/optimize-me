from typing import List, Optional, Tuple, Union

import numpy as np


Matrix = Union[List[List[float]], List[np.ndarray], np.ndarray]
Vector = Union[List[float], np.ndarray]


def cosine_similarity(X: Matrix, Y: Matrix) -> np.ndarray:
    if len(X) == 0 or len(Y) == 0:
        return np.array([])
    X = np.array(X)
    Y = np.array(Y)
    if X.shape[1] != Y.shape[1]:
        raise ValueError(
            f"Number of columns in X and Y must be the same. X has shape {X.shape} "
            f"and Y has shape {Y.shape}."
        )
    X_norm = np.linalg.norm(X, axis=1)
    Y_norm = np.linalg.norm(Y, axis=1)
    similarity = np.dot(X, Y.T) / np.outer(X_norm, Y_norm)
    similarity[np.isnan(similarity) | np.isinf(similarity)] = 0.0
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


def pca(X: np.ndarray, n_components: int = 2) -> tuple[np.ndarray, np.ndarray]:
    X_centered = X - np.mean(X, axis=0)
    cov_matrix = np.zeros((X.shape[1], X.shape[1]))
    for i in range(X.shape[1]):
        for j in range(X.shape[1]):
            for k in range(X.shape[0]):
                cov_matrix[i, j] += X_centered[k, i] * X_centered[k, j]
            cov_matrix[i, j] /= X.shape[0] - 1
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    components = eigenvectors[:, :n_components]
    X_transformed = np.zeros((X.shape[0], n_components))
    for i in range(X.shape[0]):
        for j in range(n_components):
            for k in range(X.shape[1]):
                X_transformed[i, j] += X_centered[i, k] * components[k, j]
    return X_transformed, components


def kmeans_clustering(
    X: np.ndarray, k: int, max_iter: int = 100
) -> tuple[np.ndarray, np.ndarray]:
    n_samples = X.shape[0]
    centroid_indices = np.random.choice(n_samples, k, replace=False)
    centroids = X[centroid_indices]
    for _ in range(max_iter):
        labels = np.zeros(n_samples, dtype=int)
        for i in range(n_samples):
            min_dist = float("inf")
            for j in range(k):
                dist = 0
                for feat in range(X.shape[1]):
                    dist += (X[i, feat] - centroids[j, feat]) ** 2
                dist = np.sqrt(dist)
                if dist < min_dist:
                    min_dist = dist
                    labels[i] = j
        new_centroids = np.zeros_like(centroids)
        counts = np.zeros(k)
        for i in range(n_samples):
            cluster = labels[i]
            counts[cluster] += 1
            for feat in range(X.shape[1]):
                new_centroids[cluster, feat] += X[i, feat]
        for j in range(k):
            if counts[j] > 0:
                for feat in range(X.shape[1]):
                    new_centroids[j, feat] /= counts[j]
        if np.array_equal(centroids, new_centroids):
            break
        centroids = new_centroids
    return centroids, labels


def singular_value_decomposition(
    A: np.ndarray, k: int = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    AAT = np.dot(A, A.T)
    ATA = np.dot(A.T, A)
    U_vals, U_vecs = np.linalg.eigh(AAT)
    V_vals, V_vecs = np.linalg.eigh(ATA)
    U_idx = U_vals.argsort()[::-1]
    U_vals, U_vecs = U_vals[U_idx], U_vecs[:, U_idx]
    V_idx = V_vals.argsort()[::-1]
    V_vals, V_vecs = V_vals[V_idx], V_vecs[:, V_idx]
    S = np.sqrt(U_vals)
    if k is not None:
        U_vecs = U_vecs[:, :k]
        S = S[:k]
        V_vecs = V_vecs[:, :k]
    return U_vecs, np.diag(S), V_vecs.T


def gradient_descent(
    X: np.ndarray, y: np.ndarray, learning_rate: float = 0.01, iterations: int = 1000
) -> np.ndarray:
    m, n = X.shape
    weights = np.zeros(n)
    for _ in range(iterations):
        predictions = np.zeros(m)
        for i in range(m):
            for j in range(n):
                predictions[i] += X[i, j] * weights[j]
        errors = predictions - y
        gradient = np.zeros(n)
        for j in range(n):
            for i in range(m):
                gradient[j] += errors[i] * X[i, j]
            gradient[j] /= m
        for j in range(n):
            weights[j] -= learning_rate * gradient[j]
    return weights
