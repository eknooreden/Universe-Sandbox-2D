import os
import pygame
import random
from pygame import event

from GameHandler.game_handlers import *
from GameHandler.graph_handler import RunTracker, append_run_to_json, now_iso 

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
W, H = screen.get_size()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

bg = BgStars(250)

sun = CelestialMass(
    pos=(W / 2, H / 2),
    vel=(0.0, 0.0),
    mass=70000.0,
    radius=70,
    base_color=(255, 170, 90),
    bounce_on_edges=True
)

bodies = [sun]

dragging = False
drag_start = (0, 0)
drag_end = (0, 0)

tracker = RunTracker(sample_every_seconds=10.0)

# Always save next to main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "game_data.json")

running = True
try:
    while running:
        dt = clock.tick(60) / 1000.0
        if dt > 0.03:
            dt = 0.03

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                if ev.key == pygame.K_c:
                    bodies = [sun]

            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mods = pygame.key.get_mods()
                if ev.button == 1:
                    chaos = 1.0 if (mods & pygame.KMOD_SHIFT) else 0.0
                    bodies.append(spawn_body(ev.pos, bodies, chaos=chaos))
                elif ev.button == 3:
                    dragging = True
                    drag_start = ev.pos
                    drag_end = ev.pos

            elif ev.type == pygame.MOUSEMOTION:
                if dragging:
                    drag_end = ev.pos

            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 3 and dragging:
                    dragging = False
                    dx = drag_start[0] - drag_end[0]
                    dy = drag_start[1] - drag_end[1]
                    vel = (dx * 2.8, dy * 2.8)

                    radius = random.randint(10, 26)
                    mass = radius * radius * 4.0
                    base_color = random.choice(COLOR_LIST)

                    primary = pick_primary(bodies)
                    pos2 = safe_spawn_pos(primary, drag_start, radius)
                    bodies.append(
                        CelestialMass(pos=pos2, vel=vel, mass=mass, radius=radius, base_color=base_color)
                    )

        gravitate(bodies)
        for b in bodies:
            b.step(dt)
        merge_collisions(bodies)

        # Find greatest mass safely
        greatest = 0.0
        for b in bodies:
            if b.m > greatest:
                greatest = b.m

        tracker.update(dt, len(bodies))

        screen.fill((0, 0, 0))
        bg.draw(screen)

        for b in bodies:
            b.draw(screen)

        label = font.render(f"Bodies: {len(bodies)}", True, (255, 255, 255))
        screen.blit(label, (20, 20))

        greatest_label = font.render(f"Greatest mass: {greatest:.1f}", True, (255, 255, 255))
        screen.blit(greatest_label, (20, 60))

        if dragging:
            pygame.draw.line(screen, (255, 255, 255), drag_start, drag_end, 2)

        pygame.display.flip()

finally:
    pygame.quit()
    append_run_to_json(
        JSON_PATH,
        body_points=tracker.body_points(),
        time_ended=tracker.time_ended_seconds(),
        date_done=now_iso(),
    )

    tracker.show_graph(title="UniverseSandbox2D: Bodies vs Time (every 10s)")