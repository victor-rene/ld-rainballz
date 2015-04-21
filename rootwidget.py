import math

from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_sdl2 import SoundSDL2
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from background import Background
from rainball import Rainball
from rainbox import Rainbox
from powerup import Powerup
from poplabel import PopLabel
from gameoverdlg import GameOverDlg

def distance(wgt1, wgt2):
    dx = wgt1.center_y - wgt2.center_y
    dy = wgt1.center_x - wgt2.center_x
    return math.sqrt(dx ** 2 + dy ** 2)

sounds = {
    'levelup': SoundSDL2(source='sfx/levelup.wav'),
    'powerup': SoundSDL2(source='sfx/levelup.wav'),
    'hit': SoundSDL2(source='sfx/hit.wav'),
    'hurt': SoundSDL2(source='sfx/hurt.wav'),
    'gameover': SoundSDL2(source='sfx/gameover.wav'),
    'music': SoundLoader.load('sfx/acidamine.ogg'),
}


class RootWidget(Widget):

    def __init__(self, **kw):
        super(RootWidget, self).__init__(**kw)
        self.level = 1
        self.seconds = 0
        self.combo = 1
        self.score = 0
        self.hits = 0
        self.cons = 0
        self.rainboxes = [Rainbox(pos=(-500, 0)) for i in range(10)]
        self.powerup = Powerup()
        self.miniball = Rainball(size=(60, 60), name='mini')
        self.miniball.speed = 20
        self.maxiball = Rainball(size=(120, 120), name='maxi', element='stone')
        self.background = Background(size=Window.size)
        self.target_l = Image(source='img/target_l.zip', size=(60, 60))
        self.lbl_fps = Label(pos=(Window.width -100, 0))
        self.lbl_level = PopLabel(
            pos=(100, Window.height-100),
            font_name='font/Mouser.ttf')
        self.lbl_hits = PopLabel(
            pos=(100, Window.height-140),
            font_name='font/Mouser.ttf')
        self.lbl_combo = PopLabel(
            pos=(100, Window.height-180),
            font_name='font/Mouser.ttf')
        self.lbl_score = PopLabel(
            pos=(100, Window.height-220),
            font_name='font/Mouser.ttf')
        self.add_widget(self.background, canvas='before')
        self.add_widget(self.target_l)
        self.add_widget(self.miniball)
        self.add_widget(self.maxiball)
        self.add_widget(self.lbl_fps)
        self.add_widget(self.lbl_level)
        self.add_widget(self.lbl_hits)
        self.add_widget(self.lbl_combo)
        self.add_widget(self.lbl_score)
        self.add_widget(self.powerup)
        for i in range(10):
            self.add_widget(self.rainboxes[i])
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_key_down)
        sounds['music'].loop = True
        sounds['music'].play()
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, dt):
        self.background.move()
        miniball = self.miniball
        self.miniball.move()
        maxiball = self.maxiball
        maxiball.move()
        # powerup collision
        powerup = self.powerup
        powerup.move()
        d_maxi =  distance(powerup, maxiball)
        if d_maxi < powerup.hitbox + maxiball.hitbox:
            self.combo += 1
            sounds['powerup'].play()
            maxiball.color = powerup.fg_img.color
            maxiball.element = powerup.element
            if powerup.element == 'ice':
                for i in range(self.level):
                    self.rainboxes[i].frozen = 180
            print miniball.hitbox
            miniball.deployed = powerup.element == 'fire'
            print miniball.hitbox
            powerup.reset()
        # mistake mini
        d_mini =  distance(powerup, miniball)
        if d_mini < powerup.hitbox + miniball.hitbox:
            self.combo = 1
            sounds['hurt'].play()
            powerup.reset()
            if maxiball.element == 'stone':
                self.end_game()
            else: maxiball.element = 'stone'
            miniball.deployed = False
        # box collision
        for i in range(self.level):
            rainbox = self.rainboxes[i]
            rainbox.move()
            d_mini =  distance(rainbox, miniball)
            if d_mini < rainbox.hitbox + miniball.hitbox:
                print rainbox.hitbox, miniball.hitbox
                self.hits += 1
                self.cons += 1
                if self.cons == 10:
                    self.level += 1
                    sounds['levelup'].play()
                self.score += self.hits * self.combo
                sounds['hit'].play()
                rainbox.reset()
            # mistake maxi
            d_maxi =  distance(rainbox, maxiball)
            if d_maxi < rainbox.hitbox + maxiball.hitbox:
                self.cons = 0
                sounds['hurt'].play()
                rainbox.reset()
                if maxiball.element == 'stone':
                    self.end_game()
                else: maxiball.element = 'stone'
                miniball.deployed = False
        # labels update
        self.lbl_fps.text = 'FPS: %d' % Clock.get_fps()
        self.lbl_hits.text = 'HITS: x%d (%d)' % (self.cons, self.hits)
        self.lbl_combo.text = 'COMBO: x%d' % self.combo
        self.lbl_score.text = 'SCORE: %d' % self.score
        self.lbl_level.text = 'LEVEL: %d (%d)' % (self.level, self.seconds)

    def on_touch_down(self, touch):
        if 'button' in touch.profile:
            if touch.button == 'left':
                self.miniball.target = touch.pos
                self.target_l.center = touch.pos
            elif touch.button == 'right':
                self.maxiball.target = touch.pos

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'escape':
            self.end_game()
        return True

    def end_game(self):
        sounds['gameover'].play()
        sounds['music'].stop()
        Clock.unschedule(self.update)
        godlg = GameOverDlg(score=self.score).open()

    def new_game(self):
        wnd = self.parent
        wnd.remove_widget(self)
        wnd.add_widget(RootWidget())
