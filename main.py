"""An App that helps you decide what dish to have for your meal"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


class HomePage(Screen):
    pass


class MealTypeSelectionPage(Screen):
    pass


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        if key == 27:  # the esc key
            if self.current_screen.name == "HomePage":
                return False  # exit the app from this page
            elif self.current_screen.name == "MealTypeSelectionPage":
                self.current = "HomePage"
                return True  # do not exit the app


kv = Builder.load_file("mealsuggestion.kv")


class MealSuggestionApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MealSuggestionApp().run()
