from pico2d import load_image

class Win:
    def __init__(self):
        self.win_image = load_image('./resource\\icon\\Win.png')

    def draw(self):
        self.win_image.clip_draw(0, 0, 300, 90, 450, 300, 200, 150)

    def update(self):
        pass