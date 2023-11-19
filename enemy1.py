import random
import math
import game_framework
import game_world
import play_mode
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

from pico2d import *



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
        if enemy.attack_count>0:
            for n in range(enemy.attack_count, 4):
                enemy.remove_arrow(n)
            enemy.create_arrow()
        enemy.attack_count=0
        enemy.dir = 0
        enemy.frame = 0
        pass

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(enemy):
        enemy.idle_image.clip_draw(int(enemy.frame) * 120, 0, 60, 80, enemy.x, enemy.y, 100, 100)

class Attack_ready:
    @staticmethod
    def enter(enemy, e):
        enemy.remove_arrow(enemy.attack_count)
        enemy.wait_time = get_time()
        enemy.frame = (enemy.frame + 1) % 3
        enemy.attack_count += 1
        enemy.dir=1

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(hero):
        if hero.attack_count >= 4:
            hero.attack_count = 0
            hero.state_machine.handle_event(('Attack', 0))
        if get_time() - hero.wait_time > 1:
            hero.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(enemy):
        enemy.attack_ready_image.clip_draw(int(enemy.frame) * 120, 0, 60, 90, enemy.x, enemy.y, 100, 100)

class Attack:
    @staticmethod
    def enter(enemy, e):
        enemy.attack_count = 0
        enemy.frame = 0
        # hero.wait_time = get_time()
        enemy.dir=1

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame= (enemy.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 2
        if enemy.frame>1:
            enemy.x += enemy.dir * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - enemy.wait_time > 1:
            enemy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(enemy):
        enemy.attack_image.clip_draw(int(enemy.frame) * 120, 0, 100, 90, enemy.x, enemy.y, 130, 100)

class Retreat:

    @staticmethod
    def enter(enemy, e):
        if enemy.attack_count>0:
            for n in range(enemy.attack_count, 4):
                enemy.remove_arrow(n)
            enemy.create_arrow()
        enemy.attack_count=0
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
        enemy.x += enemy.dir * RUN_SPEED_PPS * game_framework.frame_time
        enemy.x = clamp(25, enemy.x, 1600 - 25)
        if enemy.x <= 100:
            enemy.attack_count = 0
            enemy.state_machine.handle_event(('Die', 0))
        elif get_time() - enemy.wait_time > 0.5:
            enemy.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(enemy):
        enemy.retreat_image.clip_draw(int(enemy.frame) * 65, 0, 50, 90, enemy.x, enemy.y, 100, 100)

class Die:
    @staticmethod
    def enter(enemy, e):
        enemy.frame = 0
        enemy.dir=-1

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(hero):
        hero.frame=(hero.frame + FRAMES_PER_DIE * DIE_PER_TIME * game_framework.frame_time) % 3
        # if hero.frame>1:
        #     hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - hero.wait_time > 2:
            hero.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(enemy):
        enemy.die_image.clip_draw(int(enemy.frame) * 65, 0, 65, 90, enemy.x, enemy.y, 100, 100)


class Enemy1:
    global idle_state
    global attack_state
    global retreat_state
    global die_state

    idle_state=1
    attack_state=2
    retreat_state=3
    die_state=4

    def __init__(self):
        self.x, self.y = 700, 150
        self.frame = 0
        self.dir = 0
        self.attack_count = 0

        self.state=1
        self.build_behavior_tree()

        self.idle_image = load_image('./resource\\character\\enemy1\\enemy1_idle.png')
        self.attack_ready_image = load_image(
            './resource\\character\\enemy1\\enemy1_attack_ready.png')
        self.retreat_image = load_image(
            './resource\\character\\enemy1\\enemy1_retreat.png')
        self.attack_image = load_image('./resource\\character\\enemy1\\enemy1_attack.png')
        self.die_image = load_image('./resource\\character\\enemy1\\enemy1_die.png')

    def update(self):
        if self.state==idle_state:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        elif self.state==attack_state:
            self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % 2
            if self.frame > 1:
                self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time
        elif self.state==retreat_state:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            self.x -= self.dir * RUN_SPEED_PPS * game_framework.frame_time
        elif self.state==die_state:
            self.frame = (self.frame + FRAMES_PER_DIE * DIE_PER_TIME * game_framework.frame_time) % 3
        self.bt.run()


    def handle_event(self, event):
        pass

    def draw(self):
        if self.state==idle_state:
            self.idle_image.clip_composite_draw(int(self.frame) * 120, 0, 60, 80,0,'h', self.x, self.y, 100, 100)
        elif self.state==attack_state:
            self.attack_image.clip_composite_draw(int(self.frame) * 120, 0, 100, 90,0,'h', self.x, self.y, 130, 100)
        elif self.state==retreat_state:
            self.retreat_image.clip_composite_draw(int(self.frame) * 65, 0, 50, 90,0,'h', self.x, self.y, 100, 100)
        elif self.state==die_state:
            self.die_image.clip_composite_draw(int(self.frame) * 65, 0, 65, 90,0,'h', self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())  # 튜플을 풀어서 인자로 전달

    def get_bb(self):
        return self.x - 50, self.y - 60, self.x + 50, self.y + 50

    def handle_collision(self, group, other):
        pass


    def idle(self):
        self.state=idle_state
        pass

    def attack(self):
        self.state=attack_state
        pass

    def retreat(self):
        self.retreat=retreat_state
        pass

    def die(self):
        self.die=die_state
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def is_boy_nearby(self, r):
        if self.distance_less_than(play_mode.hero.x, play_mode.hero.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def isnt_boy_nearby(self, r):
        if self.distance_less_than(play_mode.hero.x, play_mode.hero.y, self.x, self.y, r):
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):

        a1=Action('공격',self.attack)

        a2=Action('회피',self.retreat)

        c1 = Condition('hero가 근처에 있는가?',self.is_boy_nearby,10)

        c2=Condition('hero가 근처에 없는가?',self.isnt_boy_nearby,10)

        SEQ_retreat = Sequence('가까우면 회피',c1,a2)

        SEQ_attack=Sequence('멀면 공격',c2,a1)

        root = SEL_attack_or_retreat = Selector('공격 또는 회피',SEQ_attack,SEQ_retreat)

        self.bt = BehaviorTree(root)