import numpy as np


def manual_convolution_1d(signal: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    signal_len = len(signal)
    kernel_len = len(kernel)
    result_len = signal_len - kernel_len + 1

    # Preserve original behavior for negative/zero lengths and empty kernel
    if result_len < 0:
        return np.zeros(result_len)
    if result_len == 0:
        return np.zeros(0)
    if kernel_len == 0:
        return np.zeros(result_len)

    # Use NumPy's optimized correlate to compute the same inner sum efficiently
    signal = np.asarray(signal)
    kernel = np.asarray(kernel)
    result = np.correlate(signal, kernel, mode="valid").astype(np.float64, copy=False)
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
