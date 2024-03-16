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
def getDatas():
    #读取总数据
    with open('data.txt', 'r') as file:
        lines = file.readlines()
        data_lists = []
        # 遍历文件中的每一行
        for line in lines:
            # 使用eval函数将字符串转换为列表
            data_list = eval(line.strip())
            # 将列表添加到大列表中
            data_lists.append(data_list)
        return data_lists

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=4)
        for i in range(14):
            if i == 12:
                btn = Button(text='ourTotal', on_release=self.change_screen)
                source = 'image/z.png'
                img = Image(source=source)
                layout.add_widget(img)
                layout.add_widget(btn)
                continue
            elif i == 13:
                btn = Button(text='theirTotal', on_release=self.change_screen)
                source = 'image/z.png'
                img = Image(source=source)
                layout.add_widget(img)
                layout.add_widget(btn)
                break
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
        labels = ['Times of passing', 'Times of losing possession', 'Rate of successfully passing', 'Rate of losing possession', 'Is MVP']
        if index == 12 or index == 13:
            labels.clear()
            labels = ['Rate of  holding', 'Times of passing', 'Times of losing possession', 'Times of shooting', 'Rate of successfully passing']
        super(ColorScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='horizontal')
        data_layout = GridLayout(cols=2, size_hint_x=None, width=300)
        for i, label in enumerate(labels):
            lbl = Label(text=label, size_hint_y=None, height=100, halign='left')
            data_layout.add_widget(lbl)
            txt_input = TextInput(text=str(data[i]), size_hint_y=None, height=100, halign='left')
            txt_input.bind(minimum_height=txt_input.setter('height'))
            data_layout.add_widget(txt_input)
        layout.add_widget(data_layout)
        img = Image(source='image/Max.png')
        layout.add_widget(img)
        anchor_layout = AnchorLayout(anchor_x='right', anchor_y='bottom')
        lbl = Label(text="Robot Number:  " + str(index),  size_hint=(0.2, 0.2),  color=(0, 0, 0, 1))
        anchor_layout.add_widget(lbl)
        layout.add_widget(anchor_layout)
        box_layout = BoxLayout(size_hint=(None, None), size=(100, 50))
        btn = Button(text='ESC', on_release=self.go_back)
        box_layout.add_widget(btn)
        anchor_layout.add_widget(box_layout)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_back(self, instance):
        self.manager.current = 'main_screen'

class TestApp(App):
    def build(self):
        data = getDatas()
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        colors = [(0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1),
                  (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1),
                  (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1),
                  (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1)]
        for i in range(14):
            if i == 12:
                sm.add_widget(ColorScreen(name='ourTotal', color=colors[i], data=data[0], index=i))
                continue
            elif i == 13:
                sm.add_widget(ColorScreen(name='theirTotal', color=colors[i], data=data[1], index=i))
                break
            sm.add_widget(ColorScreen(name='Robot{}'.format(i), color=colors[i], data=data[i+2], index=i))
        return sm

if __name__ == '__main__':
    TestApp().run()


