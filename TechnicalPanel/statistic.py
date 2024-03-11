from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
class OperatorWindow(BoxLayout):
    def __init__(self, **kwsrgs):
        super().__init__(**kwsrgs)

class OperatorApp(App):
    def build(self):
        Builder.load_file("./statistic.kv")
        return OperatorWindow()

if __name__ == "__main__":
    oa = OperatorApp()
    oa.run()