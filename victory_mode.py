from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time
from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import select_mode
import game_framework
import title_mode

def init():
    global victory1_image
    global victory2_image
    global victory3_image
    global victory4_image

    victory1_image=load_image('./resource\\start\\victory1.png')
    victory2_image = load_image('./resource\\start\\victory2.png')
    victory3_image = load_image('./resource\\start\\victory3.png')
    victory4_image = load_image('./resource\\start\\victory4.png')
    pass

def finish():
    pass

def update():
    pass

def draw():
    clear_canvas()
    if select_mode.selector_count==1:
        victory1_image.draw(500,250)
    elif select_mode.selector_count==2:
        victory2_image.draw(500,250)
    elif select_mode.selector_count==3:
        victory3_image.draw(500,250)
    elif select_mode.selector_count==4:
        victory4_image.draw(500,250)
    update_canvas()
    pass

def handle_events():
    events=get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(title_mode)
    pass

