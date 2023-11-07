from pico2d import load_image
import random

from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_SPACE


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


class Arrow:
    def __init__(self,index):
        self.index=index
        self.upimage = load_image('C:\\qudgus\\TUK\\2Grade 2Semester\\2DGP\\2020184009\\2DGPproject\\resource\icon\\Arrow_up.png')
        self.downimage = load_image(
            'C:\\qudgus\\TUK\\2Grade 2Semester\\2DGP\\2020184009\\2DGPproject\\resource\icon\\Arrow_down.png')
        self.leftimage = load_image(
            'C:\\qudgus\\TUK\\2Grade 2Semester\\2DGP\\2020184009\\2DGPproject\\resource\icon\\Arrow_left.png')
        self.rightimage = load_image(
            'C:\\qudgus\\TUK\\2Grade 2Semester\\2DGP\\2020184009\\2DGPproject\\resource\icon\\Arrow_right.png')
        self.list=[self.upimage,self.downimage,self.rightimage, self.leftimage]

    def draw(self):
        self.list[self.index].draw(self.index*60+400,30)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        pass
