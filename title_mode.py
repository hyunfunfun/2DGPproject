from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time
from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import play_mode
import game_framework

def init():
    global image
    image=load_image('C:\\qudgus\\TUK\\2Grade 2Semester\\2DGP\\2020184009\\2DGPproject\\resource\\start\\title.png')
    pass

def finish():
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(400,300)
    update_canvas()
    pass

def handle_events():
    events=get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)
    pass

