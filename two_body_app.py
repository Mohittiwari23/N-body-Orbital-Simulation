import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import streamlit as st

st.set_page_config(layout="wide")
st.title("Interactive Two-Body Gravitational Simulation")

# Sidebar inputs
st.sidebar.header("Initial Conditions")

G = st.sidebar.number_input("Gravitational Constant G", 0.01, 10.0, 1.0)

m1 = st.sidebar.number_input("Mass m1", 0.1, 10.0, 1.0)
m2 = st.sidebar.number_input("Mass m2", 0.1, 10.0, 1.0)

r1x = st.sidebar.number_input("r1 x", -2.0, 2.0, -0.5)
r1y = st.sidebar.number_input("r1 y", -2.0, 2.0,  0.0)

r2x = st.sidebar.number_input("r2 x", -2.0, 2.0,  0.5)
r2y = st.sidebar.number_input("r2 y", -2.0, 2.0,  0.0)

v1x = st.sidebar.number_input("v1 x", -2.0, 2.0, 0.0)
v1y = st.sidebar.number_input("v1 y", -2.0, 2.0, 0.6)

v2x = st.sidebar.number_input("v2 x", -2.0, 2.0, 0.0)
v2y = st.sidebar.number_input("v2 y", -2.0, 2.0, -0.6)

dt = st.sidebar.slider("Time Step", 0.001, 0.05, 0.01)

run = st.sidebar.button("Run Simulation")

if run:

    state = {
        "r1": np.array([r1x, r1y]),
        "r2": np.array([r2x, r2y]),
        "v1": np.array([v1x, v1y]),
        "v2": np.array([v2x, v2y]),
    }

    fig, ax = plt.subplots()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_title("Two Body Orbit")

    p1, = ax.plot([], [], 'bo', ms=8)
    p2, = ax.plot([], [], 'ro', ms=8)

    trail1, = ax.plot([], [], 'b-', lw=1, alpha=0.5)
    trail2, = ax.plot([], [], 'r-', lw=1, alpha=0.5)

    r1_hist, r2_hist = [], []

    def update(frame):

        r = state["r2"] - state["r1"]
        dist = np.linalg.norm(r) + 1e-6

        force = G * m1 * m2 * r / dist**3

        a1 =  force / m1
        a2 = -force / m2

        state["v1"] += a1 * dt
        state["v2"] += a2 * dt

        state["r1"] += state["v1"] * dt
        state["r2"] += state["v2"] * dt

        r1_hist.append(state["r1"].copy())
        r2_hist.append(state["r2"].copy())

        p1.set_data([state["r1"][0]], [state["r1"][1]])
        p2.set_data([state["r2"][0]], [state["r2"][1]])

        trail1.set_data(np.array(r1_hist)[:,0], np.array(r1_hist)[:,1])
        trail2.set_data(np.array(r2_hist)[:,0], np.array(r2_hist)[:,1])

        return p1, p2, trail1, trail2

    ani = FuncAnimation(fig, update, frames=1500, interval=20)

    st.pyplot(fig)
