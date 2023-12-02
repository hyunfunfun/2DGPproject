import random
import math
import game_framework
import game_world
import play_mode
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

from pico2d import *

def retreat(e):
    return e[0] == 'Retreat'

def time_out(e):
    return e[0] == 'TIME_OUT'

def attack(e):
    return e[0] == 'Attack'

def attack_ready(e):
    return e[0] == 'Attack_Ready'

def die(e):
    return e[0] == 'Die'

def defense(e):
    return e[0] == 'Defense'

# zombie Run Speed
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
    def enter(enemy, e):
        enemy.defense_range_per=random.randint(0,5)
        enemy.wait_time = get_time()
        enemy.dir = 0
        enemy.frame = 0
        enemy.next_behavior=random.randint(0,4)
        pass

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        if enemy.lose:
            enemy.state_machine.handle_event(('Die', 0))
        if (enemy.x-play_mode.hero.x)<130:
            if enemy.defense_range_per>3:
                enemy.state_machine.handle_event(('Defense', 0))
            elif enemy.next_behavior>1:
                enemy.state_machine.handle_event(('Retreat', 0))
            else :
                enemy.next_behavior=random.randint(0,4)
        if get_time() - enemy.wait_time > 3:
            enemy.state_machine.handle_event(('TIME_OUT', 0))
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(enemy):
        enemy.idle_image.clip_composite_draw(int(enemy.frame) * 120, 0, 70, 80,0,'h', enemy.x, enemy.y,  enemy.size,  enemy.size)

class Attack_ready:
    @staticmethod
    def enter(enemy, e):
        enemy.wait_time = get_time()
        enemy.frame = 0
        enemy.dir=0

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        if (enemy.x-play_mode.hero.x)<130:
            if enemy.defense_range_per>3:
                enemy.state_machine.handle_event(('Defense', 0))
            elif enemy.next_behavior>1:
                enemy.state_machine.handle_event(('Retreat', 0))
            else :
                enemy.next_behavior=random.randint(0,4)
        if enemy.lose:
            enemy.state_machine.handle_event(('Die', 0))
        if get_time() - enemy.wait_time > 0.5:
            enemy.state_machine.handle_event(('TIME_OUT', 0))
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    @staticmethod
    def draw(enemy):
        enemy.attack_ready_image.clip_composite_draw(int(enemy.frame) * 120, 0, 100, 120,0,'h', enemy.x, enemy.y,  enemy.size+10,  enemy.size+10)

class Attack:
    @staticmethod
    def enter(enemy, e):
        enemy.attack_range=80
        enemy.wait_time = get_time()
        enemy.frame = 0
        enemy.dir=-1

    @staticmethod
    def exit(enemy, e):
        enemy.attack_range = -100
        enemy.next_behavior = random.randint(0, 4)
        pass

    @staticmethod
    def do(enemy):
        enemy.frame= (enemy.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 2
        if enemy.lose:
            enemy.state_machine.handle_event(('Die', 0))
        if enemy.frame>1:
            enemy.x += enemy.dir * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - enemy.wait_time > 1:
            enemy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(enemy):
        enemy.attack_image.clip_composite_draw(int(enemy.frame) * 120, 0, 120, 120,0,'h', enemy.x, enemy.y,  enemy.size+30,  enemy.size+10)

class Retreat:

    @staticmethod
    def enter(enemy, e):
        enemy.frame=0
        enemy.dir=-1
        enemy.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        enemy.x -= enemy.dir * RUN_SPEED_PPS * game_framework.frame_time
        if enemy.lose:
            enemy.state_machine.handle_event(('Die', 0))
        if enemy.x >= 900:
            enemy.lose=True
            enemy.state_machine.handle_event(('Die', 0))
        if get_time() - enemy.wait_time > 0.5:
            enemy.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(enemy):
        enemy.retreat_image.clip_composite_draw(int(enemy.frame) * 55, 0, 55, 90,0,'h', enemy.x, enemy.y,  enemy.size,  enemy.size)


class Defense:
    @staticmethod
    def enter(enemy, e):
        enemy.frame=0
        enemy.dir=-1
        enemy.wait_time = get_time()  # pico2d import 필요
        enemy.defense_per=random.randint(0, 5)
        pass

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        if enemy.defense_per>1:
            if (enemy.x - play_mode.hero.x)<130:
                play_mode.hero.x = enemy.x - 130
        if enemy.lose:
            enemy.state_machine.handle_event(('Die', 0))
        elif get_time() - enemy.wait_time > 1:
            enemy.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(enemy):
        enemy.defense_image.clip_composite_draw(0, 0, 60, 90,0,'h', enemy.x, enemy.y,  enemy.size,  enemy.size)


class Die:
    @staticmethod
    def enter(enemy, e):
        play_mode.score.hero_score += 1
        game_world.remove_collision_object(enemy)
        enemy.frame = 0
        enemy.dir=-1

    @staticmethod
    def exit(enemy, e):
        game_world.add_collision_pairs('enemy:hero', enemy, None)
        game_world.add_collision_pairs('hero:enemy', None, enemy)
        enemy.x, enemy.y = 800, 150
        play_mode.hero.x, play_mode.hero.y = 200, 150
        enemy.lose = False

    @staticmethod
    def do(enemy):
        enemy.frame= (enemy.frame + FRAMES_PER_DIE * DIE_PER_TIME * game_framework.frame_time) % 3
        # if hero.frame>1:
        #     hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - enemy.wait_time > 2.5:
            enemy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(enemy):
        enemy.die_image.clip_composite_draw(int(enemy.frame) * 55, 0, 55, 90,0,'h', enemy.x, enemy.y,  enemy.size,  enemy.size)


class StateMachine:
    def __init__(self, enemy):
        self.enemy = enemy
        self.cur_state = Idle
        self.transitions = {
            Idle: {retreat : Retreat, time_out : Attack_ready, die:Die, defense:Defense},
            Attack_ready: {time_out : Attack,retreat: Retreat,die:Die, defense:Defense},
            Attack:{time_out:Idle,die:Die},
            Defense:{time_out:Idle,die:Die},
            Retreat:{time_out:Idle, die:Die},
            Die:{time_out:Idle}
        }

    def start(self):
        self.cur_state.enter(self.enemy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.enemy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.state_change(e, next_state)
                return True
            else:
                continue

    def state_change(self, e, next_state):
        self.cur_state.exit(self.enemy, e)
        self.cur_state = next_state
        self.cur_state.enter(self.enemy, e)

    def draw(self):
        self.cur_state.draw(self.enemy)

class Enemy4:

    def __init__(self):
        self.size=120
        self.x, self.y = 800, 150
        self.frame = 0
        self.dir = 0
        self.attack_range=-100
        self.next_behavior=0
        self.lose = False

        self.defense_range_per=0
        self.defense_per=0

        self.idle_image = load_image('./resource\\character\\enemy4\\enemy4_idle.png')
        self.attack_ready_image = load_image(
            './resource\\character\\enemy4\\enemy4_attack_ready.png')
        self.retreat_image = load_image(
            './resource\\character\\enemy4\\enemy4_retreat.png')
        self.defense_image = load_image('./resource\\character\\enemy4\\enemy4_defense.png')
        self.attack_image = load_image('./resource\\character\\enemy4\\enemy4_attack.png')
        self.die_image = load_image('./resource\\character\\enemy4\\enemy4_die.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()

    def attack_bb(self):
        return self.x-self.attack_range,self.y-20,self.x+30,self.y+0

    def get_bb(self):
        return self.x - 40, self.y - 60, self.x + 30, self.y + 50

    def handle_collision(self, group, other):
        if group == 'enemy:hero':
            pass
        if group == 'hero:enemy':
            self.lose=True
