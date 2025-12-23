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
    for y in range(new_height):
        for x in range(new_width):
            offset_y = y - new_center_y
            offset_x = x - new_center_x
            original_y = int(offset_y * cos_theta - offset_x * sin_theta + center_y)
            original_x = int(offset_y * sin_theta + offset_x * cos_theta + center_x)
            if 0 <= original_y < height and 0 <= original_x < width:
                rotated[y, x] = image[original_y, original_x]
    return rotated


def histogram_equalization(image: np.ndarray) -> np.ndarray:
    height, width = image.shape
    total_pixels = height * width

    # Use bincount but ensure we only count values 0-255
    # This maintains the IndexError behavior for out-of-range values
    image_flat = image.ravel()
    if image_flat.size > 0 and (image_flat.max() >= 256 or image_flat.min() < 0):
        # Trigger the same IndexError as original code
        _ = np.zeros(256, dtype=int)[image_flat.max()]

    histogram = np.bincount(image_flat, minlength=256)[:256]

    # Build CDF exactly as original to match floating-point behavior
    cdf = np.zeros(256, dtype=float)
    cdf[0] = histogram[0] / total_pixels
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + histogram[i] / total_pixels

    mapping = np.round(cdf * 255).astype(image.dtype)
    equalized = mapping[image]
    return equalized
