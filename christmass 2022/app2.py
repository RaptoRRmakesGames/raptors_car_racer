import pygame
from pygame.locals import *
from random import choice, randint 
import math

# screen size
screen_WIDTH    = 1000
screen_HEIGHT   = 1000
screen_SURFACE  = pygame.HWSURFACE|pygame.DOUBLEBUF

class CarSprite( pygame.sprite.Sprite ):
    def __init__( self, car_image, x, y, max_speed, accel,rot_speed=1.8 ,rotations=360 ):
        pygame.sprite.Sprite.__init__(self)

        self.rotated_images = {}
        self.min_angle = ( 360 / rotations ) 
        for i in range( rotations ):
            rotated_image = pygame.transform.rotozoom( car_image, 360-90-( i*self.min_angle ), 1 )
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
        self.steer_strenght = rot_speed
        self.drift_point = 0.00
        self.accel = accel
        self.max_speed = self.accel * 180

    def turn( self, ori=1 ):
        if self.speed > 0 or self.speed < 0 :
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
            self.steer_strenght = 1.5
        else:
            self.steer_strenght = 3

        if self.speed > self.max_speed and not pygame.key.get_pressed()[K_SPACE]:
            self.speed = self.max_speed

        if self.speed < -self.max_speed / 4:
            self.speed = -self.max_speed / 4

        self.speed += self.drift_point

        if not pygame.key.get_pressed()[K_SPACE]:
            self.velocity.from_polar((self.speed, math.degrees(self.heading)))
            
            self.drift_point -= 0.001
            if self.drift_point < 0:
                self.drift_point = 0 
            
        else:
            self.steer_strenght = 4
            self.drift_point += 0.001
            if self.drift_point > self.accel / 1.5:
                self.drift_point = self.accel / 1.5

        self.speed -= self.drift_point

        if not self.acc and not self.speed < 0.04:
            self.speed -= 0.04

        self.position += self.velocity
        self.rect.center = self.position

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode( ( screen_WIDTH, screen_HEIGHT ), screen_SURFACE )
pygame.display.set_caption("Car Steering")

road_image = road_image = pygame.image.load( 'road_texture.png' )
background = pygame.transform.smoothscale( road_image, ( screen_WIDTH, screen_HEIGHT ) )
car_image  = pygame.transform.scale(pygame.image.load( 'car.png' ).convert_alpha(), (24,50))

black_car = CarSprite( car_image, screen_WIDTH//2, screen_HEIGHT//2,5, 0.05, rotations=360)
car_group = pygame.sprite.Group()
car_group.add( black_car )

clock = pygame.time.Clock()
done = False
while not done:

    for event in pygame.event.get():
        if ( event.type == pygame.QUIT ):
            done = True

    keys = pygame.key.get_pressed()

    car_group.update()

    screen.blit( background, ( 0, 0 ) ) 
    car_group.draw( screen )
    pygame.display.flip()
  
    clock.tick_busy_loop(75)

pygame.quit()