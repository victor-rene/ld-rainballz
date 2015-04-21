from random import choice, randint

from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget

elements = ('fire', 'ice', 'lightning')


class Powerup(Widget):

    element = StringProperty()

    def __init__(self, **kw):
        self.bg_img = Image(source='img/rainbox.png', allow_stretch = True)
        self.fg_img = Image(allow_stretch = True)
        super(Powerup, self).__init__(**kw)
        self.add_widget(self.bg_img)
        self.add_widget(self.fg_img)
        self.dx = 0
        self.speed = 0
        self.hitbox = 0

    def on_element(self, *args):
        self.fg_img.source = 'img/%s.png' % self.element
        print self.fg_img.source
        if self.element == 'fire':
            self.fg_img.color = [1, .2, .6, 1]
            self.bg_img.color = [.5, .1, .3, 1]
        elif self.element == 'lightning':
            self.fg_img.color = [.6, 1, .2, 1]
            self.bg_img.color = [.3, .5, .1, 1]
        elif self.element == 'ice':
            self.fg_img.color = [.2, .6, 1, 1]
            self.bg_img.color = [.1, .3, .5, 1]

    def on_size(self, *args):
        self.bg_img.size = self.size
        self.fg_img.size = self.width/2., self.height/2.
        self.fg_img.center = self.center
        self.bg_img.center = self.center
        
    def on_pos(self, *args):
        self.fg_img.center = self.center
        self.bg_img.center = self.center

    def reset(self):
        if not self.parent:
            return
        # element
        self.element = choice(elements)
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

    def move(self):
        if not self.parent:
            return
        if self.dx == 0:
            self.reset()
        self.center_x += self.dx * self.speed
        if self.center_x < -100 or self.center_x > self.parent.right + 100:
            self.reset()

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.uix.boxlayout import BoxLayout
    elements = ('fire', 'ice', 'lightning')
    powerups = [Powerup(element=elements[i]) for i in range(3)]
    bl = BoxLayout()
    for i in range(3):
        bl.add_widget(powerups[i])
    runTouchApp(bl)
