from kivy.factory import Factory
from kivy.core.window import Window
from kaki.app import App
from kivymd.app import MDApp

Window.size = (350, 700)


class HotReload(App, MDApp):
    CLASSES = {
        'Box': 'logic'
    }

    AUTORELOADER_PATHS = [
        ('.', {'recursive': True})
    ]

    KV_FILES = [
        'logic.kv'
    ]

    def build_app(self, first=False):
        return Factory.Box()

if __name__ == '__main__':
    HotReload().run()
