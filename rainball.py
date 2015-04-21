import math

from kivy.uix.image import Image
from kivy.properties import BooleanProperty, StringProperty

from bullets import Bullets

dark_colors = {
    'stone': [.1,.1,.1,1],
    'lightning': [.1,.2,0,1],
    'fire': [.2,0,.1,1],
    'ice': [0,.1,.2,1],
}

light_colors = {
    'fire': [1, .2, .6, 1],
    'lightning': [.6, 1, .2, 1],
    'ice': [.2, .6, 1, 1],
    'stone': [.7,.7,.7,1],
}

class Rainball(Image):

    element = StringProperty()
    name = StringProperty()
    deployed = BooleanProperty(False)

    def __init__(self, **kw):
        self.source='img/rainball.png'
        self.speed = 10
        self.angle = 0
        self.rotation = 1
        self.target = None
        self.hitbox = self.size[0] * .5
        self.img_element = Image(
            source='img/blank.png',
            size=(self.width/2.,self.height/2.))
        self.bullets = Bullets(size=self.size)
        super(Rainball, self).__init__(**kw)
        self.add_widget(self.img_element)

    def on_size(self, *args):
        self.bullets.size = self.width * 2, self.height * 2

    def on_element(self, *args):
        self.img_element.source = 'img/%s.png' % self.element
        self.img_element.source = 'img/%s.png' % self.element
        if self.name == 'maxi':
            self.img_element.color = dark_colors[self.element]
            self.color = light_colors[self.element]
        else:
            self.img_element.color = light_colors[self.element]
            self.color = dark_colors[self.element]

    def on_deployed(self, *args):
        if self.deployed:
            self.hitbox = self.bullets.width / 2.
            if not self.bullets in self.children:
                self.add_widget(self.bullets)
        else:
            self.hitbox = self.width / 2.
            if self.bullets in self.children:
                self.remove_widget(self.bullets)

    def move(self):
        if self.target:
            if self.element != 'lightning':
                dx = self.center_x - self.target[0]
                dy = self.center_y - self.target[1]
                da = math.atan2(dy, dx)
                self.x += math.cos(da) * - self.speed
                self.y += math.sin(da) * - self.speed
                if math.sqrt(dx**2 + dy**2) < 10:
                    self.center = self.target
                    self.target = None
            else:
                self.center = self.target
                self.target = None
            self.img_element.center = self.center
        self.bullets.center = self.center
        self.bullets.move()
