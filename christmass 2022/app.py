import pygame
from pygame.locals import *
from random import choice, randint 
import math, car, ui, pySave, camera, level

pygame.init()

# Basic Variables
screen_width = 1000
screen_height = 1000
fps = 80

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

cam = camera.Camera(1, screen)
#cam.zoom_game(1.55)

stage = "home"

# Loading Images

images = {
    "start" : pygame.transform.scale(pygame.image.load("road_texture.png"), (200*cam.zoom, 75*cam.zoom)).convert_alpha(),
    "bcg" : pygame.transform.scale(pygame.image.load("map2.png"), (1000*cam.zoom, 1000*cam.zoom)).convert_alpha(),
    "car" : pygame.image.load("car.png").convert_alpha()
}

# Functionality Functions

def play_game():
    global stage
    stage = "game"

# Instansiating stuff

pos_save = pySave.Save_Manager("saved_info", "pos")

start_button = ui.Button((500,500), images["start"], play_game, text="startgame")

test_car = car.CarSprite(images["car"], 400, 400,[2, 2.3, 2.7], 0.013, rotations=360, camera=cam)

speedometer = ui.TextWithBackground((100,50), (100,950), images["start"])

level = level.Level(images["bcg"], test_car,cam,pos = (0,100))

# Groups and Lists

car_group = pygame.sprite.Group()

# Adding to Groups 

car_group.add(test_car)

# Game Functions
def render():
    
    if stage == "home":
        
        screen.fill((255,255,255))
        start_button.update("Start Game")
        start_button.draw(screen)
        
    elif stage == "game":

        screen.fill((0,76,18))
        level.update(screen)#screen.blit(images["bcg"], (0-cam.scroll[0],0-cam.scroll[1]))

        car_group.update()
        car_group.draw(screen)

        #cam.follow(test_car, )

        #speedometer.draw(screen)
        speedometer.update(screen,round(test_car.speed*60,2) , " km/h")
        #cam.zoom_game(2)


def collisions():
    pass

run = True
while run:

    clock.tick_busy_loop(80)

    render()
    collisions()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False


            pos_save.save("x", test_car.rect.x)
            pos_save.save("y", test_car.rect.y)

            pos_save.apply()

            print(f"Quit with {round(clock.get_fps(), 2)} FPS")

            quit()

    pygame.display.update()