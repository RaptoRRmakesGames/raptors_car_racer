import pygame
from pygame.locals import *
from random import choice, randint 
import math, car_file, ui, pySave, camera, time

screen_width = 1000
screen_height = 1000

class Level:
    def __init__(self,image, car, camera,screen, name ,bcg_color=(0,18,48) ,pos=(0,0)):
       # Convert the images to a more suitable format for faster blitting
        self.image = image.convert()
        self.road = image
        self.cam = camera
        self.x,self.y = pos    
        self.bcg_mask = pygame.mask.from_surface(self.road) 
        self.car = car
        self.get_car_mask()
        self.name = name

        self.offset = 0


        #self.rect2 = self.circle2.get_rect(topleft=[320, 280])

        self.bcg_color = bcg_color

        self.went_bottom = False
        self.went_bottom_again = False
        self.went_above = False
        self.went_left = False
        self.went_right = False

    def update(self, screen):
        self.circle = pygame.Rect(-self.cam.scroll[0], -self.cam.scroll[1],1000*1.3,150*1.3
            #[0,0,255],
            #[427,850],#pygame.mouse.get_pos(),
            
        )
        #self.rect1 = self.circle.get_rect(topleft=[360, 780])

        self.circle2 = pygame.Rect(
            #pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
           470-self.cam.scroll[0], 1020-self.cam.scroll[1],
           150*1.3,150*1.3
            
        )
        #(pygame.mouse.get_pos())

        self.circle3 = pygame.Rect(-self.cam.scroll[0], 0-self.cam.scroll[1],150*1.3,1000*1.3
            #[0,0,255],
            #[427,850],#pygame.mouse.get_pos(),
            
        )
        #self.rect1 = self.circle.get_rect(topleft=[360, 780])

        self.circle4 = pygame.Rect(
           1000-self.cam.scroll[0], 0-self.cam.scroll[1],
           150*1.3,1000*1.3
            
        )

        self.x = 0 - self.cam.scroll[0]
        self.y = 0 - self.cam.scroll[1]

        # Calculate the overlap between the car mask and the background mask
        self.offset = (self.car.rect.x - self.x, self.car.rect.y - self.y)
        overlap = self.bcg_mask.overlap_mask(self.car_mask, self.offset)  

        # Fill the screen with the background color
        screen.fill(self.bcg_color)
        screen.blit(self.road.convert_alpha(), (self.x, self.y))
        #screen.blit(overlap.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,255,255,255)), (self.x, self.y))

        # Print the overlap count to the console
        #print(overlap.count())

        # pygame.draw.rect(
        #     screen, (255,126,12),
        #     self.circle
        # )
        # pygame.draw.rect(
        #     screen, (255,126,12),
        #     self.circle2
        # )

        # pygame.draw.rect(
        #     screen, (255,126,12),
        #     self.circle3
        # )
        # pygame.draw.rect(
        #     screen, (255,126,12),
        #     self.circle4
        # )
        
        #screen.blit(overlap.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,255,255,255)), (self.x, self.y))

        # make car go slower if its not touching the road completely
        if overlap.count() < 180:
            self.car.out = True
        else:
            self.car.out = False

        if self.circle2.collidepoint(self.car.rect.center):
            if not self.went_bottom:
                self.start_time = time.time()
            else:
                if self.went_above:
                    self.end_time = time.time()
                    self.went_bottom_again = True
            self.went_bottom = True
            

        if self.circle.collidepoint(self.car.rect.center) :
            self.went_above = True

        if self.circle3.collidepoint(self.car.rect.center) :
            self.went_left= True
        
        if self.circle4.collidepoint(self.car.rect.center) :
            self.went_right = True

            
        if self.went_bottom and self.went_above and self.went_left and self.went_right and self.went_bottom_again:
            self.car.laps += 1
            self.end_time = time.time()
            self.went_bottom = False
            self.went_above = False
            self.went_left = False
            self.went_right = False
            self.went_bottom_again
            print(f"Finished {self.car.laps} in {round(self.end_time - self.start_time,3)}")
            self.car.add_lap(self.name, f"{round(self.end_time - self.start_time,3)}", self.car.laps)
        #print(self.car.laps)

    def get_car_mask(self):
        # Convert the car image to a more suitable format for faster blitting
        carimg = self.car.image.convert()
        carimg.set_colorkey((0,0,0))

        self.carimg = carimg
        self.car_mask = pygame.mask.from_surface(self.carimg)