from pico2d import load_image
import game_framework
import game_world
import random

TIME_PER_ACTION = 10
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


TIME_PER_ACTION1 = 100
ACTION_PER_TIME1 = 1.0 / TIME_PER_ACTION1
FRAMES_PER_ACTION1 = 10

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class Timer:

    def __init__(self):
        self.sec_frame = 0
        self.ten_frame= 0
        self.x=500
        self.y=550

        self.timer_image = load_image('./resource\icon\\number1.png')

    def draw(self):
        self.timer_image.clip_draw(int(self.sec_frame) * 17, 0, 18, 18, self.x, self.y)
        self.timer_image.clip_draw(int(self.ten_frame) * 17, 0, 18, 18, self.x-20, self.y)


    def handle_event(self, event):
        pass

    def update(self):
        self.ten_frame = (self.ten_frame + FRAMES_PER_ACTION1 * ACTION_PER_TIME1 * game_framework.frame_time) % 10
        self.sec_frame = (self.sec_frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        pass
