import numpy as np


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
