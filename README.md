# Particle Swarm Optimization (PSO) Visualization

This project interactively implements and visualizes the PSO algorithm optimizing functions of two variables. Observe particles swarm towards the global minimum on different functions in 2D or 3D.

## Examples

- **Default Example Objective Function in 3D:**

  ```bash
  python main.py --3d --save
  ```

  ![Default Function 3D PSO Animation](examples/pso_3d_default_animation.gif)

- **Custom Objective Function in 2D:**

  ```bash
  python main.py --function "sin(x**2) * cos(y)" --save
  ```

  ![Custom Function 2D PSO Animation](examples/pso_2d_custom_animation.gif)

- **Random Objective Function in 3D:**

  ```bash
  python main.py --random --3d --save
  ```

  ![Random 3D PSO Animation](examples/pso_3d_random_animation.gif)

## Introduction

Particle Swarm Optimization (PSO) is a population-based stochastic optimization technique inspired by the social behavior of bird flocking or fish schooling. It is a versatile algorithm capable of finding both the minimum and the maximum (the optima) of a function. Instead of directly searching for a maximum, PSO typically finds the minimum of a function. To find the maximum of a function using PSO, you would optimize the negative of that function, as finding the minimum of −f(x) will find the maximum of f(x).

## Features

- **Interactive Visualization**: Real-time particle swarming.
- **Custom Functions**: Optimize the default, your own, or random functions.
- **2D and 3D Modes**: Visualize with contour or surface plots.
- **Save Animations**: Save the generated visualizations as GIF files.

## Getting Started

### Prerequisites

Ensure you have Python 3 and these packages:

```bash
pip install numpy matplotlib sympy Pillow
```

### Running the Project

Clone and navigate to the project directory:

```bash
git clone https://github.com/anngo-1/pso.git
cd pso
```

Run the script:

```bash
python main.py
```

This runs the default visualization in 2D.

## Usage

Customize the script with command-line arguments:

- `--3d`: Enable 3D visualization.
- `--function FUNCTION`: Specify a Python expression for the function (e.g., `'sin(x) + cos(y)'`).
- `--random`: Use a randomly generated function.
- `--save`: Save the animation as a GIF file in the specified directory.
- `--save_path PATH`: Specify the directory to save the animation (default: `examples`).
## How It Works

### The PSO Algorithm

The Particle Swarm Optimization (PSO) algorithm in this project simulates particles moving within a two-dimensional search space. Each particle adjusts its movement based on two main factors:

*   **Its own best experience (cognitive component):**  The particle remembers the best position it has personally discovered so far.
*   **The swarm's collective experience (social component):** The particle is also influenced by the best position found by any particle in the entire swarm.

**Velocity Update Equation:**

The change in a particle's position (its velocity) is calculated at each step using the following logic:

The new velocity of particle `i` at the next time step (`t+1`) is determined by:

*   **Inertia:**  A fraction of its current velocity (`w` multiplied by the velocity of particle `i` at time `t`). This helps the particle maintain its direction.
*   **Cognitive Attraction:** A pull towards the particle's own best-found position (`c1` multiplied by a random number `r1` multiplied by the difference between the particle's best position `pi` and its current position at time `t`).
*   **Social Attraction:** A pull towards the swarm's overall best-found position (`c2` multiplied by a random number `r2` multiplied by the difference between the global best position `g` and the particle's current position at time `t`).

We can represent this mathematically as:

$$ velocity_i(t+1) = w \cdot velocity_i(t) + c_1 \cdot r_1 \cdot (personalbest_i - position_i(t)) + c_2 \cdot r_2 \cdot (globalbest - position_i(t)) $$

Where:

*   `velocity_i(t)`: The velocity of particle `i` at time `t`.
*   `w`: The inertia weight, controlling how much the particle retains its previous velocity.
*   `c1`, `c2`:  Acceleration coefficients that determine the strength of the pull towards the personal best and global best, respectively.
*   `r1`, `r2`: Random numbers between 0 and 1, adding a stochastic element to the movement.
*   `personalbest_i`: The best position found so far by particle `i`.
*   `globalbest`: The best position found so far by the entire swarm.
*   `position_i(t)`: The current position of particle `i` at time `t`.

**Position Update Equation:**

Once the new velocity is calculated, the particle's position is updated by simply adding the velocity to its current position:

$$ position_i(t+1) = position_i(t) + velocity_i(t+1) $$

These update rules guide the particles to explore the search space while also converging towards promising areas where better solutions have been found.

### Objective Functions

The objective function defines the "landscape" that the particles are navigating. The goal of the PSO is to find the lowest point (minimum) on this landscape.

#### Default Objective Function

We try to design the default objective function in this visualization to be complex, with multiple "hills" (local minima) to challenge the optimization algorithm. It's created by combining several Gaussian "peak" functions with some wave-like (sinusoidal) ripples.

The function can be described as:

$$ f(x, y) =  3 \cdot \exp\left(-\frac{(x - 1)^2 + (y - 1)^2}{2 \cdot 1.5^2}\right) + 2 \cdot \exp\left(-\frac{(x + 1.5)^2 + (y + 1)^2}{2 \cdot 1^2}\right) + 1.5 \cdot \exp\left(-\frac{(x + 1)^2 + (y - 1.5)^2}{2 \cdot 0.8^2}\right) + \exp\left(-\frac{(x - 1.5)^2 + (y + 1.5)^2}{2 \cdot 1.2^2}\right) + 0.3 \cdot \sin(2x + y) + 0.2 \cdot \cos(x - 2y) $$

There are two parts to this function:

*   **Gaussian Terms (the `exp(...)` parts):** These create the "hills". Each term represents a peak centered at a specific `(x, y)` coordinate. The numbers in the exponent control the width and shape of the peak, and the number multiplying the `exp` controls the height of the peak. For example, `3 * exp(-((x - 1)^2 + (y - 1)^2) / (2 * 1.5^2))` creates a tall, relatively wide peak centered around `x=1` and `y=1`.

*   **Sinusoidal Terms (the `sin(...)` and `cos(...)` parts):** These add ripples or waves to the landscape. `0.3 * sin(2x + y)` and `0.2 * cos(x - 2y)` and can create local minima, making the optimization problem more difficult.

#### Random Objective Function

To provide a different challenge each time, the visualization can also use a randomly generated objective function. This function is created by placing several Gaussian "peaks" at random locations with random heights and widths.

The general form of the random objective function is:

$$ f(x, y) = \sum_{k=1}^{N} \left( amplitude_k \cdot \exp\left(-\frac{(x - center_{x\_k})^2 + (y - center_{y\_k})^2}{2 \cdot width_k^2}\right) \right) + 0.3 \cdot \sin(2x + y) + 0.2 \cdot \cos(x - 2y) $$

Where:

*   `N`: The number of peaks (default is 4).
*   `amplitude_k`:  A random number determining the height of the k-th peak.
*   `center_{x\_k}`, `center_{y\_k}`: Random numbers determining the center coordinates of the k-th peak.
*   `width_k`: A random number determining the width of the k-th peak.

The sinusoidal terms are added to introduce further complexity, just like in the default function. Each time you run the visualization with the random objective, a new and unique landscape is generated.


## Code

### `main.py`

Entry point handling argument parsing, objective function setup, PSO initialization, visualization, and saving functionality.

### `pso.py`

Contains the `PSO` class implementing the algorithm, including initialization and the update method.

### `objective_functions.py`

Defines the default, random, and Gaussian helper functions.

## Customize and Experiment

Tweak parameters in `pso.py` or define new functions in `objective_functions.py`.

- **Change Number of Particles**: Adjust `n_particles`.
- **Adjust Coefficients**: Modify `c1` and `c2`.
- **Modify Inertia**: Experiment with `w`.
- **Define Functions**: Add your own in `objective_functions.py` or use the `--function` command-line argument.
- **Experiment with Bounds**: Change the search space limits within the `PSO` class initialization.
