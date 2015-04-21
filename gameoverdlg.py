from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class GameOverDlg(Popup):

    def __init__(self, **kw):
        super(GameOverDlg, self).__init__(**kw)
        self.content = GridLayout(rows=4)
        self.title = 'Rainballz'
        self.content.add_widget(Label(
            text='GAME OVER',
            font_name='font/Mouser 3D.ttf',
            font_size=60))
        self.content.add_widget(Label(
            text='SCORE: ' + str(kw['score']),
            font_name='font/Mouser 3D.ttf',
            font_size=60))
        self.content.add_widget(Label(
            text='CONTINUE?',
            font_name='font/Mouser 3D.ttf',
            font_size=60))
        self.bl_btns = GridLayout(cols=2)
        self.img_yes = Image(source='img/yes_gray.png', size_hint=(.5, .5))
        self.img_no = Image(source='img/no_gray.png', size_hint=(.5, .5))
        self.bl_btns.add_widget(self.img_yes)
        self.bl_btns.add_widget(self.img_no)
        self.content.add_widget(self.bl_btns)
        self.timeout = False
        Clock.schedule_once(self.set_timeout, 2)

    def set_timeout(self, *args):
        self.timeout = True
        self.img_yes.source='img/yes.png'
        self.img_no.source='img/no.png'

    def on_touch_down(self, touch):
        if self.timeout:
            app = App.get_running_app()
            if self.img_no.collide_point(*touch.pos):
                app.stop()
            elif self.img_yes.collide_point(*touch.pos):
                wnd = app.root_window
                for child in wnd.children:
                    wnd.remove_widget(child)
                    del child
                from rootwidget import RootWidget
                wnd.add_widget(RootWidget())
