
import numpy as np

class PSO:
    def __init__(self, objective_func, n_particles=50, v_max=0.3, bounds=(-3, 3)):
        self.objective_func = objective_func
        self.n_particles = n_particles
        self.bounds = bounds
        self.pos = np.random.uniform(bounds[0], bounds[1], (n_particles, 2))
        self.vel = np.random.uniform(-0.1, 0.1, (n_particles, 2))
        self.best_pos = self.pos.copy()
        self.best_scores = self._evaluate_objective(self.pos)
        self.global_best_pos = self.pos[np.argmin(self.best_scores)].copy()
        self.global_best_score = np.min(self.best_scores)
        self.iteration = 0
        self.v_max = v_max
        self.w_start = 0.9
        self.w_end = 0.4
        self.c1_start = 2.0
        self.c1_end = 1.0
        self.c2_start = 1.0
        self.c2_end = 2.0

    def _evaluate_objective(self, positions):
        return self.objective_func(positions[:, 0], positions[:, 1])

    def update(self, max_iterations=100):
        w = self.w_start - (self.w_start - self.w_end) * (
            self.iteration / max_iterations
        )
        c1 = self.c1_start - (self.c1_start - self.c1_end) * (
            self.iteration / max_iterations
        )
        c2 = self.c2_start + (self.c2_end - self.c2_start) * (
            self.iteration / max_iterations
        )

        r1 = np.random.rand(self.n_particles, 2)
        r2 = np.random.rand(self.n_particles, 2)

        cognitive = c1 * r1 * (self.best_pos - self.pos)
        social = c2 * r2 * (self.global_best_pos - self.pos)
        self.vel = w * self.vel + cognitive + social
        self.vel = np.clip(self.vel, -self.v_max, self.v_max)
        self.pos += self.vel
        self.pos = np.clip(self.pos, *self.bounds)

        scores = self._evaluate_objective(self.pos)
        better_mask = scores < self.best_scores
        self.best_pos[better_mask] = self.pos[better_mask]
        self.best_scores[better_mask] = scores[better_mask]

        current_best_idx = np.argmin(scores)
        if scores[current_best_idx] < self.global_best_score:
            self.global_best_pos = self.pos[current_best_idx].copy()
            self.global_best_score = scores[current_best_idx]

        self.iteration += 1
        return self.pos