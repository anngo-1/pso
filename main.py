
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import argparse
import sympy as sp
from pso import PSO
from objective_functions import create_random_objective, default_objective, default_function_expression

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Particle Swarm Optimization Visualization")
    parser.add_argument("--3d", action="store_true", help="Visualize in 3D")
    parser.add_argument("--function", type=str, help="Mathematical expression for Z=f(x,y) (e.g., 'sin(x) + cos(y)')")
    parser.add_argument("--random", action="store_true", help="Use a randomly generated objective function")
    args = parser.parse_args()

    if args.random:
        objective_function, function_expr_str = create_random_objective()
    elif args.function:
        try:
            x_sym, y_sym = sp.symbols('x y')
            expr = sp.sympify(args.function)
            objective_function = sp.lambdify((x_sym, y_sym), expr, 'numpy')
            function_expr_str = args.function
        except Exception as e:
            print(f"Error parsing function: {e}")
            print("Falling back to default objective function.")
            objective_function = default_objective
            function_expr_str = default_function_expression
    else:
        objective_function = default_objective
        function_expr_str = default_function_expression

    pso = PSO(objective_function)

    if args.__dict__.get('3d', False):
        # 3D Visualization
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        Z = objective_function(X, Y)

        ax.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.6)
        ax.set_xlim([-3, 3])
        ax.set_ylim([-3, 3])
        ax.set_zlim([np.min(Z), np.max(Z)])
        ax.set_xlabel('X', fontsize=14)
        ax.set_ylabel('Y', fontsize=14)
        ax.set_zlabel('Z', fontsize=14)

        z_values = objective_function(pso.pos[:, 0], pso.pos[:, 1])
        particles, = ax.plot(pso.pos[:, 0], pso.pos[:, 1], z_values, 'o', color="red", markersize=7)

        def update(frame):
            positions = pso.update()
            z_values = objective_function(positions[:, 0], positions[:, 1])
            particles.set_data(positions[:, 0], positions[:, 1])
            particles.set_3d_properties(z_values)
            return particles,

        ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=False)
        plt.title(f"Particle Swarm Optimization (3D)\nFunction: {function_expr_str}", fontsize=14)
    else:
        # 2D Visualization
        fig, ax = plt.subplots(figsize=(10, 8))

        x = np.linspace(-3, 3, 200)
        y = np.linspace(-3, 3, 200)
        X, Y = np.meshgrid(x, y)
        Z = objective_function(X, Y)

        levels = np.linspace(np.min(Z), np.max(Z), 50)
        contour = ax.contourf(X, Y, Z, levels=levels, cmap=cm.viridis)
        cbar = fig.colorbar(contour, shrink=0.8, aspect=20)
        cbar.ax.tick_params(labelsize=12)
        ax.set_xlim([-3, 3])
        ax.set_ylim([-3, 3])
        ax.set_xlabel('X', fontsize=14)
        ax.set_ylabel('Y', fontsize=14)

        particles, = ax.plot(pso.pos[:, 0], pso.pos[:, 1], 'o', color="red", markersize=7)

        def update(frame):
            positions = pso.update()
            particles.set_data(positions[:, 0], positions[:, 1])
            return particles,

        ani = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)
        plt.title(f"Particle Swarm Optimization (2D)\nFunction: {function_expr_str}", fontsize=14)

    plt.tight_layout()
    plt.show()