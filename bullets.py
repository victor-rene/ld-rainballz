import math

from kivy.uix.image import Image
from kivy.uix.widget import Widget


class Bullets(Widget):

    def __init__(self, **kw):
        super(Bullets, self).__init__(**kw)
        self.bullets = [Image(source='img/bullet.png') for i in range(3)]
        for i in range(3):
            b = self.bullets[i]
            b.size = b.texture_size
            self.add_widget(b)
        self.angle = 0
        self.radius = 0

    def on_size(self, *args):
        self.radius = min(self.width / 2., self.height / 2.)

    def move(self, *args):
        self.angle += 6
        r = self.radius
        for i in range(3):
            a = (self.angle + i * 120) / 180. * math.pi
            b = self.bullets[i]
            b.center = (
                self.center_x + math.cos(a) * r,
                self.center_y + math.sin(a) * r)

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.clock import Clock

    b = Bullets(size=(120, 120))
    Clock.schedule_interval(b.move, 1/60.)
    runTouchApp(b)
