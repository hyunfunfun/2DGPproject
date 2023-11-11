from pico2d import load_image
import game_world
import random

from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_SPACE

class Arrow:
    def __init__(self,index):
        self.index=index
        self.upimage = load_image('./resource\icon\\Arrow_up.png')
        self.downimage = load_image(
            './resource\icon\\Arrow_down.png')
        self.leftimage = load_image(
            './resource\icon\\Arrow_left.png')
        self.rightimage = load_image(
            './resource\icon\\Arrow_right.png')
        self.arrow_list=[self.upimage,self.downimage,self.leftimage,self.rightimage]
        random.shuffle(self.arrow_list)

    def remove_arrow(self):
        game_world.remove_object(self)

    def draw(self):
        if self.index==0:
            self.arrow_list[0].draw(self.index * 60 + 400, 30)
        elif self.index == 1:
            self.arrow_list[0].draw(self.index * 60 + 400, 30)
        elif self.index == 2:
            self.arrow_list[0].draw(self.index * 60 + 400, 30)
        elif self.index == 3:
            self.arrow_list[0].draw(self.index * 60 + 400, 30)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        pass
