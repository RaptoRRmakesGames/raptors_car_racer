import pygame
from pygame.locals import *
from random import choice, randint 

class Button:
    def __init__(self, pos, image, action, click_times=1, dissapear=True , text="", textcolor = (255,255,255), fontsize=30):
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        self.clicked = False
        self.clicked_times = click_times
        self.dissapear = dissapear
        self.dont_draw = False

        self.force_click = False

        self.function = action

        self.text= text

        if not self.text == "":
            self.font = pygame.font.SysFont("Arial", fontsize, False, False)
            self.color = textcolor


    def update(self, var=""):
        pressed = pygame.mouse.get_pressed()[0]
        if not self.text == "":
            self.text = self.font.render(f"{var}", 1, self.color)
            self.text_rect = self.text.get_rect(center = self.rect.center)

        if pressed and not self.clicked and not self.clicked_times <= 0 and self.rect.collidepoint(pygame.mouse.get_pos()) or self.force_click:
            self.function()
            self.clicked = True
            self.clicked_times -= 1
            self.force_click = False

        if not pressed:
            self.clicked = False

        if self.clicked_times <= 0:
            if self.dissapear:
                self.dont_draw = True

    def draw(self, screen):

        if not self.dont_draw:
            screen.blit(self.image, (self.rect.x,self.rect.y))
            screen.blit(self.text, (self.text_rect.x, self.text_rect.y))

class ButtonWithArg:
    def __init__(self, pos, image, action,arg=0 ,click_times=1, dissapear=True , text="", textcolor = (255,255,255), fontsize=30):
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        self.clicked = False
        self.clicked_times = click_times
        self.dissapear = dissapear
        self.dont_draw = False

        self.arg = arg

        self.function = action

        self.text= text

        if not self.text == "":
            self.font = pygame.font.SysFont("Arial", fontsize, False, False)
            self.color = textcolor


    def update(self,arg ,var=""):
        if self.arg != arg:
            self.arg = arg
        pressed = pygame.mouse.get_pressed()[0]
        if not self.text == "":
            self.text = self.font.render(f"{var}", 1, self.color)
            self.text_rect = self.text.get_rect(center = self.rect.center)

        if pressed and not self.clicked and not self.clicked_times <= 0 and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.function(self.arg)
            self.clicked = True
            self.clicked_times -= 1
            print("clicked")

        if not pressed:
            self.clicked = False

        if self.clicked_times <= 0:
            if self.dissapear:
                self.dont_draw = True

    def draw(self, screen):

        #if not self.dont_draw:
        screen.blit(self.image, (self.rect.x,self.rect.y))
        screen.blit(self.text, (self.text_rect.x, self.text_rect.y))

class TextWithBackground:
    def __init__(self, image_size, pos, image, fontsize=30, colour=(255, 255, 255)):
        self.image = pygame.transform.scale(image, image_size)
        self.rect = self.image.get_rect(center=pos)
        self.font = pygame.font.SysFont("Arial", fontsize, False, False)
        self.color = colour
        self.text = self.font.render("", 1, self.color)
        self.other_text = None
        self.other_rect = None

    def update(self, screen, variable, othertext=""):
        self.text = self.font.render(f"{variable}", 1, self.color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

        if othertext:
            self.other_text = self.font.render(f"{othertext}", 1, self.color)
            self.other_rect = self.other_text.get_rect(topleft=(self.rect.center[0] - 5, self.rect.center[1] - 5))

        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text, (self.rect.x, self.rect.y))
        if self.other_text:
            screen.blit(self.other_text, (self.other_rect.x, self.other_rect.y))

pygame.init()

# font = pygame.font.SysFont(font, size, True, False)
def write(screen,text, pos,size=60,color=(0,0,0),font=pygame.font.SysFont("Arial",60,True,False)):
    screen.blit(
        font.render(text, 1, color),
        pos
    )