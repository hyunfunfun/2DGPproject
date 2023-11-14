from pico2d import load_image


class Background:
    def __init__(self,index):
        self.index=index
        self.stage1_1_image = load_image('./resource\\Background\\stage1-1.png')
        self.stage1_2_image = load_image('./resource\\Background\\stage1-2.png')

    def draw(self):
        if self.index==1:
            self.stage1_1_image.draw(500, 350)
        elif self.index==0:
            self.stage1_2_image.draw(500, 350)

    def update(self):
        pass
