import kivy
from kivy import platform
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import WindowBase, Window

class MainUI(FloatLayout):
    #window = WindowBase()
    pass
   
class GuessTheHeroApp(App):

    def build(self):
        self.icon='data/images/dota_icon.png'
        Window.bind(on_size=self.do_rotate)
        return MainUI()

    def do_rotate(self):
        print('SIZE SIZE SIZE SIZE ========== ', Window.size)


if __name__=='__main__':
    GuessTheHeroApp().run()
