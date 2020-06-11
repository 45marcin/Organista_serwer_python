from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from kivy.clock import Clock
from kivy.config import Config
import getpass


if not "marcin" in getpass.getuser():
    Config.set('kivy', 'exit_on_escape', '0')
    Config.set('graphics', 'window_state', 'maximized')
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set("graphics", "show_cursor", 0)
else:
    Config.set('kivy', 'exit_on_escape', '1')
    Config.set('graphics', 'window_state', 'maximized')
    Config.set('graphics', 'fullscreen', 0)
    Config.set("graphics", "show_cursor", 0)

import subprocess
import sys

import datetime

p = subprocess.Popen([sys.executable, '/home/organista/Organista_python/main.py'])

class MyLabel(Image):
    text = StringProperty('')

    def on_text(self, *_):
        # Just get large texture:
        l = Label(text=self.text)
        if "Organista" in self.text:
            l = Label(text=str(datetime.date.today()))
        l.font_size = '600dp'  # something that'll give texture bigger than phone's screen size
        l.texture_update()
        # Set it to image, it'll be scaled to image size automatically:
        self.texture = l.texture

def WriteToFile(text):
    file = open('/home/organista/tekst', 'w')
    file.write(text)
    file.close()


class RootWidget(BoxLayout):
    pass



class Display(MyLabel):
    def update(self, *args):
        try:
            tmp = open("/home/organista/tekst", "r")
            self.text = tmp.read()
        except: None


class TestApp(App):
    def build(self):
        display = Display()
        App.title = "organista"
        Clock.schedule_interval(display.update, 0.5)
        return display

if __name__ == '__main__':
    TestApp().run()