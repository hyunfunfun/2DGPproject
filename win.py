from pico2d import load_image

class Win:
    def __init__(self):
        self.win_image = load_image('./resource\\icon\\Win.png')

    def draw(self):
        self.win_image.draw(400, 300)

    def update(self):
        pass