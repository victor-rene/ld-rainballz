from kivy.animation import Animation
from kivy.uix.label import Label


class PopLabel(Label):

    def on_text(self, *args):
        anim = Animation(font_size=30, t='out_elastic') \
            + Animation(font_size=15, t='in_elastic')
        anim.start(self)
