import numpy as np


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

    if new_height == 0 or new_width == 0:
        return rotated

    ys = np.arange(new_height, dtype=float)[:, None] - new_center_y
    xs = np.arange(new_width, dtype=float)[None, :] - new_center_x

    original_yf = ys * cos_theta - xs * sin_theta + center_y
    original_xf = ys * sin_theta + xs * cos_theta + center_x

    original_y = original_yf.astype(int)
    original_x = original_xf.astype(int)

    valid_mask = (
        (original_y >= 0)
        & (original_y < height)
        & (original_x >= 0)
        & (original_x < width)
    )

    # Single assignment works for both grayscale and color images:
    rotated[valid_mask] = image[original_y[valid_mask], original_x[valid_mask]]

    return rotated


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
