import numpy as np


def kmeans_clustering(
    X: np.ndarray, k: int, max_iter: int = 100
) -> tuple[np.ndarray, np.ndarray]:
    n_samples = X.shape[0]
    centroid_indices = np.random.choice(n_samples, k, replace=False)
    centroids = X[centroid_indices]
    for _ in range(max_iter):
        differences = X[:, np.newaxis, :] - centroids[np.newaxis, :, :]
        distances = np.linalg.norm(differences, axis=2)
        labels = np.argmin(distances, axis=1)
        new_centroids = np.zeros_like(centroids)
        for j in range(k):
            mask = labels == j
            if np.any(mask):
                new_centroids[j] = X[mask].mean(axis=0)
        if np.array_equal(centroids, new_centroids):
            break
        centroids = new_centroids
    return centroids, labels
