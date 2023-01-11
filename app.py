import pygame
from pygame.locals import *
import math, car_file, ui, pySave, camera, level, particles, json
from random import randint, choice,uniform

pygame.init()

# loading stuf from settings.json
with open("settings.json","r") as file:
    settings_dict = json.load(file)
    file.close()

# Basic Variables
screen_width = 1000
screen_height = 1000
fps = settings_dict["fps"]

has_speedo = False
has_car_icon = False
has_particles = False

if settings_dict["speedometer"] == "True":
    has_speedo = True
if settings_dict["car_icon"] == "True":
    has_car_icon = True
if settings_dict["particles"] == "True":
    has_particles = True

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

GAME_NAME = "Budget GTA"

pygame.display.set_caption(GAME_NAME)

cam = camera.Camera(1, screen)

cam.zoom_game(1.2)

stage = "home"

laps = settings_dict["laps"]

money = 0

path = "images/"

# Fonts

bigger = pygame.font.SysFont("Arial", 80, True, False)
big = pygame.font.SysFont("Arial", 60, True, False)
small = pygame.font.SysFont("Arial", 30, True, False)

# Loading Images

images = {
    "background" : {
        0 : pygame.transform.scale(pygame.image.load(path+"map-1.png"), (1000*cam.zoom, 1000*cam.zoom)).convert_alpha(),
        1 : pygame.transform.scale(pygame.image.load(path+"map-2.png"), (1000*cam.zoom, 1000*cam.zoom)).convert_alpha(),
        2 : pygame.transform.scale(pygame.image.load(path+"map-3.png"), (1000*cam.zoom, 1000*cam.zoom)).convert_alpha(),
        3 : pygame.transform.scale(pygame.image.load(path+"map-4.png"), (1000*cam.zoom, 1000*cam.zoom)).convert_alpha(),
    },

    "start" : pygame.transform.scale(pygame.image.load(path+"road_texture.png"), (200, 75)).convert(),
    "start2" : pygame.transform.scale(pygame.image.load(path+"road_texture.png"), (75, 75)).convert(),
    "bugatti chiron" :   pygame.image.load(path+"car.png").convert_alpha(),
    "dodge hellcat" : pygame.image.load(path+"hellcat.png").convert_alpha(),
    "mclaren 720s" : pygame.image.load(path+"mclaren.png").convert_alpha(),
    "aston martin" : pygame.image.load(path+"aston.png").convert_alpha(),
    "lambo avendator" : pygame.image.load(path+"avendator.png").convert_alpha(),
}

# Functionality Functions and Manager classes

# Level Manager class to handle levels more effectively

class LevelManager:
    def __init__(self, levels):
        # You don't need to assign the levels parameter to a new variable with the same name.
        # You can just use self.levels directly.
        self.levels = levels
        self.current_level = 0

        # You can use a list comprehension to create the button_cords and button_args lists.
        self.button_cords = [(x, y) for x in range(400, 601, 100) for y in range(300, 501, 100)]
        self.button_args = list(range(len(self.button_cords)))

        self.button_list = []
        for cord, arg in zip(self.button_cords, self.button_args):
            self.button_list.append(ui.ButtonWithArg(cord, images["start2"], set_level,click_times=1000000000000, arg=arg, text="selectlvl"))

    def set_level(self, lvl):
        self.current_level = lvl
        play_game()

    def update_level(self, screen):
        self.levels[self.current_level].update(screen)

    def update_select_buttons(self, screen):
        for button in self.button_list:
            button.update(int(button.arg), var=str(button.arg))
            button.draw(screen)

def play_game():
    global stage,fps
    player_car.reset()
    stage = "game"
    #fps=80

def level_select():
    global stage,fps
    stage = "level"
    #fps=15

def set_level(level):
    level_m.set_level(level)
    level_m.levels[level_m.current_level].reset()
    player_car.laps = 0
    select_car()
    #play_game()

def select_car():
    global stage,fps
    stage = "select_car"
    #fps=15

# Draws cars to the car selection screen
def blit_cars():
    global index

    car_list[index].blit_icon(screen, middle_car_pos, 1.4)

    if not car_list[index].name in unlocked_car_list:
        ui.write(screen, f"LOCKED", (middle_car_pos[0]- 40, middle_car_pos[1]+400), color = (230,0,0), font=big)
        buy_car_fun.update(car_to_buy,var=f"BUY {car_list[index].cost}$")
        buy_car_fun.draw(screen)
    #print(f"{car_list[index-1].name} - {car_list[index].name} - {car_list[index+1].name}")
    if not index+1 > len(car_list)-1 :
        car_list[index + 1].blit_icon(screen, right_car_pos, 1)
    if index-1 > -1:
        car_list[index - 1].blit_icon(screen, left_car_pos, 1)

    ui.write(screen, f"{car_list[index].name}", (middle_car_pos[0]- 80, middle_car_pos[1]+300), font=big)

def select_car():
    global stage,fps
    stage = "select_car"
    car_group.empty()
    #fps=15

def show_results(level_name):
    global stage,fps,money
    global money_made
    stage = "results"
    best_round = float(min(player_car.performances[level_name]))
    worst_round = float(max(player_car.performances[level_name]))

    money_made = ((worst_round / best_round) *laps)*1000

    money += money_made #((worst_round / best_round) *laps)*80 #w
    # += 
    #fps=15

def write_result_string(level_name):
    
    ui.write(screen, f"{level_name} match results",(150,300), font = bigger )
    ui.write(screen,f"Fastest time - {min(player_car.performances[level_name])}s", (300,400), font=big)
    ui.write(screen,f"Slowest time - {max(player_car.performances[level_name])}s",(300,500), font=big)
    ui.write(screen,
    # f"Money Made - {round(((float(max(player_car.performances[level_name].values( ))) / float(min(player_car.performances[level_name].)))  * laps) * 1000)}$",(300,600),
    f"Money Made - {round(money_made)}$",(300,600), color=(0,223,0) , font = big)


def go_home():
    global stage
    stage = "home"
    player_car.laps = 0 

def buy_car(car):
    global money

    car_obj = cars[car]

    name = car_obj.name
    price = car_obj.cost
    if money >= price:
        money -= price
        unlocked_car_list[name] = 0
        car_obj.bought = True

# Instansiating stuff

# Loads stuff from the save files

currency_save = pySave.Save_Manager("saved_info", "currency")
lap_save = pySave.Save_Manager("saved_info", "laps")
unlocked_cars_save = pySave.Save_Manager("saved_info", "cars")

try:
    unlocked_car_list = unlocked_cars_save.load("cars")
except:
    print("Unlocked cars reset because they werent found in the file")
    unlocked_car_list = {}

try:
    money = currency_save.load("money")
except:
    print("Playing for first time, money is 0")
    money = 0

car_to_buy = "dodge hellcat"

# Instantiating buttons

start_button = ui.Button((500,500), images["start"], play_game,click_times=1000000000000, text="startgame")
select_button = ui.Button((500,600), images["start"], level_select,click_times=1000000000000, text="selectlvl")

quit_result = ui.Button((500,800), images["start"], go_home,click_times=1000000000000 ,text="startgame")

# Creating all the cars in a dictionary
cars = {
    "bugatti chiron" :  car_file.CarSprite(images["bugatti chiron"],    300, 500,   [2.3, 2.5,   3.2],      0.014,      top_speed=130 ,    name="bugatti chiron",     rotations=360, camera=cam,   price=50_000),
    "dodge hellcat" :   car_file.CarSprite(images["dodge hellcat"],    300, 500,   [2.6, 2.9, 3.3],    0.01,       top_speed=150 ,    name="dodge hellcat"   ,   rotations=360, camera=cam,   price=0),
    "mclaren 720s" :    car_file.CarSprite(images["mclaren 720s"],    300, 500,   [2.3, 2.6, 3],      0.0101,     top_speed=170 ,    name="mclaren 720s"     ,  rotations=360, camera=cam,   price=10_000),
    "aston martin" :    car_file.CarSprite(images["aston martin"],      300, 500,   [2.3, 2.6, 3],      0.012,      top_speed=172 ,    name="aston martin"       ,rotations=360, camera=cam,   price=18_000),
    "lambo avendator" : car_file.CarSprite(images["lambo avendator"],  300, 500,   [2.2, 2.5, 2.9],    0.014,      top_speed=150 ,    name="lambo avendator",    rotations=360, camera=cam,   price = 42_000)
}

# Adding the cars to a list for easier iteration, also in order of highest price
car_list = [
    cars["dodge hellcat"],
    cars["mclaren 720s"],
    cars["aston martin"],
    cars["lambo avendator"],
    cars["bugatti chiron"],
]

# Check all cars if they are bought
for car in car_list:
    if car.name in unlocked_car_list:
        car.bought = True
        print(car.name, car.bought)

# Blit positions for all cars in the buy car stage

left_car_pos = (screen_height // 2- 450, screen_width // 2 - 125)

middle_car_pos = (screen_width // 2 - 75 , screen_height // 2 - 150)

right_car_pos = (screen_height // 2+ 350, screen_width // 2 - 125)

# Button that redirects player to buy_car stage
buy_car_fun = ui.ButtonWithArg(
    (middle_car_pos[0]+60, middle_car_pos[1] + 500),
    images["start"],
    buy_car,
    arg=car_to_buy,
    click_times=100000000000000,
    text="scr",
)

# setting player_car index, selected car string and player_car
index = 0

selected_car = "dodge hellcat"

carname = cars[selected_car]
player_car = carname

# setting the levels with the Level Manager and creating a public variable that determines the level
level_m = LevelManager({
    0 : level.Level(images["background"][0], player_car,cam, screen,  "Cold Valley",        pos = (0,100)),
    1 : level.Level(images["background"][1], player_car,cam, screen,  "Roundy Street",      pos = (0,100)),
    2 : level.Level(images["background"][2], player_car,cam, screen,  "Drifter's Heaven",   pos = (0,100)),
    3 : level.Level(images["background"][3], player_car,cam, screen,  "3 Quarters Devil",   pos = (0,100)),
}) 

level = 0 

# creating the particle manager 
pm = particles.Particle_Manager(cam)

# Groups and Lists

car_group = pygame.sprite.Group()

# Adding to Groups 

car_group.add(player_car)

# Game Functions
def render():
    global player_car


    # Code for "home" stage
    if stage == "home":
        screen.fill((255,255,255))

        # write the game name, balance and update buttons
        ui.write(screen, f"Money - {money}$", (screen_width //2 - 120,300),color=(0,223,0),font=big)

        ui.write(screen, f"{GAME_NAME.upper()}", (screen_width //2 - 210,100),font=bigger)

        if cars["dodge hellcat"].bought:
            start_button.update("Quick Play")
            start_button.draw(screen)

        select_button.update("Select Level")
        select_button.draw(screen)

    
    # code for "game" stage
    if stage == "game":
        
        # handling particles

        # particles for drifting without boost
        if pygame.key.get_pressed()[K_SPACE] and not player_car.blue_fire:
            pm.create_particle(
                
                (player_car.rect.center),
                (0,0),
                8 * cam.zoom,
                0.2,
                (255,255,255),
                custom_death_meter=4)

        # particles for boost
        if player_car.blue_fire:
            pm.create_particle(
            
            (player_car.rect.center),
            (0,0),
            8 * cam.zoom,
            0.2,
            (255,25,25),
            custom_death_meter=4)

        # boom particle for when player exceeds certain speed
        
        if player_car.boom_effect:
            for i in range(2):
                pm.create_particle(
                
                    (player_car.rect.center),
                    (uniform(-3,3)- choice([1,-1]),uniform(-3,3)- choice([1,-1])),
                    8 * cam.zoom,
                    0.1,
                    (23,255,195),
                    custom_death_meter=0)

        # kinda useless line of code that makes sure the correct car is being displayed/rendered
        if not player_car is carname:
            player_car = carname

        # Drawing proccess begins here
        # Update the level/clear the canvas
        level_m.update_level(screen)

        # write the fps, update particles, car, make the camera follow the car 
        # and setting the stage to "results" if player completes all the laps
        ui.write(screen,f"{round(clock.get_fps(), 2)}FPS",(10,10), color=(255,255,255), font = small)
        

        if has_particles:
            pm.update_particles(screen)

        car_group.update(screen)
        car_group.draw(screen)

        if has_speedo:
        
            player_car.show_speedometer(screen)

        if has_car_icon:
            screen.blit(player_car.show_image, (910,780))

        cam.follow(player_car)
        

        if player_car.laps > laps:
            show_results(level_m.levels[level_m.current_level].name)

    # Code for "level" stage
    if stage == "level":
        
        # Clearing the Canvas, updating the buttons and writing the headline

        screen.fill((255,255,255))
        level_m.update_select_buttons(screen)
        ui.write(screen, "Select Level:", (360,150), font = bigger)

    # code for "select_car" or "buy_car" stage
    if stage == "select_car": 

        # clearing the canvas and writing headlines and balance
        screen.fill((220,222,236))

        ui.write(screen, f"Money - {money}$", (10,10),color=(0,223,0), font = big)

        ui.write(screen, "Select Car", (screen_width//2-140,150), font = bigger)
        
        # blits the cars in the right index. Controls are in the event handler
        blit_cars()


    # code for "results" stage
    if stage == "results":
        
        # clearing the canvas
        screen.fill((220,222,236))

        # show the results, money
        write_result_string(level_m.levels[level_m.current_level].name)
        ui.write(screen, f"Money - {money}$", (10,10),color=(0,223,0), font = big)

        # update the button to go home
        quit_result.update("Main Menu")
        quit_result.draw(screen)

        # kinda useless code that ensures the go home button has the correct function assigned 
        if not quit_result.function is go_home:
            quit_result.function = go_home

# empty function for collisions
def collisions():
    pass

# reseting the car before the game begins
player_car.reset()

run = True
while run:

    # ticking clock. Using "tick_busy_loop" rather than "tick" because it gives better performance
    clock.tick_busy_loop(fps)

    # rounding the amount of money player has to ensure the lack of decimals
    if money != round(money):
        money = round(money)

    # kinda useless piece of code that ensures that "select_car" is equal to the correct car name from the list according to the index
    if select_car is not car_list[index].name:
        selected_car = car_list[index].name

    # Prints for debugging and stuff



    # calling render and collisions functions
    render()
    collisions()

    # Event Handler

    for event in pygame.event.get():
        # closes the game if the "X" is pressed. Provides a short summary of what happened in the game aswell as saves data that has to be saved

        if event.type == QUIT:
            run = False
            currency_save.save("money", round(money))

            lap_save.save("performances", player_car.performances)

            unlocked_cars_save.save("cars", unlocked_car_list)

            currency_save.apply()
            lap_save.apply()
            unlocked_cars_save.apply()
            print(f"Quit with {round(clock.get_fps(), 2)} FPS")
            print(player_car.performances)
            quit()
        
        # Button Handler

        if event.type == KEYDOWN:
            # Sets the stage to select level if "r" is pressed
            if event.key == K_r:
                level_select()

            # Code for controlling the car index in the "select_car" stage
            if stage == "select_car":

                # adding or subtracting one from the index if right or left arrow key is pressed
                if event.key == K_RIGHT and index < len(car_list) -1 :
                    index += 1
                    car_to_buy = car_list[index].name
                    print(car_list[index].name)

                if event.key == K_LEFT and index > 0:
                    index -= 1
                    car_to_buy = car_list[index].name
                    print(car_list[index].name)

                # if the right enter button is hit, it tries to set carname to the car selected by the index in the car list
                # if that gives a NameError it means that the player is choosing quickplay rather than level select so it 
                # lets it go.
                # Then it checks if the car has been bought and if yes, sets player_car (which is the variable where i keep
                # the car the player is controlling, followed by the screen and creates particles for. Also resets this car
                # because which means 0-ing the velocity and speed, setting the position to the starting position and 
                # rotating it to the correct radians. Also adds the car to the car_group again, but car_group is cleared 
                # before entering this stage. from here the game starts. 
                # If the selected car is not bought an error message pops up for half a second
                if event.key == K_RETURN:
                    

                    try:
                        carname = car_list[index]

                        if carname.bought:

                            selected_car = car_list[index].name

                            player_car= cars[selected_car]
                            player_car.reset()
                       
                            car_group.add(player_car)
                            print(player_car.name)
                            for level in level_m.levels:
                                level_m.levels[level].car = player_car 

                            #reset_car()
                    
                            stage = "game"
                        else:
                            ui.write(screen, "ERROR", (400,200), font = big)
                        #print()
                    except NameError:
                        print("quick play")

    pygame.display.update()
