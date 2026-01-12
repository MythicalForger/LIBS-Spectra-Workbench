def pixel_to_wavelength(pixel, a, b):
    """
    Convert pixel index to wavelength using calibrated parameters.
    """
    return a * pixel + b
