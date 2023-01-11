import pygame
from pygame.locals import *
from random import choice, randint 
import math, camera, ui

class CarSprite( pygame.sprite.Sprite ):
    def __init__( self, car_image, x, y, max_speed, accel,rot_speed=[1.8, 2.2, 3],top_speed=0,price=0,name="" ,rotations=360, camera="" ):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        
        self.cost = price

        self.rotated_images = {}
        self.min_angle = ( 360 / rotations ) 
        for i in range( rotations ):
            rotated_image = pygame.transform.rotozoom( pygame.transform.scale(car_image, (12*camera.zoom,30*camera.zoom)), 360-90-( i*self.min_angle ), 1.4 )
            self.rotated_images[i*self.min_angle] = rotated_image

        self.show_image = pygame.transform.rotozoom(pygame.transform.scale(car_image, (12*3.6, 30*3.6)),0,1.8) 
            
        self.min_angle = math.radians( self.min_angle )

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
        self.max_speed = self.accel * top_speed
        self.cam = camera
        self.laps = 0 
        self.starting = True
        self.best_speed = 0
        self.performances = {}
        self.out = False
        self.bought = False
        self.image_index = 180
        self.blue_fire = False
        self.boom_effect = False
        self.speed_multi = top_speed
        self.turn_speeds = rot_speed
        self.heading =3

        self.start_pos = x,y

        self.image       = self.rotated_images[self.image_index]
        self.rect        = self.image.get_rect()
        self.rect.center = ( x, y )

        self.speedometer = speedometer = ui.TextWithBackground((100,50), (60,950),  pygame.transform.scale(pygame.image.load("images/road_texture.png"), (200, 75)).convert(),)

        self.turn()

    def show_speedometer(self, screen):
        self.speedometer.update(screen,round(self.speed*100,2) , " km/h")

    def reset(self):
        self.position = pygame.math.Vector2(500,770)
        self.speed = 0 
        self.velocity =  pygame.math.Vector2( 0, 0 )
        self.heading =3
        self.image_index = 180
        self.image       = self.rotated_images[self.image_index]
        self.starting = True
        print(f"{self.name} reset")

    def turn( self, ori=1 ):

        if self.speed > 0.1 or self.speed < 0. :
            self.heading += math.radians( self.steer_strenght * ori ) 

            self.image_index = int((self.heading + self.min_angle / 2) / self.min_angle) % len(self.rotated_images)
            
            image = self.rotated_images[self.image_index]
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

    def update( self, screen ):
        
        if self.out:
            self.speed /= 2

        if self.starting:
            self.position = pygame.math.Vector2(500,750)

        self.move()
        self.speed_hardening = self.speed / 110
        self.speed = round(self.speed, 3)

        if self.acc:
            self.steer_strenght = self.steer_strenght_acc
        else:
            self.steer_strenght = self.steer_strength_normal

        if self.speed > self.max_speed and not pygame.key.get_pressed()[K_SPACE] and not self.drift_point > 0:
            self.speed += self.accel / 4 - self.speed_hardening / 2

        if self.speed > self.max_speed * 1.8:
            self.speed = self.max_speed * 1.8

        if self.speed > self.max_speed * 1.5:
            self.blue_fire = True
            self.boom_effect = True
            if self.speed > self.max_speed * 1.55:
                self.boom_effect = False

        else:
            self.blue_fire = False
            self.boom_effect = False
            #self.speed = self.max_speed * 1.8

        #print(self.boom_effect)

        if self.speed < -self.max_speed / 4:
            self.speed = -self.max_speed / 4

        if not pygame.key.get_pressed()[K_SPACE]:
            self.velocity.from_polar((self.speed, math.degrees(self.heading)))
            self.speed += self.drift_point
            
            self.drift_point -= 0.0002
            if self.drift_point < 0:
                self.drift_point = 0 
            self.speed -= self.drift_point
            
        else:
            self.velocity /= 1.02
            self.steer_strenght = self.steer_strength_drift
            if not self.acc:
                self.drift_point += 0.0001
                if self.drift_point > self.accel / 1.5:
                    self.drift_point = self.accel / 1.5

        if not self.acc and not self.speed < 0.04:
            self.speed -= (self.accel / 2) + self.speed_hardening

            if self.speed < 0.05:
                self.speed = 0 

        self.position += self.velocity
        self.rect.center = self.position

        

        if self.out:
            self.speed *= 1.9
    
    def add_lap(self, mapname, time, lap_num):
        if not mapname in self.performances:
            self.performances[mapname] = []
        
        self.performances[mapname].append(time)

    def blit_icon(self,screen ,pos, size):
        screen.blit(pygame.transform.rotozoom(self.show_image, 1,size), pos)

    def bought_car(self):
        self.bought = self.bought
