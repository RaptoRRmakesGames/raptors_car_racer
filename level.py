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

        self.started = False
        self.time = 4
        self.time_rate = 1000
        self.next_time = pygame.time.get_ticks()

        #self.rect2 = self.circle2.get_rect(topleft=[320, 280])

        self.bcg_color = bcg_color

        self.went_bottom = False
        self.went_bottom_again = False
        self.went_above = False
        self.went_left = False
        self.went_right = False

        self.touching = False

    def update(self, screen):
        time_now = pygame.time.get_ticks()

        self.circle = pygame.Rect(-self.cam.scroll[0], -self.cam.scroll[1],1000*1.3,150*1.3
            
        )

        self.circle2 = pygame.Rect(440-self.cam.scroll[0], 920-self.cam.scroll[1],150*1.3,150*1.3)

        self.circle3 = pygame.Rect(-self.cam.scroll[0], 0-self.cam.scroll[1],150*1.3,1000*1.3)

        self.circle4 = pygame.Rect(1000-self.cam.scroll[0], 0-self.cam.scroll[1],150*1.3,1000*1.3)

        self.x = 0 - self.cam.scroll[0]
        self.y = 0 - self.cam.scroll[1]

        self.offset = (self.car.rect.x - self.x, self.car.rect.y - self.y)
        overlap = self.bcg_mask.overlap_mask(self.car_mask, self.offset)  

        screen.fill(self.bcg_color)
        screen.blit(self.road.convert_alpha(), (self.x, self.y))

        #print(overlap.count())

        #screen.blit(overlap.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,255,255,255)), (self.x, self.y))

        if overlap.count() < 180:
            self.car.out = True
        else:
            self.car.out = False

        if not self.started:
            self.car.starting = True
        else:
            self.car.starting = False

        if self.time > -1:
            if self.time == 0:
                ui.write(screen, f"GO", (400,300), 50,(0,255,0), pygame.font.SysFont("Arial",150,True, False))
            else:
                ui.write(screen, f"{self.time}", (400,300), 50,(255,255,255), pygame.font.SysFont("Arial",150,True, False))
            if time_now > self.next_time:
                self.time -= 1
                print(self.time)
                self.next_time = time_now + self.time_rate
                if self.time == 0:
                    self.started = True
                    self.car.starting = False

        self.check_level_complete()
        # self.draw_circles(screen)

    def get_car_mask(self):
        carimg = self.car.image.convert()
        carimg.set_colorkey((0,0,0))

        self.carimg = carimg
        self.car_mask = pygame.mask.from_surface(self.carimg)

    def reset(self):
        self.started = False
        self.time = 4
        self.time_rate = 1000
        self.next_time = pygame.time.get_ticks()

    def draw_circles(self, screen):
        
        pygame.draw.rect(
            screen, (255,126,12),
            self.circle
        )
        pygame.draw.rect(
            screen, (255,126,12),
            self.circle2
        )
        pygame.draw.rect(
            screen, (255,126,12),
            self.circle3
        )
        pygame.draw.rect(
            screen, (255,126,12),
            self.circle4
        )
    
    def check_level_complete(self):

        if self.circle2.collidepoint(self.car.rect.center): # --> START POINT 

            self.touching = True
            if not self.went_bottom and self.started:
                self.went_bottom = True
                self.start_time = time.time()
                print("bottom 1")
            if not self.went_bottom_again and self.went_above:
                self.went_bottom_again = True
                self.end_time = time.time()
                print("bottom 2")
        else:
            self.touching = False

        if self.circle.collidepoint(self.car.rect.center) : # --> ABOVE POINT 
            self.went_above = True
            print("up")

        if self.circle3.collidepoint(self.car.rect.center) : # --> LEFT POINT 
            self.went_left= True
            print("left")
        
        if self.circle4.collidepoint(self.car.rect.center) : # --> RIGHT POINT 
            self.went_right = True
            print("right")

            
        if self.went_bottom and self.went_above and self.went_left and self.went_right and self.went_bottom_again:
            self.car.laps += 1
            #self.end_time = time.time()
            self.went_bottom = False
            self.went_above = False
            self.went_left = False
            self.went_right = False
            self.went_bottom_again = False
            print(f"Finished {self.car.laps} in {round(self.end_time - self.start_time,3)}")
            self.car.add_lap(self.name, f"{round(self.end_time - self.start_time,3)}", self.car.laps)