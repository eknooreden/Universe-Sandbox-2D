import random
import pygame
import math

pygame.init()

RESOLUTION = (3300, 1400)
W, H = RESOLUTION

COLOR_LIST = [
    (202, 255, 253),
    (255, 242, 204),
    (255, 191, 0),
    (209, 110, 120),
    (209, 12, 12),
    (82, 17, 17),
    (166, 152, 242),
    (155, 52, 237),
    (52, 237, 173),
    (0, 255, 240),
    (104, 135, 2)
]

G = 900.0
SOFTENING = 90.0
MAX_ACCEL = 2200.0
MAX_SPEED = 2600.0

def clamp(v, a, b):
    return a if v < a else b if v > b else v

def darken_color(rgb, factor):
    r, g, b = rgb
    return (int(r * factor), int(g * factor), int(b * factor))

class BgStars:
    def __init__(self, count=250):
        self.stars = []
        for _ in range(count):
            x = random.randint(0, W)
            y = random.randint(0, H)
            r = random.randint(1, 3)
            self.stars.append((x, y, r))

    def draw(self, surface):
        for x, y, r in self.stars:
            pygame.draw.circle(surface, (255, 255, 255), (x, y), r)

class CelestialMass:
    def __init__(self, pos, vel, mass, radius, base_color, bounce_on_edges=False):
        self.x = float(pos[0])
        self.y = float(pos[1])
        self.vx = float(vel[0])
        self.vy = float(vel[1])
        self.m = float(mass)
        self.r = int(radius)
        self.base_color = base_color
        self.ax = 0.0
        self.ay = 0.0
        self.bounce_on_edges = bounce_on_edges
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color(), (int(self.x), int(self.y)), self.r)


    def reset_accel(self):
        self.ax = 0.0
        self.ay = 0.0

    def add_accel(self, ax, ay):
        self.ax += ax
        self.ay += ay

    def color(self):
        factor = 1.05 - 0.55 * (self.m / (self.m + 90000.0))
        factor = clamp(factor, 0.35, 1.0)
        return darken_color(self.base_color, factor)

    def step(self, dt):
        amag = math.hypot(self.ax, self.ay)
        if amag > MAX_ACCEL:
            s = MAX_ACCEL / amag
            self.ax *= s
            self.ay *= s

        self.vx += self.ax * dt
        self.vy += self.ay * dt

        vmag = math.hypot(self.vx, self.vy)
        if vmag > MAX_SPEED:
            s = MAX_SPEED / vmag
            self.vx *= s
            self.vy *= s

        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.bounce_on_edges:
            if self.x < self.r:
                self.x = self.r
                self.vx *= -0.25
            elif self.x > W - self.r:
                self.x = W - self.r
                self.vx *= -0.25

            if self.y < self.r:
                self.y = self.r
                self.vy *= -0.25
            elif self.y > H - self.r:
                self.y = H - self.r
                self.vy *= -0.25

def gravitate(bodies):
    soft2 = SOFTENING * SOFTENING
    for b in bodies:
        b.reset_accel()

    n = len(bodies)
    for i in range(n):
        a = bodies[i]
        for j in range(i + 1, n):
            b = bodies[j]
            dx = b.x - a.x
            dy = b.y - a.y
            dist2 = dx * dx + dy * dy + soft2
            dist = math.sqrt(dist2)
            inv_dist3 = 1.0 / (dist2 * dist)

            ax_a = G * b.m * dx * inv_dist3
            ay_a = G * b.m * dy * inv_dist3
            ax_b = -G * a.m * dx * inv_dist3
            ay_b = -G * a.m * dy * inv_dist3

            a.add_accel(ax_a, ay_a)
            b.add_accel(ax_b, ay_b)

def merge_collisions(bodies):
    i = 0
    while i < len(bodies):
        a = bodies[i]
        j = i + 1
        while j < len(bodies):
            b = bodies[j]
            dx = b.x - a.x
            dy = b.y - a.y
            dist = math.hypot(dx, dy)
            if dist < a.r + b.r:
                if a.m < b.m:
                    a, b = b, a
                    bodies[i], bodies[j] = bodies[j], bodies[i]

                total_m = a.m + b.m
                a.vx = (a.m * a.vx + b.m * b.vx) / total_m
                a.vy = (a.m * a.vy + b.m * b.vy) / total_m
                a.x = (a.m * a.x + b.m * b.x) / total_m
                a.y = (a.m * a.y + b.m * b.y) / total_m
                a.m = total_m

                a.r = int(max(a.r, math.sqrt(a.m) * 0.35))

                r1, g1, b1 = a.base_color
                r2, g2, b2 = b.base_color
                a.base_color = (int((r1 + r2) / 2), int((g1 + g2) / 2), int((b1 + b2) / 2))

                bodies.pop(j)
                continue
            j += 1
        i += 1

def pick_primary(bodies):
    biggest = bodies[0]
    for b in bodies[1:]:
        if b.m > biggest.m:
            biggest = b
    return biggest

def safe_spawn_pos(primary, pos, new_r):
    dx = pos[0] - primary.x
    dy = pos[1] - primary.y
    dist = math.hypot(dx, dy)
    extra = 180.0
    min_dist = primary.r + new_r + extra

    if dist < 1.0:
        ang = random.uniform(0.0, math.tau)
        return (primary.x + math.cos(ang) * min_dist, primary.y + math.sin(ang) * min_dist)

    if dist < min_dist:
        nx = dx / dist
        ny = dy / dist
        return (primary.x + nx * min_dist, primary.y + ny * min_dist)

    return (float(pos[0]), float(pos[1]))

def natural_orbit_velocity(primary, pos, chaos=0.0):
    dx = pos[0] - primary.x
    dy = pos[1] - primary.y
    r = math.hypot(dx, dy)
    if r < 1.0:
        return (0.0, 0.0)

    v_circ = math.sqrt(G * primary.m / max(r, 1.0))

    tangential_scale = random.uniform(0.85 - 0.25 * chaos, 1.08 + 0.25 * chaos)
    radial_scale = random.uniform(-0.10 - 0.30 * chaos, 0.10 + 0.30 * chaos)

    tx = -dy / r
    ty = dx / r
    rx = dx / r
    ry = dy / r

    v = v_circ * tangential_scale
    vr = v_circ * radial_scale

    vx = v * tx + vr * rx
    vy = v * ty + vr * ry

    noise = (0.03 + 0.10 * chaos) * v_circ
    vx += random.uniform(-noise, noise)
    vy += random.uniform(-noise, noise)

    return (vx, vy)

def spawn_body(pos, bodies, chaos=0.0):
    radius = random.randint(10, 26)
    mass = radius**2 * 3.5
    base_color = random.choice(COLOR_LIST)

    primary = pick_primary(bodies)
    pos2 = safe_spawn_pos(primary, pos, radius)

    vx, vy = natural_orbit_velocity(primary, pos2, chaos=chaos)
    return CelestialMass(pos=pos2, vel=(vx, vy), mass=mass, radius=radius, base_color=base_color)