import pygame
from pygame.locals import *
from random import choice, randint 
import math, camera

class CarSprite( pygame.sprite.Sprite ):
    def __init__( self, car_image, x, y, max_speed, accel,rot_speed=[1.8, 2.2, 3] ,rotations=360, camera="" ):
        pygame.sprite.Sprite.__init__(self)

        self.rotated_images = {}
        self.min_angle = ( 360 / rotations ) 
        for i in range( rotations ):
            rotated_image = pygame.transform.rotozoom( pygame.transform.scale(car_image, (12*camera.zoom,25*camera.zoom)), 360-90-( i*self.min_angle ), 1 )
            self.rotated_images[i*self.min_angle] = rotated_image
            
        self.min_angle = math.radians( self.min_angle )
        self.image       = self.rotated_images[0]
        self.rect        = self.image.get_rect()
        self.rect.center = ( x, y )
        self.reversing = False
        self.heading   = 0 
        self.speed     = 0    
        self.velocity  = pygame.math.Vector2( 0, 0 )
        self.position  = pygame.math.Vector2( x, y )
        self.speed_hardening = 1 
        self.acc = False
        self.steer_strenght_acc = rot_speed[0]
        self.steer_strength_normal= rot_speed[1]
        self.steer_strength_drift= rot_speed[2]
        self.steer_strength = rot_speed[1]
        self.drift_point = 0.00
        self.accel = accel
        self.max_speed = self.accel * 150
        self.cam = camera

    def turn( self, ori=1 ):
        if self.speed > 0.1 or self.speed < 0. :
            self.heading += math.radians( self.steer_strenght * ori ) 
            image_index = int((self.heading + self.min_angle / 2) / self.min_angle) % len(self.rotated_images)
            image = self.rotated_images[image_index]
            if self.image is not image:
                x,y = self.rect.center
                self.image = image
                self.rect  = self.image.get_rect()
                self.rect.center = (x,y)

    def accelerate( self):
        self.speed += self.accel

    def brake( self ):
        if self.speed > 0:
            self.speed -= self.accel * 3

        if abs(self.speed) < 0.1:
            self.speed = 0
        self.velocity.from_polar((self.speed, math.degrees(self.heading)))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.accelerate()

        if keys[K_s]:
            self.brake()
        if keys[K_a]:
            self.turn(-1)
        if keys[K_d]:
            self.turn()

        if keys[pygame.K_s] or keys [pygame.K_w]:
            self.acc = True
        else:
            self.acc = False

    def update( self ):
        

        self.move()
        self.speed_hardening = self.speed / 100
        self.speed = round(self.speed, 3)

        if self.acc:
            self.steer_strenght = self.steer_strenght_acc
        else:
            self.steer_strenght = self.steer_strength_normal

        if self.speed > self.max_speed and not pygame.key.get_pressed()[K_SPACE] and not self.drift_point > 0:
            self.speed += self.accel / 4 - self.speed_hardening / 2

        if self.speed > self.max_speed * 1.8:
            self.speed = self.max_speed * 1.8

        if self.speed < -self.max_speed / 4:
            self.speed = -self.max_speed / 4

        if not pygame.key.get_pressed()[K_SPACE]:
            self.velocity.from_polar((self.speed, math.degrees(self.heading)))
            self.speed += self.drift_point
            
            self.drift_point -= 0.0001
            if self.drift_point < 0:
                self.drift_point = 0 
            self.speed -= self.drift_point
            
        else:
            self.steer_strenght = self.steer_strength_drift
            self.drift_point += 0.0001
            if self.drift_point > self.accel / 1.5:
                self.drift_point = self.accel / 1.5

        

        if not self.acc and not self.speed < 0.04:
            self.speed -= (self.accel / 2) + self.speed_hardening

            if self.speed < 0.05:
                self.speed = 0 

        self.position += self.velocity
        self.rect.center = self.position
