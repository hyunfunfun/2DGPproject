from pico2d import *
import title_mode
import game_framework
import game_world
from grass import Grass
from boy import Boy
from Arrow import Arrow


# Game object class here


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            boy.handle_event(event)


def init():
    global running
    global grass
    global team
    global boy
    global arrow

    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    arrow = Arrow()
    game_world.add_object(arrow,2)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    boy.wait_time = 100000000.0
    pass

def resume():
    boy.wait_time = get_time()
    pass