import numpy as np

def gaussian(x, y, x0, y0, sigma):
    return np.exp(-((x - x0) ** 2 + (y - y0) ** 2) / (2 * sigma ** 2))

def create_random_objective(num_peaks=4):
    x0s = np.random.uniform(-2, 2, num_peaks)
    y0s = np.random.uniform(-2, 2, num_peaks)
    sigmas = np.random.uniform(0.5, 1.5, num_peaks)
    amplitudes = np.random.uniform(1, 3, num_peaks)

    terms = [
        f"{amplitude:.2f} * exp(-((x - {x0:.2f})^2 + (y - {y0:.2f})^2) / (2 * {sigma:.2f}^2))"
        for x0, y0, sigma, amplitude in zip(x0s, y0s, sigmas, amplitudes)
    ]
    ripples_expr = "+ 0.3 * sin(2 * x + y) + 0.2 * cos(x - 2 * y)"
    function_expression = " + ".join(terms) + " " + ripples_expr

    def random_objective(x, y):
        x = np.asarray(x)
        y = np.asarray(y)
        x_flat = x.ravel()[:, np.newaxis]
        y_flat = y.ravel()[:, np.newaxis]
        exponent = -((x_flat - x0s) ** 2 + (y_flat - y0s) ** 2) / (2 * sigmas ** 2)
        gaussians = amplitudes * np.exp(exponent)
        z = np.sum(gaussians, axis=1)
        ripples = 0.3 * np.sin(2 * x_flat[:, 0] + y_flat[:, 0]) + 0.2 * np.cos(x_flat[:, 0] - 2 * y_flat[:, 0])
        total = z + ripples
        return total.reshape(x.shape)

    return random_objective, function_expression

def default_objective(x, y):
    x0s = np.array([1, -1.5, -1, 1.5])
    y0s = np.array([1, -1, 1.5, -1.5])
    sigmas = np.array([1.5, 1.0, 0.8, 1.2])
    amplitudes = np.array([3, 2, 1.5, 1])

    x = np.asarray(x)
    y = np.asarray(y)
    x_flat = x.ravel()[:, np.newaxis]
    y_flat = y.ravel()[:, np.newaxis]
    exponent = -((x_flat - x0s) ** 2 + (y_flat - y0s) ** 2) / (2 * sigmas ** 2)
    gaussians = amplitudes * np.exp(exponent)
    z = np.sum(gaussians, axis=1)
    ripples = 0.3 * np.sin(2 * x_flat[:, 0] + y_flat[:, 0]) + 0.2 * np.cos(x_flat[:, 0] - 2 * y_flat[:, 0])
    total = z + ripples
    return total.reshape(x.shape)

default_function_expression = (
    "3 * exp(-((x - 1)^2 + (y - 1)^2)/(2 * 1.5^2)) + "
    "2 * exp(-((x + 1.5)^2 + (y + 1)^2)/(2 * 1^2)) + "
    "1.5 * exp(-((x + 1)^2 + (y - 1.5)^2)/(2 * 0.8^2)) + "
    "exp(-((x - 1.5)^2 + (y + 1.5)^2)/(2 * 1.2^2)) + "
    "0.3 * sin(2 * x + y) + 0.2 * cos(x - 2 * y)"
)