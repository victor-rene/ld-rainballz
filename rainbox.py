from random import randint

from kivy.uix.image import Image
from kivy.properties import NumericProperty


class Rainbox(Image):

    frozen = NumericProperty()

    def __init__(self, **kw):
        super(Rainbox, self).__init__(**kw)
        self.source = 'img/rainbox.png'
        self.allow_stretch = True
        self.dx = 0
        self.speed = 0
        self.hitbox = 0

    def reset(self):
        if not self.parent:
            return
        # x
        if self.center_x < self.parent.center_x:
            self.x = self.parent.right
            self.dx = -1
        else:
            self.right = self.parent.x
            self.dx = 1
        # y
        dy = randint(-4, 4) / 10.
        self.center_y = self.parent.center_y + self.parent.height * dy
        # size
        scale = randint(1, 3)
        self.size = (60 * scale, 60 * scale)
        self.hitbox = 60 * scale * .66
        self.speed = (4 - scale) * 3
        self.frozen = 0

    def on_frozen(self, *args):
        if self.frozen:
            self.color = [0, 1, 1, 1]
        else:
            self.color = [1,1,1,1]

    def move(self):
        if not self.parent:
            return
        if self.frozen:
            self.frozen -= 1
        else:
            if self.dx == 0:
                self.reset()
            self.center_x += self.dx * self.speed
            if self.center_x < -100 or self.center_x > self.parent.right + 100:
                self.reset()
