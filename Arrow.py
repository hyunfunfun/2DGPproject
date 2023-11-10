from pico2d import load_image
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
        self.arrow_images = [self.upimage,self.downimage,self.leftimage,self.rightimage]
        self.arrow_images=random.sample(self.arrow_images,4)


    def draw(self):
        for arrow_image in self.arrow_images:
            self.arrow_images[self.index].draw(self.index * 60 + 400, 30)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        pass
