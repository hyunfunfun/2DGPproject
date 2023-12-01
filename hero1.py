# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, clamp, \
    draw_rectangle, SDLK_LSHIFT
from sdl2 import SDLK_UP, SDLK_DOWN
from arrow import Arrow
import game_world
import game_framework
import play_mode

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

def lshift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

def time_out(e):
    return e[0] == 'TIME_OUT'

def attack(e):
    return e[0] == 'Attack'

def die(e):
    return e[0] == 'Die'


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

TIME_PER_ATTACK = 1
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ACTION1 = 2

FRAMES_PER_ATTACK = ATTACK_PER_TIME * FRAMES_PER_ACTION1

TIME_PER_DIE = 1.5
DIE_PER_TIME = 1.0 / TIME_PER_DIE
FRAMES_PER_DIE = 3

FRAMES_PER_DIE = DIE_PER_TIME * FRAMES_PER_DIE

class Idle:

    @staticmethod
    def enter(hero, e):
        if hero.attack_count>0:
            for n in range(hero.attack_count, 4):
                hero.remove_arrow(n)
            hero.create_arrow()
        hero.attack_count=0
        hero.dir = 0
        hero.frame = 0
        pass

    @staticmethod
    def exit(hero, e):
        if space_down(e):
            pass

    @staticmethod
    def do(hero):
        if hero.lose:
            hero.state_machine.handle_event(('Die', 0))
        else:
            hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(hero):
        hero.idle_image.clip_draw(int(hero.frame) * 120, 0, 60, 80, hero.x, hero.y,100,100)



class Attack_ready:
    @staticmethod
    def enter(hero, e):
        hero.remove_arrow(hero.attack_count)
        hero.wait_time = get_time()
        hero.frame = (hero.frame + 1) % 3
        hero.attack_count += 1
        hero.dir=1

    @staticmethod
    def exit(hero, e):
        if space_down(e):
            pass

    @staticmethod
    def do(hero):
        if hero.lose:
            hero.state_machine.handle_event(('Die', 0))
        if hero.attack_count >= 4:
            hero.attack_count = 0
            hero.state_machine.handle_event(('Attack', 0))
        if get_time() - hero.wait_time > 1:
            hero.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hero):
        hero.attack_ready_image.clip_draw(int(hero.frame) * 120, 0, 60, 90, hero.x, hero.y,100,100)


class Attack:
    @staticmethod
    def enter(hero, e):
        hero.attack_range = 70
        hero.attack_count = 0
        hero.frame = 0
        hero.wait_time = get_time()
        hero.dir=1

    @staticmethod
    def exit(hero, e):
        hero.attack_range = -100
        hero.create_arrow()
        if space_down(e):
            pass

    @staticmethod
    def do(hero):
        hero.frame=(hero.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 2
        if hero.lose:
            hero.state_machine.handle_event(('Die', 0))
        if hero.frame>1:
            hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - hero.wait_time > 1:
            hero.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hero):
        hero.attack_image.clip_draw(int(hero.frame) * 120, 0, 100, 90, hero.x, hero.y,130,100)

class Retreat:

    @staticmethod
    def enter(hero, e):
        if hero.attack_count>0:
            for n in range(hero.attack_count, 4):
                hero.remove_arrow(n)
            hero.create_arrow()
        hero.attack_count=0
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
        if hero.lose:
            hero.state_machine.handle_event(('Die', 0))
        if hero.x <= 100:
            hero.lose=True
            hero.attack_count = 0
            hero.state_machine.handle_event(('Die', 0))
        elif get_time() - hero.wait_time > 0.5:
            hero.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(hero):
        hero.retreat_image.clip_draw(int(hero.frame) * 65, 0, 50, 90, hero.x, hero.y,100,100)

class Defense:
    @staticmethod
    def enter(hero, e):
        if hero.attack_count>0:
            for n in range(hero.attack_count, 4):
                hero.remove_arrow(n)
            hero.create_arrow()
        hero.attack_count=0
        hero.frame=0
        hero.dir=-1
        hero.wait_time = get_time()  # pico2d import 필요
        hero.defense_per=random.randint(0,5)
        pass

    @staticmethod
    def exit(hero, e):
        if space_down(e):
            pass

    @staticmethod
    def do(hero):
        if hero.defense_per>0:
            if (play_mode.enemy.x - hero.x)<130:
                play_mode.enemy.x = hero.x+130
        if hero.lose:
            hero.state_machine.handle_event(('Die', 0))
        elif get_time() - hero.wait_time > 1:
            hero.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(hero):
        hero.defense_image.clip_draw(0, 0, 60, 90, hero.x, hero.y,100,100)


class Die:
    @staticmethod
    def enter(hero, e):
        play_mode.score.enemy_score += 1
        game_world.remove_collision_object(hero)
        hero.frame = 0
        hero.dir=-1
        hero.wait_time = get_time()

    @staticmethod
    def exit(hero, e):
        game_world.add_collision_pairs('hero:enemy', hero, None)
        game_world.add_collision_pairs('enemy:hero', None, hero)
        hero.x, hero.y = 200, 150
        play_mode.enemy.x, play_mode.enemy.y = 700, 150
        hero.lose=False
        if space_down(e):
            pass

    @staticmethod
    def do(hero):
        hero.frame=(hero.frame + FRAMES_PER_DIE * DIE_PER_TIME * game_framework.frame_time) % 3
        # if hero.frame>1:
        #     hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - hero.wait_time > 2:
            hero.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hero):
        hero.die_image.clip_draw(int(hero.frame) * 65, 0, 65, 90, hero.x, hero.y,100,100)



class StateMachine:
    def __init__(self, hero):
        self.attack_count=0
        self.hero = hero
        self.cur_state = Idle
        self.transitions = {
            Idle: {lshift_down:Defense,right_down: Attack_ready, left_down: Attack_ready, up_down: Attack_ready, down_down : Attack_ready,space_down: Retreat, die:Die},
            Attack_ready: {lshift_down:Defense,right_down: Attack_ready, left_down: Attack_ready, up_down: Attack_ready, down_down : Attack_ready , space_down: Retreat, attack:Attack, time_out:Idle,die:Die},
            Attack:{time_out:Idle, die:Die},
            Defense:{time_out:Idle, die:Die},
            Retreat:{time_out:Idle, die:Die},
            Die:{time_out:Idle}
        }

    def start(self):
        self.cur_state.enter(self.hero, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.hero)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                if next_state==Attack_ready and check_event==up_down and self.hero.arrow_dir[self.attack_count]==0:
                    self.attack_count += 1
                    self.state_change(e, next_state)
                    return True
                elif next_state==Attack_ready and check_event==down_down and self.hero.arrow_dir[self.attack_count]==1:
                    self.attack_count += 1
                    self.state_change(e, next_state)
                    return True
                elif next_state==Attack_ready and check_event==left_down and self.hero.arrow_dir[self.attack_count]==2:
                    self.attack_count += 1
                    self.state_change(e, next_state)
                    return True
                elif next_state==Attack_ready and check_event==right_down and self.hero.arrow_dir[self.attack_count]==3:
                    self.attack_count += 1
                    self.state_change(e, next_state)
                    return True
                elif next_state==Attack:
                    self.state_change(e, next_state)
                    self.attack_count = 0
                elif next_state!=Attack_ready:
                    self.attack_count = 0
                    self.state_change(e, next_state)
                    return True
                else:
                    return False

        return False

    def state_change(self, e, next_state):
        self.cur_state.exit(self.hero, e)
        self.cur_state = next_state
        self.cur_state.enter(self.hero, e)

    def draw(self):
        self.cur_state.draw(self.hero)


class Hero1:
    def __init__(self):
        self.win_count=4
        self.x, self.y = 200, 150
        self.frame = 0
        self.dir = 0
        self.attack_count=0
        self.arrow_dir=[n for n in range(4)]
        self.attack_range = -100
        self.lose=False
        self.defense_per=0

        self.idle_image = load_image('./resource\\character\\Hero1\\Hero1_idle.png')
        self.attack_ready_image = load_image(
            './resource\\character\\Hero1\\Hero1_attack_ready.png')
        self.retreat_image = load_image(
            './resource\\character\\Hero1\\Hero1_retreat.png')
        self.attack_image=load_image('./resource\\character\\Hero1\\Hero1_attack.png')
        self.die_image=load_image('./resource\\character\\Hero1\\Hero1_die.png')
        self.defense_image=load_image('./resource\\character\\Hero1\\Hero1_defense.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()


        # self.item = None

    def create_arrow(self):
        global arrow
        random.shuffle(self.arrow_dir)
        arrow = [Arrow(n,self.arrow_dir[n]) for n in range(4)]
        game_world.add_objects(arrow, 2)

    def remove_arrow(self,n):
        game_world.remove_object(arrow[n])
        pass

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.attack_bb())  # 튜플을 풀어서 인자로 전달
        draw_rectangle(*self.get_bb())  # 튜플을 풀어서 인자로 전달

    def attack_bb(self):
        return self.x-40,self.y-20,self.x+self.attack_range,self.y+0

    def get_bb(self):
        return self.x -40,self.y-60,self.x+30,self.y+50

    def handle_collision(self,group,other):
        if group == 'enemy:hero':
            self.lose=True
            game_world.remove_collision_object(self)
        if group == 'hero:enemy':
            pass
