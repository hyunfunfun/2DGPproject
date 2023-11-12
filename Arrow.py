from pico2d import load_image
import game_world
import random

class Arrow:

    def __init__(self,index,arrow_dir):
        self.index=index
        self.arrow_dir=arrow_dir
        self.upimage = load_image('./resource\icon\\Arrow_up.png')
        self.downimage = load_image(
            './resource\icon\\Arrow_down.png')
        self.leftimage = load_image(
            './resource\icon\\Arrow_left.png')
        self.rightimage = load_image(
            './resource\icon\\Arrow_right.png')

    def remove_arrow(self):
        game_world.remove_object(self)


    def draw(self):
        if self.arrow_dir==0:
            self.upimage.draw(self.index * 60 + 400, 30)
        elif self.arrow_dir==1:
            self.downimage.draw(self.index * 60 + 400, 30)
        elif self.arrow_dir == 2:
            self.leftimage.draw(self.index * 60 + 400, 30)
        elif self.arrow_dir == 3:
            self.rightimage.draw(self.index * 60 + 400, 30)

    def handle_event(self, event):
        pass

    def update(self):
        pass
