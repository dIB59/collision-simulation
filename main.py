import random

import pygame

from Particle import Particle, draw_particle


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def main():
    pygame.init()

    WIDTH, HEIGHT = 1000, 1000

    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("A particle simulation")

    run = True
    clock = pygame.time.Clock()

    particle_lst = dict()
    p1 = Particle(500, 500, 10, random_color(), 10 ** 12, 5, 9)
    p = Particle(700, 700, 10, random_color(), 10 ** 12, -9, -12)
    p2 = Particle(300, 300, 10, random_color(), 10 ** 12, 2, 6)
    p3 = Particle(100, 100, 10, random_color(), 10 ** 12, -12, -11)
    p4 = Particle(900, 900, 10, random_color(), 10 ** 12, 9, 12)

    particle_lst[p1.id] = p1
    particle_lst[p.id] = p
    particle_lst[p2.id] = p2
    particle_lst[p3.id] = p3
    particle_lst[p4.id] = p4

    while run:
        # Limits the game to 60fps
        clock.tick(60)
        WIN.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for particle in particle_lst.values():
            draw_particle(particle, WIN)
            particle.update_position(particle_lst.values().__iter__())

        particle_lst = {k: v for k, v in particle_lst.items() if not v.remove}
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
