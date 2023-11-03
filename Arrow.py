from pico2d import load_image


class Arrow:
    def __init__(self):
        self.upimage = load_image('C:\\qudgus\\TUK\\2Grade 2Semester\\2DGP\\2020184009\\2DGPproject\\resource\icon\\Arrow_up.png')
        self.downimage = load_image(
            'C:\\qudgus\\TUK\\2Grade 2Semester\\2DGP\\2020184009\\2DGPproject\\resource\icon\\Arrow_down.png')
        self.leftimage = load_image(
            'C:\\qudgus\\TUK\\2Grade 2Semester\\2DGP\\2020184009\\2DGPproject\\resource\icon\\Arrow_left.png')
        self.rightimage = load_image(
            'C:\\qudgus\\TUK\\2Grade 2Semester\\2DGP\\2020184009\\2DGPproject\\resource\icon\\Arrow_right.png')

    def draw(self):
        self.upimage.draw(500, 30)
        self.downimage.draw(550, 30)
        self.leftimage.draw(600, 30)
        self.rightimage.draw(650, 30)

    def update(self):
        pass
