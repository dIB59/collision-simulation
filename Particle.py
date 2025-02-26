import math

import pygame
from pygame import gfxdraw, SurfaceType, Surface
from typing import Self, Iterator


class Particle:
    TIMESTEP = 1  # Each time step is 1/2 day
    G = 6.57e-11  # Gravitational constant
    number = 0

    def __hash__(self):
        return self.id

    def __init__(self, x, y, radius, color, mass, x_vel, y_vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.id = Particle.number
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.remove = False

        Particle.number += 1

    def attraction(self: Self, other: Self):
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

    def collision(self, other: Self):
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

                difference_vel = math.sqrt((self.x_vel - other.x_vel) ** 2 + (self.y_vel - other.y_vel) ** 2)

                if difference_vel < self.escape_velocity(other):
                    if not self.remove:
                        other.remove = True

                    self.mass += other.mass
                    self.radius += other.radius
                    self.x_vel = (self.x_vel * self.mass + other.x_vel * other.mass) / self.mass
                    self.y_vel = (self.y_vel * self.mass + other.y_vel * other.mass) / self.mass

                    self.color = (
                        min(255, (self.color[0] + other.color[0]) // 2 + 1),
                        min(255, (self.color[1] + other.color[1]) // 2 + 1),
                        min(255, (self.color[2] + other.color[2]) // 2 + 1)
                    )

                # Calculate the new position of the particles after the collision
                self.x = self.x + self.x_vel * Particle.TIMESTEP
                self.y = self.y + self.y_vel * Particle.TIMESTEP
                other.x = other.x + other.x_vel * Particle.TIMESTEP
                other.y = other.y + other.y_vel * Particle.TIMESTEP

    def escape_velocity(self, other: Self) -> float:
        return math.sqrt(2 * self.G * (self.mass + other.mass) / self.radius)

    def update_position(self, particles: Iterator[Self]):
        for particle in particles:
            if particle != self:
                force_x, force_y = self.attraction(particle)
                self.x_vel += force_x / self.mass
                self.y_vel += force_y / self.mass

                self.collision(particle)

        self.x = self.x + self.x_vel * Particle.TIMESTEP
        self.y = self.y + self.y_vel * Particle.TIMESTEP

        self.y_vel = self.y_vel * 0.995
        self.x_vel = self.x_vel * 0.995

        if self.x >= 1000 or self.x <= 0:
            self.x_vel = -self.x_vel
        if self.y >= 1000 or self.y <= 0:
            self.y_vel = -self.y_vel


def draw_particle(particle: Particle, win: Surface | SurfaceType):
    x_int = int(particle.x)
    y_int = int(particle.y)
    radius_int = int(particle.radius)
    gfxdraw.aacircle(win, x_int, y_int, radius_int, particle.color)
    gfxdraw.filled_circle(win, x_int, y_int, radius_int, particle.color)
