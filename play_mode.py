from pico2d import *
import random
import title_mode
import game_framework
import game_world
from grass import Grass
from hero import Hero
from timer import Timer
from arrow import Arrow


# Game object class here


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            hero.handle_event(event)


def init():
    global running
    global grass
    global team
    global hero
    global timer

    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    hero = Hero()
    game_world.add_object(hero, 1)

    timer = Timer()
    game_world.add_object(timer,2)

    hero.create_arrow()


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
    pass

def resume():
    pass