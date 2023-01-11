import pygame
from pygame.locals import *
class Camera:
    def __init__(self, speed, screen):
        self.scroll = [0,0]
        self.speed = speed
        self.screen = screen
        self.zoom = 1

    def move_on_command(self):

        keys = pygame.key.get_pressed()
        
        if keys[K_UP]:
            self.scroll[1] -= self.speed 
        if keys[K_DOWN]:
            self.scroll[1] += self.speed 
        if keys[K_RIGHT]:
            self.scroll[0] += self.speed 
        if keys[K_LEFT]:
            self.scroll[0] -= self.speed 
            
    def follow(self, obj, speed=2):


        if (obj.rect.x  - self.scroll[0]) != self.screen.get_width()/2:
            self.scroll[0] += ((obj.rect.x - (self.scroll[0] + self.screen.get_width()/2))) / speed
        if obj.rect.y   - self.scroll[1] != self.screen.get_height()/2:
           self.scroll[1] += ((obj.rect.y - (self.scroll[1] + self.screen.get_height()/2))) / speed


    def zoom_game(self, zoom):
        self.zoom = zoom

    def center_obj(self, obj):
        self.scroll = [obj.rect.x,obj.rect.y]

