from pico2d import load_image, clear_canvas, update_canvas, get_events, SDLK_LEFT, SDLK_RIGHT
from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import play_mode
import game_world
import game_framework
from hero1 import Hero1
from hero2 import Hero2

def init():
    global Hero1_image
    global Hero2_image
    global Hero3_image
    global Hero4_image
    global selector
    global selector_count
    Hero1_image=load_image('./resource\\chpic\\Hero1_pic.jpg')
    Hero2_image = load_image('./resource\\chpic\\Hero2_pic.jpg')
    Hero3_image = load_image('./resource\\chpic\\Hero3_pic.jpg')
    Hero4_image = load_image('./resource\\chpic\\Hero4_pic.jpg')
    selector = load_image('./resource\\icon\\selector.png')
    selector_count=1
    pass

def finish():
    pass

def update():
    game_world.update()

def draw():
    clear_canvas()
    selector.draw(200*selector_count-50,350)
    Hero1_image.draw(150,200)
    Hero2_image.draw(350,200)
    Hero3_image.draw(550,200)
    Hero4_image.draw(750,200)
    update_canvas()
    pass

def handle_events():
    global hero
    global selector_count
    events=get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            play_mode.create_hero(selector_count)
            game_framework.change_mode(play_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if selector_count<4:
                selector_count+=1
            else:
                selector_count=1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if selector_count>1:
                selector_count-=1
            else:
                selector_count=4

