import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G = 1.0
m1 = 1.0
m2 = 1.0

dt = 0.1


r1 = np.array([-0.5, 0.0])
r2 = np.array([ 0.5, 0.0])

v1 = np.array([0.0,  0.6])
v2 = np.array([0.0, -0.6])

fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

p1, = ax.plot([], [], 'bo', ms=8)
p2, = ax.plot([], [], 'ro', ms=8)

trail1, = ax.plot([], [], 'b-', lw=1, alpha=0.5)
trail2, = ax.plot([], [], 'r-', lw=1, alpha=0.5)

r1_hist = []
r2_hist = []

def update(frame):
    global r1, r2, v1, v2

    r = r2 - r1
    dist = np.linalg.norm(r)

    force = G * m1 * m2 * r / dist**3

    a1 =  force / m1
    a2 = -force / m2

    v1 += a1 * dt
    v2 += a2 * dt

    r1 += v1 * dt
    r2 += v2 * dt

    r1_hist.append(r1.copy())
    r2_hist.append(r2.copy())

    p1.set_data([r1[0]], [r1[1]])
    p2.set_data([r2[0]], [r2[1]])

    trail1.set_data(np.array(r1_hist)[:,0], np.array(r1_hist)[:,1])
    trail2.set_data(np.array(r2_hist)[:,0], np.array(r2_hist)[:,1])

    return p1, p2, trail1, trail2

ani = FuncAnimation(fig, update, frames=20000, interval=20)
plt.show()
