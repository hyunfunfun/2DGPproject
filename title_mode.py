from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time
from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import select_mode
import game_framework

def init():
    global image
    image=load_image('./resource\\start\\title1.png')
    pass

def finish():
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(450,300)
    update_canvas()
    pass

def handle_events():
    events=get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(select_mode)
    pass

