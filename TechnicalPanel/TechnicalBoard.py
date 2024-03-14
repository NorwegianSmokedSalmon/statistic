from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=4)
        for i in range(12):
            btn = Button(text='Robot{}'.format(i), on_release=self.change_screen)
            source = 'image/b{}.png'.format(i)
            img = Image(source=source)
            layout.add_widget(img)
            layout.add_widget(btn)
        self.add_widget(layout)

    def change_screen(self, instance):
        self.manager.current = instance.text.split('Board')[-1]

class ColorScreen(Screen):
    def __init__(self, color, data, index, **kwargs):
        super(ColorScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='horizontal')
        data_layout = GridLayout(cols=2, size_hint_x=None, width=300)
        labels = ['a', 'b', 'c', 'd', 'e', 'f']
        for i, label in enumerate(labels):
            lbl = Label(text=label, size_hint_y=None, height=100)
            txt_input = TextInput(text=str(data[i]), size_hint_y=None, height=100, halign='left')
            txt_input.bind(minimum_height=txt_input.setter('height'))
            data_layout.add_widget(lbl)
            data_layout.add_widget(txt_input)
        layout.add_widget(data_layout)

        img = Image(source='image/b3.png')
        lbl = Label(text=str(index), size_hint=(None, None), pos=img.pos, color=(0, 0, 0, 1))
        img.add_widget(lbl)
        layout.add_widget(img)

        anchor_layout = AnchorLayout(anchor_x='left', anchor_y='bottom')
        box_layout = BoxLayout(size_hint=(None, None), size=(100, 50))
        btn = Button(text='ESC', on_release=self.go_back)
        box_layout.add_widget(btn)
        anchor_layout.add_widget(box_layout)
        layout.add_widget(anchor_layout)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_back(self, instance):
        self.manager.current = 'main_screen'

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        colors = [(0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1),
                  (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1),
                  (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1),]
        data = [[i for i in range(6)] for _ in range(12)]
        test = ['jack', 'mark', 'david', 'neymar', 'messi', 'ronaldo']
        for i in range(12):
            sm.add_widget(ColorScreen(name='Robot{}'.format(i), color=colors[i], data=test, index=i))
            #sm.add_widget(ColorScreen(name='Robot{}'.format(i), color=colors[i], data=test))
        return sm

if __name__ == '__main__':
    TestApp().run()