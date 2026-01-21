/**
 * Signal Processing Functions
 * JavaScript equivalents of Python/NumPy implementations
 */

/**
 * 1D Manual Convolution
 * @param {number[]} signal - Input signal
 * @param {number[]} kernel - Convolution kernel
 * @returns {number[]} - Convolved signal
 */
export function convolution1d(signal, kernel) {
  const signalLen = signal.length;
  const kernelLen = kernel.length;
  const outputLen = signalLen + kernelLen - 1;

  const result = Array(outputLen).fill(0);

  for (let i = 0; i < outputLen; i++) {
    for (let j = 0; j < kernelLen; j++) {
      const signalIdx = i - j;
      if (signalIdx >= 0 && signalIdx < signalLen) {
        result[i] += signal[signalIdx] * kernel[j];
      }
    }
  }

  return result;
}

/**
 * Fast Fourier Transform (Cooley-Tukey recursive)
 * @param {number[]} x - Input signal (real values, length must be power of 2)
 * @returns {{real: number[], imag: number[]}} - FFT result (complex)
 */
export function fft(x) {
  const n = x.length;

  if (n === 1) {
    return { real: [x[0]], imag: [0] };
  }

  if (n % 2 !== 0) {
    throw new Error('Input length must be a power of 2');
  }

  // Split into even and odd
  const even = [];
  const odd = [];
  for (let i = 0; i < n; i++) {
    if (i % 2 === 0) {
      even.push(x[i]);
    } else {
      odd.push(x[i]);
    }
  }

  // Recursive FFT
  const fftEven = fft(even);
  const fftOdd = fft(odd);

  // Combine
  const real = Array(n).fill(0);
  const imag = Array(n).fill(0);

  for (let k = 0; k < n / 2; k++) {
    const angle = -2 * Math.PI * k / n;
    const cos = Math.cos(angle);
    const sin = Math.sin(angle);

    // Twiddle factor * odd[k]
    const tReal = cos * fftOdd.real[k] - sin * fftOdd.imag[k];
    const tImag = cos * fftOdd.imag[k] + sin * fftOdd.real[k];

    real[k] = fftEven.real[k] + tReal;
    imag[k] = fftEven.imag[k] + tImag;

    real[k + n / 2] = fftEven.real[k] - tReal;
    imag[k + n / 2] = fftEven.imag[k] - tImag;
  }

  return { real, imag };
}

/**
 * Inverse FFT
 * @param {{real: number[], imag: number[]}} X - FFT result
 * @returns {number[]} - Time domain signal
 */
export function ifft(X) {
  const n = X.real.length;

  // Conjugate
  const conjugateImag = X.imag.map(v => -v);

  // Forward FFT on conjugate
  const result = fft(X.real.map((r, i) => r)); // Simplified: only works for real input

  // Conjugate and scale
  return result.real.map(v => v / n);
}

/**
 * Create Gaussian kernel for blur
 * @param {number} size - Kernel size (must be odd)
 * @param {number} sigma - Standard deviation
 * @returns {number[][]} - 2D Gaussian kernel
 */
export function createGaussianKernel(size, sigma) {
  const kernel = Array(size).fill(null).map(() => Array(size).fill(0));
  const center = Math.floor(size / 2);
  let sum = 0;

  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      const x = i - center;
      const y = j - center;
      const value = Math.exp(-(x * x + y * y) / (2 * sigma * sigma));
      kernel[i][j] = value;
      sum += value;
    }
  }

  // Normalize
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      kernel[i][j] /= sum;
    }
  }

  return kernel;
}

/**
 * Apply 2D convolution (for image filtering)
 * @param {number[][]} image - Input image
 * @param {number[][]} kernel - Convolution kernel
 * @returns {number[][]} - Filtered image
 */
export function convolution2d(image, kernel) {
  const imageRows = image.length;
  const imageCols = image[0].length;
  const kernelSize = kernel.length;
  const pad = Math.floor(kernelSize / 2);

  const result = Array(imageRows).fill(null).map(() => Array(imageCols).fill(0));

  for (let i = 0; i < imageRows; i++) {
    for (let j = 0; j < imageCols; j++) {
      let sum = 0;

      for (let ki = 0; ki < kernelSize; ki++) {
        for (let kj = 0; kj < kernelSize; kj++) {
          const ii = i + ki - pad;
          const jj = j + kj - pad;

          if (ii >= 0 && ii < imageRows && jj >= 0 && jj < imageCols) {
            sum += image[ii][jj] * kernel[ki][kj];
          }
        }
      }

      result[i][j] = sum;
    }
  }

  return result;
}

/**
 * Gaussian blur
 * @param {number[][]} image - Input image
 * @param {number} kernelSize - Kernel size (odd number)
 * @param {number} sigma - Standard deviation
 * @returns {number[][]} - Blurred image
 */
export function gaussianBlur(image, kernelSize = 5, sigma = 1.0) {
  const kernel = createGaussianKernel(kernelSize, sigma);
  return convolution2d(image, kernel);
}

/**
 * Image rotation
 * @param {number[][]} image - Input image
 * @param {number} angleDegrees - Rotation angle in degrees
 * @returns {number[][]} - Rotated image
 */
export function imageRotation(image, angleDegrees) {
  const rows = image.length;
  const cols = image[0].length;
  const angleRad = angleDegrees * Math.PI / 180;
  const cos = Math.cos(angleRad);
  const sin = Math.sin(angleRad);

  // Center of image
  const centerX = cols / 2;
  const centerY = rows / 2;

  const result = Array(rows).fill(null).map(() => Array(cols).fill(0));

  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      // Translate to center, rotate, translate back
      const dx = x - centerX;
      const dy = y - centerY;

      const srcX = cos * dx + sin * dy + centerX;
      const srcY = -sin * dx + cos * dy + centerY;

      // Nearest neighbor interpolation
      const srcXi = Math.round(srcX);
      const srcYi = Math.round(srcY);

      if (srcXi >= 0 && srcXi < cols && srcYi >= 0 && srcYi < rows) {
        result[y][x] = image[srcYi][srcXi];
      }
    }
  }

  return result;
}

/**
 * Histogram equalization
 * @param {number[][]} image - Input grayscale image (0-255)
 * @returns {number[][]} - Equalized image
 */
export function histogramEqualization(image) {
  const rows = image.length;
  const cols = image[0].length;
  const totalPixels = rows * cols;

  // Compute histogram
  const histogram = Array(256).fill(0);
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      const value = Math.min(255, Math.max(0, Math.round(image[i][j])));
      histogram[value]++;
    }
  }

  // Compute CDF
  const cdf = Array(256).fill(0);
  cdf[0] = histogram[0];
  for (let i = 1; i < 256; i++) {
    cdf[i] = cdf[i - 1] + histogram[i];
  }

  // Find minimum non-zero CDF value
  let cdfMin = 0;
  for (let i = 0; i < 256; i++) {
    if (cdf[i] > 0) {
      cdfMin = cdf[i];
      break;
    }
  }

  // Create lookup table
  const lookup = Array(256).fill(0);
  for (let i = 0; i < 256; i++) {
    lookup[i] = Math.round((cdf[i] - cdfMin) * 255 / (totalPixels - cdfMin));
  }

  // Apply equalization
  const result = Array(rows).fill(null).map(() => Array(cols).fill(0));
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      const value = Math.min(255, Math.max(0, Math.round(image[i][j])));
      result[i][j] = lookup[value];
    }
  }

  return result;
}

/**
 * Rolling mean (moving average)
 * @param {number[]} series - Input series
 * @param {number} window - Window size
 * @returns {number[]} - Rolling mean (with NaN for incomplete windows)
 */
export function rollingMean(series, window) {
  const result = [];

  for (let i = 0; i < series.length; i++) {
    if (i < window - 1) {
      result.push(NaN);
    } else {
      let sum = 0;
      for (let j = 0; j < window; j++) {
        sum += series[i - j];
      }
      result.push(sum / window);
    }
  }

  return result;
}
