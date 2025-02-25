import math
import pygame
import random
from pygame import gfxdraw
from typing import Self

G = 6.57e-11  # Gravitational constant

class Particle:
    TIMESTEP = 1  # Each time step is 1/2 day

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        x_int = int(self.x)
        y_int = int(self.y)
        self.radius_int = int(self.radius)

        gfxdraw.aacircle(win, x_int, y_int, self.radius_int, self.color)
        gfxdraw.filled_circle(win, x_int, y_int, self.radius_int, self.color)

    def circle_surf(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if 2 <= distance <= 0:
            distance = 2

        try:
            force = G * (self.mass * other.mass) / distance ** 2

        except ZeroDivisionError:
            force = G * (self.mass * other.mass) / 1

        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    # If the particles collide, we will make them bounce off eachother including the radius

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

    # updates the postion of particles besed on the gravcitational force it is effected by
    def update_position(self, particles):

        # Collision between particles
        for particle in particles:
            if particle != self:
                self.collision(particle)

        # gets the screen size (width, height)
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        # collision with screen borders (if the particle goes out of bounds)(decreases the speed as well)
        if self.x >= WIDTH or self.x <= 0:
            self.x_vel *= -0.9
        if self.y >= HEIGHT or self.y <= 0:
            self.y_vel *= -0.9

        total_fx = total_fy = 0
        for particle in particles:

            if self == particle:
                continue

            fx, fy = self.attraction(particle)
            total_fx += fx
            total_fy += fy

        # Calculate Velocity using a = F / m
        self.x_vel += (total_fx / self.mass * self.TIMESTEP) * 0.9
        self.y_vel += (total_fy / self.mass * self.TIMESTEP) * 0.9

        # Because sometimes the velocity is too high and the particle goes off the screen
        # We will make sure that the velocity is not too high

        # Update coordinates usuing velocity
        # Timestep is used to ensure the we are moving the accurate amount of time
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # Append the current position to the orbit list
        self.orbit.append((self.x, self.y))

    # create a list of random particles
    def create_particles(self, num_particles):

        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        createdParticles = []
        for i in range(num_particles):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            radius = random.randint(3, 9)
            mass = radius * 2 * 10 ** 10
            particleName = "Particle" + str(i)
            createdParticles.append(Particle(x, y, radius, color, mass, particleName))

        return createdParticles

        # def paused():

        clock = pygame.time.Clock()

        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((WIDTH / 2), (HEIGHT / 2))

        gameDisplay.blit(TextSurf, TextRect)

        while pause:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # gameDisplay.fill(white)

            button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
            button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

            pygame.display.update()
            clock.tick(15)


def main():
    pygame.init()

    WIDTH, HEIGHT = 1000, 1000

    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("A particle simulation")

    run = True
    clock = pygame.time.Clock()

    # Tells which particles to draw
    # create particles list
    particles = []
    # ask the user to input the number of particles they want to create
    num_particles = int(input("Enter the number of particles: "))
    particles = Particle.create_particles(particles, num_particles)
    print(particles)

    # print the number of particles created and their names
    print("The following particles were created: ")
    for particle in particles:
        print(particle.name, ", Radius", particle.radius, ", Mass", particle.mass)

    while run:
        # Limits the game to 60fps
        clock.tick(60)
        WIN.fill((0, 0, 0))

        # funtion that quits the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draws the particles specified in line 58
        for particle in particles:
            particle.update_position(particles)
            particle.draw(WIN)

        pygame.display.update()

    pygame.quit()


# main()
if __name__ == "__main__":
    main()
