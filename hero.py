# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, clamp
from sdl2 import SDLK_UP, SDLK_DOWN
from arrow import Arrow
import game_world
import game_framework

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'
# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


class Idle:

    @staticmethod
    def enter(hero, e):
        hero.dir = 0
        hero.frame = 0
        pass

    @staticmethod
    def exit(hero, e):
        if space_down(e):
            pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(hero):
        hero.idle_image.clip_draw(int(hero.frame) * 120, 0, 60, 80, hero.x, hero.y)



class Attack:
    @staticmethod
    def enter(hero, e):
        if hero.attack_count>4:
            hero.attack_count=0
        hero.frame = (hero.frame + 1) % 3
        hero.dir=1

    @staticmethod
    def exit(hero, e):
        hero.attack_count+=1
        if space_down(e):
            pass

    @staticmethod
    def do(hero):
        if(hero.attack_count>=3):
            hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    @staticmethod
    def draw(hero):
        if hero.attack_count<3:
            hero.attack_ready_image.clip_draw(int(hero.frame) * 120, 0, 60, 90, hero.x, hero.y)
        else:
            hero.attack_image.clip_draw(int(hero.frame) * 120, 0, 100, 90, hero.x, hero.y)

class Retreat:

    @staticmethod
    def enter(hero, e):
        hero.frame=0
        hero.dir=-1
        hero.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(hero, e):
        if space_down(e):
            pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        hero.x = clamp(25, hero.x, 1600 - 25)
        if get_time() - hero.wait_time > 0.5:
            hero.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(hero):
        hero.retreat_image.clip_draw(int(hero.frame) * 70, 0, 50, 90, hero.x, hero.y)


class StateMachine:
    def __init__(self, hero):
        self.hero = hero
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Attack, left_down: Attack, up_down: Attack, down_down : Attack, space_down: Retreat},
            Attack: {right_down: Attack, left_down: Attack, up_down: Attack, down_down : Attack , space_down: Retreat},
            Retreat:{time_out:Idle}
        }

    def start(self):
        self.cur_state.enter(self.hero, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.hero)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hero, e)
                self.cur_state = next_state
                self.cur_state.enter(self.hero, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.hero)





class Hero:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.idle_image = load_image('./resource\\character\\Hero1\\Hero1_idle.png')
        self.attack_ready_image = load_image(
            './resource\\character\\Hero1\\Hero1_attack_ready.png')
        self.retreat_image = load_image(
            './resource\\character\\Hero1\\Hero1_retreat.png')
        self.attack_image=load_image('./resource\\character\\Hero1\\Hero1_attack.png')
        self.attack_count=0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.item = None
        self.arrow = [Arrow(n) for n in range(4)]
        game_world.add_objects(self.arrow, 2)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()