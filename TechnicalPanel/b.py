from kivy.graphics import Ellipse, Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label

class CircularButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text=self.text)

    def draw(self):
        with self.canvas:
            Color(0, 1, 0, 1) # set the color of the button
            d = min(self.size) # diameter of the button
            Ellipse(pos=self.pos, size=(d, d)) # draw the button
            self.label.texture_update()
            w, h = self.label.texture_size
            x = self.center_x - w / 2
            y = self.center_y - h / 2
            Color(1, 1, 1, 1) # set the color of the label
            Rectangle(texture=self.label.texture, pos=(x, y), size=self.label.texture_size) # draw the label


if __name__ == "__main__":
    a = CircularButton()
    a.
