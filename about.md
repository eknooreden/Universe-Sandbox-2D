# 🌌 Gravity Sandbox (2D)

A simple sandbox game where you can experiment with gravity and orbital physics.

This project was originally created for testing, but it’s also fun to play around with. It’s inspired by **Universe Sandbox**, a 3D universe simulator — this is a simplified **2D version** that still uses gravitational equations to simulate planetary motion.

Experiment, spawn planets, and try to build stable orbits!

The modules used to create this are listed in the following.

```
import os
import random
import math
import pygame
import matplotlib
import json
import datetime
```

---

## 🎮 Controls

The controls are intentionally simple:

- **Left click** → Instantly snap a planet into orbit around the nearest larger mass  
- **Right click** → Spawn a planet with natural gravity  
- **Right click + drag + release** → Spawn a planet with velocity  
  - Hold longer = more speed  
  - Drag direction = launch direction  
  - Useful for creating custom orbits

---

## ✨ Features

- 🎨 Every spawned celestial mass gets a **random color**
- ⭐ A large central star spawns automatically at startup (center of the screen)
- 💥 Collisions merge masses into a **larger body with stronger gravity**
- 🧲 Gravity is calculated using a simplified planetary gravity equation
- 🧱 The central star **cannot leave the screen**
  - It bounces off the edges
- 🪐 Spawned planets can freely exit the screen

---

## ⚠ Glitches / Bug Reports

If you notice glitches, bugs, or weird physics behavior, please report them so they can be fixed.

---

## ❤️ Credits

Inspired by **Universe Sandbox**  
Created as a physics sandbox experiment

---

## 🚀 Have Fun!

Play around with gravity. Break the system. Create impossible orbits.

That’s the whole point.
