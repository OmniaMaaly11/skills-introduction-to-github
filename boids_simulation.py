import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Simulation parameters
WIDTH = 200
HEIGHT = 200
NUM_BOIDS = 20
MAX_SPEED = 5
SEPARATION_RADIUS = 25
ALIGNMENT_RADIUS = 50
COHESION_RADIUS = 50
SEPARATION_WEIGHT = 1.5
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 1.0

class Boid:
    def __init__(self):
        self.pos = np.random.rand(2) * np.array([WIDTH, HEIGHT])
        self.vel = (np.random.rand(2) - 0.5) * 10

    def separation(self, boids):
        steer = np.zeros(2)
        count = 0
        for b in boids:
            if b != self:
                dist = np.linalg.norm(self.pos - b.pos)
                if dist < SEPARATION_RADIUS:
                    steer += (self.pos - b.pos) / dist
                    count += 1
        if count > 0:
            steer /= count
            steer = steer / np.linalg.norm(steer) * MAX_SPEED - self.vel
            steer = np.clip(steer, -0.5, 0.5)
        return steer * SEPARATION_WEIGHT

    def alignment(self, boids):
        avg_vel = np.zeros(2)
        count = 0
        for b in boids:
            if b != self:
                dist = np.linalg.norm(self.pos - b.pos)
                if dist < ALIGNMENT_RADIUS:
                    avg_vel += b.vel
                    count += 1
        if count > 0:
            avg_vel /= count
            steer = avg_vel - self.vel
            steer = np.clip(steer, -0.5, 0.5)
        else:
            steer = np.zeros(2)
        return steer * ALIGNMENT_WEIGHT

    def cohesion(self, boids):
        center = np.zeros(2)
        count = 0
        for b in boids:
            if b != self:
                dist = np.linalg.norm(self.pos - b.pos)
                if dist < COHESION_RADIUS:
                    center += b.pos
                    count += 1
        if count > 0:
            center /= count
            desired = center - self.pos
            dist = np.linalg.norm(desired)
            if dist > 0:
                desired = desired / dist * MAX_SPEED
            steer = desired - self.vel
            steer = np.clip(steer, -0.5, 0.5)
        else:
            steer = np.zeros(2)
        return steer * COHESION_WEIGHT

    def update(self, boids):
        sep = self.separation(boids)
        ali = self.alignment(boids)
        coh = self.cohesion(boids)
        self.vel += sep + ali + coh
        speed = np.linalg.norm(self.vel)
        if speed > MAX_SPEED:
            self.vel = self.vel / speed * MAX_SPEED
        self.pos += self.vel
        # Wrap around boundaries
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT

# Initialize boids
boids = [Boid() for _ in range(NUM_BOIDS)]

# Visualization
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, WIDTH)
ax.set_ylim(0, HEIGHT)
ax.set_aspect('equal')

def animate(frame):
    ax.clear()
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect('equal')
    for b in boids:
        b.update(boids)
        # Draw boid as a small circle
        ax.scatter(b.pos[0], b.pos[1], c='blue', s=10)
        # Draw velocity vector as arrow
        ax.arrow(b.pos[0], b.pos[1], b.vel[0], b.vel[1], head_width=2, head_length=2, fc='red', ec='red', alpha=0.5)

ani = FuncAnimation(fig, animate, frames=200, interval=50, blit=False)
plt.title('Boids Flocking Simulation')
plt.show()