import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import argparse
import sympy as sp
from pso import PSO
from objective_functions import create_random_objective, default_objective, default_function_expression
import os

def wrap_text(text, max_width=40):
    """Wraps text to a maximum width by inserting newline characters."""
    lines = []
    current_line = ""
    for word in text.split():
        if len(current_line) + len(word) + 1 <= max_width:
            current_line += (" " + word) if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Particle Swarm Optimization Visualization")
    parser.add_argument("--3d", action="store_true", help="Visualize in 3D")
    parser.add_argument("--function", type=str, help="Mathematical expression for Z=f(x,y) (e.g., 'sin(x) + cos(y)')")
    parser.add_argument("--random", action="store_true", help="Use a randomly generated objective function")
    parser.add_argument("--save", action="store_true", help="Save the animation")
    parser.add_argument("--save_path", type=str, default="examples", help="Path to save the animation (default: examples)")
    args = parser.parse_args()

    if args.random:
        objective_function, function_expr_str = create_random_objective()
        function_expr_str = wrap_text(function_expr_str)
    elif args.function:
        try:
            x_sym, y_sym = sp.symbols('x y')
            expr = sp.sympify(args.function)
            objective_function = sp.lambdify((x_sym, y_sym), expr, 'numpy')
            function_expr_str = wrap_text(args.function)
        except Exception as e:
            print(f"Error parsing function: {e}")
            print("Falling back to default objective function.")
            objective_function = default_objective
            function_expr_str = wrap_text(default_function_expression)
    else:
        objective_function = default_objective
        function_expr_str = wrap_text(default_function_expression)

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
        particles, = ax.plot(pso.pos[:, 0], pso.pos[:, 1], z_values, 'o', color="red", markersize=7, label='Particles')

        # Find the minimum point for 3D
        min_idx = np.unravel_index(np.argmin(Z), Z.shape)
        min_x = X[min_idx]
        min_y = Y[min_idx]
        min_z = Z[min_idx]
        minimum_point, = ax.plot([min_x], [min_y], [min_z], marker='o', markersize=10, color='lime', markeredgecolor='black', label='Global Minimum')

        def update(frame):
            positions = pso.update()
            z_values = objective_function(positions[:, 0], positions[:, 1])
            particles.set_data(positions[:, 0], positions[:, 1])
            particles.set_3d_properties(z_values)
            return particles,

        ani = animation.FuncAnimation(fig, update, frames=100, interval=20, blit=False)  
        ax.legend(fontsize=12)
        plt.title(f"Particle Swarm Optimization (3D)\nFunction: {function_expr_str}", fontsize=12)

        if args.save:
            os.makedirs(args.save_path, exist_ok=True)
            filename = os.path.join(args.save_path, f"pso_3d_animation.gif")
            # Ensure tight layout before saving
            fig.tight_layout()
            ani.save(filename, writer='PillowWriter', fps=60) 
            print(f"3D animation saved to {filename}")
        else:
            plt.tight_layout()

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

        particles, = ax.plot(pso.pos[:, 0], pso.pos[:, 1], 'o', color="red", markersize=7, label='Particles')

        # Find the minimum point for 2D
        min_idx = np.unravel_index(np.argmin(Z), Z.shape)
        min_x = X[min_idx]
        min_y = Y[min_idx]
        minimum_circle = plt.Circle((min_x, min_y), 0.1, color='lime', fill=False, linewidth=2, label='Global Minimum')
        ax.add_patch(minimum_circle)

        def update(frame):
            positions = pso.update()
            particles.set_data(positions[:, 0], positions[:, 1])
            return particles,

        ani = animation.FuncAnimation(fig, update, frames=100, interval=20, blit=True)  
        ax.legend(fontsize=12)
        plt.title(f"Particle Swarm Optimization (2D)\nFunction: {function_expr_str}", fontsize=12)

        if args.save:
            os.makedirs(args.save_path, exist_ok=True)
            filename = os.path.join(args.save_path, f"pso_2d_animation.gif")
            fig.tight_layout()
            ani.save(filename, writer='PillowWriter', fps=60) 
            print(f"2D animation saved to {filename}")
        else:
             plt.tight_layout()

    plt.show()