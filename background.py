from pico2d import load_image, draw_rectangle


class Background:
    def __init__(self,index):
        self.leftline_x,self.leftline_y=100,50
        self.rightline_x,self.rightline_y=800,50
        self.index=index
        self.stage1=load_image('./resource\\Background\\stage1.png')
        self.stage2=load_image('./resource\\Background\\stage2.png')
        self.stage3 = load_image('./resource\\Background\\stage3.png')
        self.stage4 = load_image('./resource\\Background\\stage4.png')
        self.stage_Boss=load_image('./resource\\Background\\Boss_stage.png')
        self.stage_dic={0:self.stage1, 1:self.stage2, 2:self.stage3, 3:self.stage4, 4:self.stage_Boss}

    def draw(self):
        self.stage_dic[self.index].draw(450, 250)

    def update(self):
        pass
