from pico2d import load_image

class Lose:
    def __init__(self):
        self.lose_image = load_image('./resource\\icon\\Lose.png')

    def draw(self):
        self.lose_image.draw(400, 300)

    def update(self):
        pass