import math
import random

import pygame
from pygame import gfxdraw, SurfaceType, Surface


class Particle:
    TIMESTEP = 1  # Each time step is 1/2 day
    G = 6.57e-11  # Gravitational constant

    def __init__(self, x, y, radius, color, mass, x_vel, y_vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.id = id(self)
        self.x_vel = x_vel
        self.y_vel = y_vel

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if 2 <= distance <= 0:
            distance = 2

        try:
            force = self.G * (self.mass * other.mass) / distance ** 2

        except ZeroDivisionError:
            force = self.G * (self.mass * other.mass) / 1

        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    # If the particles collide, we will make them bounce off each other including the radius

    def collision(self, other):
        if (
                self.x - self.radius <= other.x + other.radius
                and self.x + self.radius >= other.x - other.radius
        ):
            if (
                    self.y - self.radius <= other.y + other.radius
                    and self.y + self.radius >= other.y - other.radius
            ):
                # Calculate angle of incidence of the collision
                theta = math.atan2(self.y - other.y, self.x - other.x)
                # Calculate the angle of reflection
                theta_reflection = math.pi - theta
                # Calculate the velocity of the particle after the collision
                self.x_vel = math.cos(theta_reflection) * self.x_vel
                self.y_vel = math.sin(theta_reflection) * self.y_vel
                other.x_vel = math.cos(theta_reflection) * other.x_vel
                other.y_vel = math.sin(theta_reflection) * other.y_vel
                # Calculate the new position of the particles after the collision
                self.x = self.x + self.x_vel * Particle.TIMESTEP
                self.y = self.y + self.y_vel * Particle.TIMESTEP
                other.x = other.x + other.x_vel * Particle.TIMESTEP
                other.y = other.y + other.y_vel * Particle.TIMESTEP

    def update_position(self):
        self.x = self.x + self.x_vel * Particle.TIMESTEP
        self.y = self.y + self.y_vel * Particle.TIMESTEP


def draw_particle(particle: Particle, win: Surface | SurfaceType):
    pygame.draw.circle(win, particle.color, (particle.x, particle.y), particle.radius)
    x_int = int(particle.x)
    y_int = int(particle.y)
    radius_int = int(particle.radius)

    gfxdraw.aacircle(win, x_int, y_int, radius_int, particle.color)
    gfxdraw.filled_circle(win, x_int, y_int, radius_int, particle.color)


def main():
    pygame.init()

    WIDTH, HEIGHT = 1000, 1000

    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("A particle simulation")

    run = True
    clock = pygame.time.Clock()

    p = Particle(10, 10, 10, (10, 10, 110), 5, 3, 3)

    while run:
        # Limits the game to 60fps
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        p.update_position()
        draw_particle(p, WIN)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
