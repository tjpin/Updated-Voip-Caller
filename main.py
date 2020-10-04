from kivymd.app import MDApp
from home import HomeScreen


class MainApp(MDApp):
    def build(self):
        return HomeScreen()


MainApp().run()
