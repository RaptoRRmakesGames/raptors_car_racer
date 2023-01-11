import pygame
from pygame.locals import *
from random import randint,choice,uniform

class Particle:
    def __init__(self, pos, vel, rad, rad_speed, manager, colour, custom_death_meter=0):
        self.pos_x,self.pos_y = pos 
        self.vel = vel
        self.rad = rad
        self.diss_speed = rad_speed
        self.manager = manager
        self.colour = colour
        self.custom_death_meter = custom_death_meter

    def update(self, screen,cam):
        self.rad -= self.diss_speed

        self.pos_x += self.vel[0]
        self.pos_y += self.vel[1]

        self.x,self.y = self.pos_x, self.pos_y

        #self.pos_x = self.x - cam.scroll[0]
        #self.pos_y = self.y - cam.scroll[0]

        if self.rad < self.custom_death_meter:
            self.manager.normal_particles.remove(self)
        
        pygame.draw.circle(
            screen,
            self.colour,
            (int(self.pos_x), int(self.pos_y)),
            int(self.rad)
        )

class Particle_Manager:
    def __init__(self,cam):
        self.normal_particles = []
        self.cam = cam

    def update_particles(self, screen):
        for particle in self.normal_particles:
            particle.update(screen, self.cam)
        #print(len(self.normal_particles))
        
    def create_particle(self, pos, vel, rad, rad_speed, colour, custom_death_meter=0):
        self.normal_particles.append(Particle(pos,vel,rad,rad_speed,self,colour, custom_death_meter=custom_death_meter))

if __name__ == '__main__':

    screen = pygame.display.set_mode((500,500))

    clock = pygame.time.Clock()

    fps =83

    run = True

    pm = Particle_Manager()

    while run:

        clock.tick_busy_loop(fps)

        screen.fill((0,0,0))

        pm.create_particle(pygame.mouse.get_pos(), (-0.05, 0.05), 4.8,0.12, (255,255,255))

        pm.update_particles(screen)

        print(clock.get_fps())

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        pygame.display.update()
