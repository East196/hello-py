# import kivy
#
# kivy.require('1.0.6')  # replace with your current kivy version !
# from kivy.app import App
# from kivy.uix.label import Label

## pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string('''
<OneScreen>
    FloatLayout:
        Button:
            id: one_ask
            text: 'Who?'
            size_hint: (3.9/6.8, 1/12)
            pos_hint: {'center_x': 0.5, 'y': 0.37}
            on_press: root.do_something()
        Label:
            id: label
            text: 'Who made this?'
            size_hint: (3.9/6.8, 1/12)
            pos_hint: {'center_x': 0.5, 'y': 0.47}
''')


class OneScreen(Screen):
    def __init__(self, **kwargs):
        self.author = 'zd'
        super(OneScreen, self).__init__(**kwargs)

    def do_something(self):
        self.ids['label'].text = self.author


class TestApp(App):
    def build(self):
        return OneScreen()


from kivy.app import App
from kivy.uix.button import Button


class TestApp2(App):
    def build(self):
        return Button(text='Hello World')


if __name__ == '__main__':
    TestApp2().run()
