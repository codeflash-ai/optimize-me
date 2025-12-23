import numpy as np


def manual_convolution_1d(signal: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    signal_len = len(signal)
    kernel_len = len(kernel)
    result_len = signal_len - kernel_len + 1
    result = np.zeros(result_len)
    for i in range(result_len):
        for j in range(kernel_len):
            result[i] += signal[i + j] * kernel[j]
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

    if channels == 1:
        for y0 in range(height):
            for x0 in range(width):
                weighted_sum = 0
                weight_sum = 0
                # Determine the valid kernel range for this pixel
                ky_start = max(0, k - y0)
                kx_start = max(0, k - x0)
                ky_end = min(kernel_size, kernel_size - (y0 + k + 1 - height))
                kx_end = min(kernel_size, kernel_size - (x0 + k + 1 - width))

                for ky in range(ky_start, ky_end):
                    for kx in range(kx_start, kx_end):
                        ny = y0 + ky - k
                        nx = x0 + kx - k
                        pixel_value = image[ny, nx]
                        weight = kernel[ky, kx]
                        weighted_sum += pixel_value * weight
                        weight_sum += weight

                if weight_sum > 0:
                    output[y0, x0] = weighted_sum / weight_sum
    else:
        for y0 in range(height):
            for x0 in range(width):
                # Determine the valid kernel range for this pixel
                ky_start = max(0, k - y0)
                kx_start = max(0, k - x0)
                ky_end = min(kernel_size, kernel_size - (y0 + k + 1 - height))
                kx_end = min(kernel_size, kernel_size - (x0 + k + 1 - width))

                for c in range(channels):
                    weighted_sum = 0
                    weight_sum = 0
                    for ky in range(ky_start, ky_end):
                        for kx in range(kx_start, kx_end):
                            ny = y0 + ky - k
                            nx = x0 + kx - k
                            pixel_value = image[ny, nx, c]
                            weight = kernel[ky, kx]
                            weighted_sum += pixel_value * weight
                            weight_sum += weight

                    if weight_sum > 0:
                        output[y0, x0, c] = weighted_sum / weight_sum

    return output
