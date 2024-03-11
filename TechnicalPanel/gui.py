from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder



class Signinwindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info

        uname = user.text
        passw = pwd.text

        if uname == '' or passw == '':
            info.text = '[color=#FF0000]username/password required[/color]'
            #print('username/password required')
        else:
            if uname == 'Jack' and passw == 'HandsomeJack':
                info.text = ('[color=#00FF00]Logged in successfully!!![/color]')
            else:
                info.text = '[color=#FF0000]invalid username/password[/color]'
class SignApp(App):
    def build(self):
        Builder.load_file("./gui.kv")
        return Signinwindow()



if __name__=="__main__":
    board = SignApp()
    board.run()