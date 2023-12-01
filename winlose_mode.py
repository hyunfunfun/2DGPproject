from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time, pico2d
from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_QUIT

import play_mode
from win import Win
from lose import Lose
import game_world
import game_framework

def init():
    global win
    global lose
    global check
    global stage
    if play_mode.score.hero_score>play_mode.score.enemy_score:

        win=Win()
        game_world.add_object(win,3)
        check=True
    if play_mode.score.enemy_score>=play_mode.score.hero_score:
        lose=Lose()
        game_world.add_object(lose, 3)
        check=False
    pass

def finish():
    global stage
    if check==True:
        game_world.remove_object(win)
        game_world.remove_object(play_mode.background)
        play_mode.hero.win_count+=1;
        if play_mode.hero.win_count>4:
            pass#승리화면이동
        play_mode.create_background(play_mode.hero.win_count)
    else :
        game_world.remove_object(lose)
    game_world.remove_object(play_mode.timer)
    game_world.remove_object(play_mode.enemy)
    game_world.remove_object(play_mode.score)
    play_mode.hero.x, play_mode.hero.y = 200, 150
    play_mode.enemy.x, play_mode.enemy.y = 700, 150
    for n in range(play_mode.hero.attack_count, 4):
        play_mode.hero.remove_arrow(n)
    pass

def update():
    game_world.update()
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass

def handle_events():
    events=get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()
