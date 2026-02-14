# 🌌 Physics Backend Handling

This page documents the gravity engine and core physics logic for the sandbox simulation.

File Path: ```UniverseSandbox2D/GameHandler/physics_core.py```

---

## Core Physics Engine

This file handles:

- Gravity calculations
- Celestial body simulation
- Collisions & merging
- Orbital spawning logic
- Background stars

---

## Imports

```GameHandler/physics_core.py```
```python
import random
import pygame
import math
```

These modules handle randomness, rendering, and physics math.

---

## Global Constants

These control how gravity behaves and how the simulation is scaled.

```python
RESOLUTION = (3300, 1400)
G = 900.0
SOFTENING = 90.0
MAX_ACCEL = 2200.0
MAX_SPEED = 2600.0
```

- **G** → gravity strength
- **SOFTENING** → prevents infinite forces at close range
- **MAX_ACCEL** → caps extreme acceleration spikes
- **MAX_SPEED** → prevents unstable physics explosions

---

## Utility Functions

Small helpers used throughout the simulation.

```python
def clamp(v, a, b):
    return a if v < a else b if v > b else v
```

Prevents a value from exceeding limits.

```python
def darken_color(rgb, factor):
    r, g, b = rgb
    return (int(r * factor), int(g * factor), int(b * factor))
```

Adjusts body brightness based on mass.

---

## Background Stars

Handles the decorative starfield.

```python
class BgStars:
    def __init__(self, count=250):
        ...
```

- Generates random background stars
- Purely visual
- Adds depth to space

---

## CelestialMass Class

This is the main object representing a planet or star.

```python
class CelestialMass:
```

Each body stores:

- Position
- Velocity
- Mass
- Radius
- Color
- Acceleration

Key behaviors:

### Movement Step

```python
def step(self, dt):
```

- Applies acceleration
- Caps speed
- Updates position
- Handles edge bouncing (for the main star)

This is the heart of the physics loop.

---

### Color Scaling

```python
def color(self):
```

Bodies darken as they grow heavier, visually representing mass.

---

## Gravity Calculation

All bodies pull on each other using Newton-style gravity.

```python
def gravitate(bodies):
```

For each pair of bodies:

- Compute distance
- Apply softened gravity
- Add acceleration to both bodies

This ensures symmetrical force interaction.

---

## Collision Merging

When bodies collide, they merge.

```python
def merge_collisions(bodies):
```

Behavior:

- Larger mass absorbs smaller mass
- Momentum is conserved
- Radius scales with total mass
- Colors blend together
- One body is removed

This simulates planetary accretion.

---

## Primary Body Detection

Finds the largest gravitational anchor.

```python
def pick_primary(bodies):
```

Used when spawning new planets so they orbit the dominant mass.

---

## Safe Spawn Positioning

Prevents spawning inside the main star.

```python
def safe_spawn_pos(primary, pos, new_r):
```

Ensures new planets spawn:

- Outside collision range
- At safe orbital distance
- Randomized if too close

---

## Natural Orbit Velocity

Generates realistic orbital speeds.

```python
def natural_orbit_velocity(primary, pos, chaos=0.0):
```

Creates:

- Tangential velocity (orbit)
- Small radial drift
- Random noise

Chaos factor increases unpredictability.

---

## Body Spawning

Creates new celestial objects.

```python
def spawn_body(pos, bodies, chaos=0.0):
```

Steps:

1. Choose random radius & mass
2. Pick random color
3. Find primary star
4. Adjust safe spawn location
5. Calculate orbital velocity
6. Return new body

This ensures stable orbital entry.

---

## Summary

This file acts as the **physics brain** of the game.

It manages:

- Gravity simulation
- Motion updates
- Collision physics
- Orbital spawning
- Visual feedback

All celestial behavior flows from this engine.

---

🚀 End of Physics Backend Documentation
