from pico2d import load_image
import play_mode
import game_framework
import game_world
import random

class Score:

    def __init__(self):
        self.hero_x=250
        self.hero_y=450

        self.enemy_x = 750
        self.enemy_y = 450

        self.hero_frame=0
        self.enemy_frame = 0
        self.hero_score=0
        self.enemy_score = 0

        self.score_image = load_image('./resource\icon\\number1.png')

    def draw(self):
        self.score_image.clip_draw(int(self.hero_frame) * 17, 0, 18, 18, self.hero_x, self.hero_y,40,40)
        self.score_image.clip_draw(int(self.enemy_frame) * 17, 0, 18, 18, self.enemy_x, self.enemy_y, 40, 40)

    def handle_event(self, event):
        pass

    def update(self):
        self.hero_frame =(self.hero_score)%10
        self.enemy_frame =(self.enemy_score)%10
        pass
