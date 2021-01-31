import numpy as np

def resize_and_fix_origin(kernel, size):
    pad0, pad1 = size[0]-kernel.shape[0], size[1]-kernel.shape[1]
    shift0, shift1 = (kernel.shape[0]-1)//2, (kernel.shape[1]-1)//2

    kernel = np.pad(kernel, ((0,pad0), (0,pad1)))
    kernel = np.roll(kernel, (-shift0, -shift1), axis=(0,1))
    return kernel

def gaussian_kernel(sigma, n):
    """
    Returns a n-by-n gaussian kernel (point spread function) with scale sigma,
    centered when shift=False
    """
    indices = np.linspace(-n/2, n/2, n)
    [X,Y] = np.meshgrid(indices, indices)

    h = np.exp(-(X**2+Y**2) / (2.0*(sigma)**2))
    h /= h.sum() # Normalize

    return h

def convolve(image, kernel_fft):
    image_fft = np.fft.fftshift(np.fft.fft2(image))

    result_fft = np.multiply(image_fft, kernel_fft)
    result = np.fft.ifft2(np.fft.fftshift(result_fft))

    return np.real(result)
