from pico2d import load_image
import game_world
import random

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
        self.arrow_dir=[n for n in range(4)]
        # random.shuffle(self.arrow_dir)


    def remove_arrow(self):
        game_world.remove_object(self)


    def draw(self):
        if self.arrow_dir[self.index]==0:
            self.upimage.draw(self.index * 60 + 400, 30)
        elif self.arrow_dir[self.index]==1:
            self.downimage.draw(self.index * 60 + 400, 30)
        elif self.arrow_dir[self.index] == 2:
            self.leftimage.draw(self.index * 60 + 400, 30)
        elif self.arrow_dir[self.index] == 3:
            self.rightimage.draw(self.index * 60 + 400, 30)

    def handle_event(self, event):
        pass

    def update(self):
        pass
