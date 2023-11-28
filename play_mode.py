from pico2d import *
import random
import title_mode
import winlose_mode
import game_framework
import game_world
from hero1 import Hero1
from hero2 import Hero2
from hero3 import Hero3
from hero4 import Hero4

from enemy1 import Enemy1

from score import Score
from timer import Timer
from background import Background
from arrow import Arrow


# Game object class here


def init():
    global running
    global background
    global team
    global timer
    global enemy
    global score
    global arrow

    running = True

    background=Background(4)
    game_world.add_object(background, 0)

    # create_hero()

    score=Score()
    game_world.add_object(score, 2)

    timer = Timer()
    game_world.add_object(timer,2)

    enemy=Enemy1()
    game_world.add_object(enemy,1)

    hero.create_arrow()

    game_world.add_collision_pairs('hero:enemy', None, enemy)
    game_world.add_collision_pairs('enemy:hero',enemy,None)


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            hero.handle_event(event)


def create_hero(n):
    global hero
    if n==1:
        hero = Hero1()
    elif n==2:
        hero = Hero2()
    elif n==3:
        hero = Hero3()
    elif n==4:
        hero = Hero4()
    game_world.add_object(hero, 1)
    game_world.add_collision_pairs('hero:enemy', hero, None)
    game_world.add_collision_pairs('enemy:hero', None, hero)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    if timer.ten_frame >= 1:
        print('time_out')
        game_framework.push_mode(winlose_mode)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass