import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time

st.set_page_config(layout="wide")
st.title("Two-Body Gravitational Simulation")

# -------- Controls --------

st.sidebar.header("Controls")

# Earth-Moon preset button
if st.sidebar.button("Earth-Moon", type="primary"):
    st.session_state.earth_moon_mode = True
else:
    if 'earth_moon_mode' not in st.session_state:
        st.session_state.earth_moon_mode = False

# Check if we're in Earth-Moon mode
if st.session_state.earth_moon_mode:
    # Earth-Moon specific parameters (locked)
    m1 = 81.3  # Earth mass (relative to Moon = 1)
    m2 = 1.0  # Moon mass

    st.sidebar.info("Earth-Moon")
    st.sidebar.write(f"Earth mass: {m1:.1f}")
    st.sidebar.write(f"Moon mass: {m2:.1f}")

    # Calculate the center of mass position
    # Place Earth slightly off-center, Moon farther out
    total_mass = m1 + m2

    # Real Earth-Moon distance is ~384,400 km
    # We'll scale this to fit our simulation window
    moon_distance = 1.5  # simulation units

    # Barycenter is inside the Earth (about 4,671 km from Earth's center)
    # Earth position relative to barycenter
    earth_offset = -moon_distance * m2 / total_mass
    moon_offset = moon_distance * m1 / total_mass

    r1 = np.array([earth_offset, 0.0])
    r2 = np.array([moon_offset, 0.0])

    # Orbital velocity calculation for circular orbit
    # v = sqrt(G * M / r) for each body around barycenter
    r_earth = abs(earth_offset)
    r_moon = abs(moon_offset)

    # Reduced mass calculation for proper orbital mechanics
    mu = G = 1.0  # Gravitational constant

    # Circular orbit velocity
    v_orbital = np.sqrt(G * total_mass / moon_distance)

    # Velocities (perpendicular to position, scaled by distance from barycenter)
    v1 = np.array([0.0, v_orbital * m2 / total_mass])
    v2 = np.array([0.0, -v_orbital * m1 / total_mass])

else:
    # Manual mode - user controls
    m1 = st.sidebar.slider("Mass Body 1 (blue)", 0.5, 5.0, 1.0)
    m2 = st.sidebar.slider("Mass Body 2 (red)", 0.5, 5.0, 1.0)
    v0 = st.sidebar.slider("Initial Velocity Magnitude", 0.1, 2.0, 0.6)

    # Fixed symmetric initial conditions
    r1 = np.array([-0.5, 0.0])
    r2 = np.array([0.5, 0.0])

    # Velocity chosen perpendicular for orbit
    v1 = np.array([0.0, v0])
    v2 = np.array([0.0, -v0])

run = st.sidebar.button("Run Simulation")

# Add reset button
if st.sidebar.button("Reset to Manual Mode"):
    st.session_state.earth_moon_mode = False
    st.rerun()

# -------- Constants --------

G = 1.0
dt = 0.03
steps = 20000

# -------- Simulation --------

if run:

    fig, ax = plt.subplots()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.axis("off")

    # Size bodies according to mass
    base_size = 8
    size1 = base_size * np.sqrt(m1) if st.session_state.earth_moon_mode else base_size * np.sqrt(m1)
    size2 = base_size * np.sqrt(m2) if st.session_state.earth_moon_mode else base_size * np.sqrt(m2)

    # Use Earth/Moon colors in Earth-Moon mode - DARKER COLORS
    if st.session_state.earth_moon_mode:
        p1, = ax.plot([], [], 'o', ms=size1, color='#1E90FF', label='Earth')  # Dodger Blue
        p2, = ax.plot([], [], 'o', ms=size2, color='#A9A9A9', label='Moon')  # Dark Gray
        trail1, = ax.plot([], [], '-', lw=1.5, alpha=0.5, color='#1E90FF')
        trail2, = ax.plot([], [], '-', lw=1, alpha=0.5, color='#A9A9A9')
        # Add barycenter marker
        barycenter, = ax.plot([], [], 'o', ms=2, color='#000000', mew=2, label='Barycenter')

    else:
        p1, = ax.plot([], [], 'bo', ms=size1)
        p2, = ax.plot([], [], 'ro', ms=size2)
        trail1, = ax.plot([], [], 'b-', lw=1, alpha=0.5)
        trail2, = ax.plot([], [], 'r-', lw=1, alpha=0.5)
        # Add barycenter marker for manual mode too
        barycenter, = ax.plot([], [], 'o', ms=2, color='#000000', mew=2)

    r1_hist, r2_hist = [], []

    plot_area = st.empty()

    render_every = 6

    for i in range(steps):

        r = r2 - r1
        dist = np.linalg.norm(r) + 1e-6

        force = G * m1 * m2 * r / dist ** 3

        a1 = force / m1
        a2 = -force / m2

        v1[:] += a1 * dt
        v2[:] += a2 * dt

        r1[:] += v1 * dt
        r2[:] += v2 * dt

        r1_hist.append(r1.copy())
        r2_hist.append(r2.copy())

        if i % render_every == 0:

            # Calculate barycenter position
            barycenter_pos = (m1 * r1 + m2 * r2) / (m1 + m2)

            p1.set_data([r1[0]], [r1[1]])
            p2.set_data([r2[0]], [r2[1]])
            barycenter.set_data([barycenter_pos[0]], [barycenter_pos[1]])

            # Convert to numpy arrays only when needed for plotting
            if len(r1_hist) > 0:
                r1_arr = np.array(r1_hist)
                r2_arr = np.array(r2_hist)
                trail1.set_data(r1_arr[:, 0], r1_arr[:, 1])
                trail2.set_data(r2_arr[:, 0], r2_arr[:, 1])

            plot_area.pyplot(fig)
            time.sleep(0.02)  # Slow down the animation

    plt.close(fig)