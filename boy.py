# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, clamp
from sdl2 import SDLK_UP, SDLK_DOWN

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
    def enter(boy, e):
        boy.dir = 0
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(boy):
        boy.idleimage.clip_draw(int(boy.frame) * 120, 0, 60, 80, boy.x, boy.y)



class Attack:

    @staticmethod
    def enter(boy, e):
        boy.frame = (boy.frame + 1) % 3
        boy.dir=1

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        pass

    @staticmethod
    def draw(boy):
        boy.attack_readyimage.clip_draw(int(boy.frame) * 120, 0, 60, 90, boy.x, boy.y)

class Retreat:

    @staticmethod
    def enter(boy, e):
        boy.frame=0
        boy.dir=-1
        boy.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)
        if get_time() - boy.wait_time > 0.5:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(boy):
        boy.reteatimage.clip_draw(int(boy.frame) * 70, 0, 50, 90, boy.x, boy.y)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Attack, left_down: Attack, up_down: Attack, down_down : Attack, space_down: Retreat},
            Attack: {right_down: Attack, left_down: Attack, up_down: Attack, down_down : Attack , space_down: Retreat},
            Retreat:{time_out:Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy)





class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.idle_image = load_image('./resource\\character\\Hero1\\Hero1_idle.png')
        self.attack_ready_image = load_image(
            './resource\\character\\Hero1\\Hero1_attack_ready.png')
        self.rerteat_image = load_image(
            './resource\\character\\Hero1\\Hero1_reteat.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.item = None

        pass

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
