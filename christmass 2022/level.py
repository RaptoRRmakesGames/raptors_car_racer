import pygame
from pygame.locals import *
from random import choice, randint 
import math, car, ui, pySave, camera

screen_width = 1000
screen_height = 1000

class Level:
    def __init__(self,image, car, camera, pos=(0,0)):
       # Convert the images to a more suitable format for faster blitting
       self.image = image.convert()
       self.road = image
       self.cam = camera
       self.x,self.y = pos    
       self.bcg_mask = pygame.mask.from_surface(self.road) 
       self.car = car
       self.get_car_mask()

    def update(self, screen):
        # Calculate the overlap between the car mask and the background mask
        overlap = self.bcg_mask.overlap_mask(
            self.car_mask, 
            (self.car.rect.x, self.car.rect.y)
        )  

        self.x = 0 - self.cam.scroll[0]
        self.y = 0 - self.cam.scroll[1]

        # Fill the screen with the background color
        screen.blit(self.road.convert_alpha(), (self.x, self.y))
        screen.blit(overlap.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,255,255,255)), (self.x, self.y))


        # Print the overlap count to the console
        print(overlap.count())

    def get_car_mask(self):
        # Convert the car image to a more suitable format for faster blitting
        carimg = self.car.image.convert()
        carimg.set_colorkey((0,0,0))

        self.carimg = carimg
        self.car_mask = pygame.mask.from_surface(self.carimg)