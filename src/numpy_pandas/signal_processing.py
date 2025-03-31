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


def FFT(x: np.ndarray) -> np.ndarray:
    n = len(x)
    if n == 1:
        return x
    even = FFT(x[0::2])
    odd = FFT(x[1::2])
    factor = np.exp(-2j * np.pi * np.arange(n) / n)
    result = np.zeros(n, dtype=complex)
    half_n = n // 2
    for k in range(half_n):
        result[k] = even[k] + factor[k] * odd[k]
        result[k + half_n] = even[k] - factor[k] * odd[k]
    return result


def image_rotation(image: np.ndarray, angle_degrees: float) -> np.ndarray:
    angle_radians = np.radians(angle_degrees)
    cos_theta = np.cos(angle_radians)
    sin_theta = np.sin(angle_radians)
    height, width = image.shape[:2]
    center_y, center_x = height // 2, width // 2
    new_height = int(abs(height * cos_theta) + abs(width * sin_theta))
    new_width = int(abs(width * cos_theta) + abs(height * sin_theta))
    rotated = np.zeros(
        (new_height, new_width, image.shape[2])
        if len(image.shape) > 2
        else (new_height, new_width)
    )
    new_center_y, new_center_x = new_height // 2, new_width // 2
    for y in range(new_height):
        for x in range(new_width):
            offset_y = y - new_center_y
            offset_x = x - new_center_x
            original_y = int(offset_y * cos_theta - offset_x * sin_theta + center_y)
            original_x = int(offset_y * sin_theta + offset_x * cos_theta + center_x)
            if 0 <= original_y < height and 0 <= original_x < width:
                rotated[y, x] = image[original_y, original_x]
    return rotated


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


def histogram_equalization(image: np.ndarray) -> np.ndarray:
    height, width = image.shape
    total_pixels = height * width
    histogram = np.zeros(256, dtype=int)
    for y in range(height):
        for x in range(width):
            histogram[image[y, x]] += 1
    cdf = np.zeros(256, dtype=float)
    cdf[0] = histogram[0] / total_pixels
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + histogram[i] / total_pixels
    equalized = np.zeros_like(image)
    for y in range(height):
        for x in range(width):
            equalized[y, x] = np.round(cdf[image[y, x]] * 255)
    return equalized
