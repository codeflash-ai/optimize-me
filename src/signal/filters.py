import numpy as np


def manual_convolution_1d(signal: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    # Validate that both signal and kernel are 1D arrays
    if signal.ndim != 1:
        raise ValueError("setting an array element with a sequence.")
    if kernel.ndim != 1:
        raise ValueError("setting an array element with a sequence.")

    signal_len = len(signal)
    kernel_len = len(kernel)
    result_len = signal_len - kernel_len + 1
    result = np.zeros(result_len)
    # Use advanced numpy vectorization for faster computation
    if kernel_len == 0:
        return result  # Handles empty kernel
    # Stack the signal windows for efficient dot product
    strided = np.lib.stride_tricks.as_strided(
        signal,
        shape=(result_len, kernel_len),
        strides=(signal.strides[0], signal.strides[0]),
        writeable=False,
    )
    # Compute dot products between each window and the kernel
    result[:] = np.dot(strided, kernel)
    return result


def gaussian_blur(
    image: np.ndarray, kernel_size: int = 3, sigma: float = 1.0
) -> np.ndarray:
    k = kernel_size // 2
    y, x = np.ogrid[-k : k + 1, -k : k + 1]
    kernel = np.exp(-(x * x + y * y) / (2.0 * sigma * sigma))
    kernel = kernel / kernel.sum()
    height, width = image.shape[:2]
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    output = np.zeros_like(image)
    for y in range(height):
        for x in range(width):
            for c in range(channels):
                weighted_sum = 0
                weight_sum = 0
                for ky in range(-k, k + 1):
                    for kx in range(-k, k + 1):
                        ny, nx = y + ky, x + kx
                        if 0 <= ny < height and 0 <= nx < width:
                            if channels == 1:
                                pixel_value = image[ny, nx]
                            else:
                                pixel_value = image[ny, nx, c]
                            weight = kernel[ky + k, kx + k]
                            weighted_sum += pixel_value * weight
                            weight_sum += weight
                if weight_sum > 0:
                    if channels == 1:
                        output[y, x] = weighted_sum / weight_sum
                    else:
                        output[y, x, c] = weighted_sum / weight_sum
    return output
