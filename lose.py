from pico2d import load_image

class Lose:
    def __init__(self):
        self.lose_image = load_image('./resource\\icon\\Lose.png')

    def draw(self):
        self.lose_image.clip_draw(0, 0, 300, 90, 450, 300,200,150)

    def update(self):
        pass