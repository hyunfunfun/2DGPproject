from pico2d import load_image, draw_rectangle, load_music
import play_mode
import winlose_mode

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

        self.stage1_bgm=load_music('./resource\\music\\stage1.mp3')
        self.stage2_bgm = load_music('./resource\\music\\stage2.mp3')
        self.stage3_bgm = load_music('./resource\\music\\stage3.mp3')
        self.stage4_bgm = load_music('./resource\\music\\stage4.mp3')
        self.boss_bgm = load_music('./resource\\music\\boss.mp3')
        if play_mode.hero.win_count==0:
            self.stage1_bgm.set_volume(60)
            self.stage1_bgm.repeat_play()
        elif play_mode.hero.win_count==1:
            self.stage2_bgm.set_volume(60)
            self.stage2_bgm.repeat_play()
        elif play_mode.hero.win_count==2:
            self.stage3_bgm.set_volume(60)
            self.stage3_bgm.repeat_play()
        elif play_mode.hero.win_count==3:
            self.stage4_bgm.set_volume(60)
            self.stage4_bgm.repeat_play()
        elif play_mode.hero.win_count==4:
            self.boss_bgm.set_volume(60)
            self.boss_bgm.repeat_play()
        else:
            self.select.set_volume(60)
            self.select.repeat_play()


        self.stage_dic={0:self.stage1, 1:self.stage2, 2:self.stage3, 3:self.stage4, 4:self.stage_Boss }

    def draw(self):
        self.stage_dic[self.index].draw(500, 250)

    def update(self):
        pass
