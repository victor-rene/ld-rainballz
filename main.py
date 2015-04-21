# import os
# os.environ["KIVY_AUDIO"] = "sdl2"

from kivy.app import App
from kivy.config import Config

Config.set('input', 'wm_touch', '')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'borderless', True)
Config.set('graphics', 'fullscreen', False)
Config.set('graphics', 'height', '1080')
Config.set('graphics', 'width', '1920')

from rootwidget import RootWidget


class RainballApp(App):

    def build(self):
        return RootWidget()

        
if __name__ == '__main__':
    RainballApp().run()
