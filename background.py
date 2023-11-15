from pico2d import load_image


class Background:
    def __init__(self):
        self.stage1=load_image('./resource\\Background\\stage1.png')
        self.stage2=load_image('./resource\\Background\\stage2.png')
        self.stage3 = load_image('./resource\\Background\\stage3.png')
        self.stage4 = load_image('./resource\\Background\\stage4.png')
        self.stage5 = load_image('./resource\\Background\\stage5.png')
        self.stage_Boss=load_image('./resource\\Background\\stage2.png')

    def draw(self):
        self.stage1.draw(450, 250)

    def update(self):
        pass
