import numpy as np


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
