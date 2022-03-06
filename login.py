import pyrebase
import requests
from kivy.properties import BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from functools import partial
from kivy.metrics import dp
from kivymd.toast import toast

Window.size = (350, 650)
Window.softinput_mode = "below_target"

CREDS = JsonStore("credentials.json")

firebaseConfig = {
    "apiKey": "AIzaSyATyeXyr8XriThiyE99EvO3PIJfKzzLtlU",
    "authDomain": "su-gest.firebaseapp.com",
    "databaseURL": "https://su-gest-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "su-gest",
    "storageBucket": "su-gest.appspot.com",
    "messagingSenderId": "16999534448",
    "appId": "1:16999534448:web:8e09f666779bbca37dc9b5",
    "measurementId": "G-476SNKR2MZ"
}

FIREBASE = pyrebase.initialize_app(firebaseConfig)
AUTH = FIREBASE.auth()
DB = FIREBASE.database()


class MyMDTextField(MDTextField):
    password_mode = BooleanProperty(True)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.icon_right:
                # icon position based on the KV code for MDTextField
                icon_x = (self.width + self.x) - (self._lbl_icon_right.texture_size[1]) - dp(8)
                icon_y = self.center[1] - self._lbl_icon_right.texture_size[1] / 2
                if self.mode == "rectangle":
                    icon_y -= dp(4)
                elif self.mode != 'fill':
                    icon_y += dp(8)

                # not a complete bounding box test, but should be sufficient
                if touch.pos[0] > icon_x and touch.pos[1] > icon_y:
                    if self.password_mode:
                        self.icon_right = 'eye'
                        self.password_mode = False
                        self.password = self.password_mode
                    else:
                        self.icon_right = 'eye-off'
                        self.password_mode = True
                        self.password = self.password_mode

                    # try to adjust cursor position
                    cursor = self.cursor
                    self.cursor = (0,0)
                    Clock.schedule_once(partial(self.set_cursor, cursor))
        return super(MyMDTextField, self).on_touch_down(touch)

    def set_cursor(self, pos, dt):
        self.cursor = pos


class HomePage(MDScreen):
    pass

class LoginPage(MDScreen):

    def log_in(self):
        global AUTH, USERNAME
        if self.ids.username.text == "":
            toast("Please Enter Username")
            return
        if self.ids.password.text == "":
            toast("Please Enter Password")
            return

        username = self.ids.username.text
        password = self.ids.password.text
        try:
            AUTH.sign_in_with_email_and_password(username+"@su-gest.user", password)
            CREDS.put("User", username=username, password=password)
            USERNAME = username
            print("Logged in")
        except Exception as e:
            if type(e) == requests.exceptions.ConnectionError:
                toast("No Internet Connection")
                return
            error = eval(e.strerror)["error"]["message"]
            print(error)
            if error == "INVALID_EMAIL":
                toast("Invalid Username")
            elif error == "EMAIL_NOT_FOUND":
                toast("User does not exist")
            elif error == "INVALID_PASSWORD":
                toast("Incorrect Password")
            else:
                toast(error)
            return

        self.ids.username.text = ""
        self.ids.password.text = ""
        self.manager.current = "HomePage"
        self.manager.transition.direction = "left"

class SignUpPage(MDScreen):

    def sign_up(self):
        global AUTH, DB

        if self.ids.username.text == "":
            toast("Please Enter Username")
            return
        if self.ids.password.text == "":
            toast("Please Enter Password")
            return
        if self.ids.password.text != self.ids.re_password.text:
            toast("Password and Confirm Password do not match")
            return

        try:
            username = self.ids.username.text
            password = self.ids.password.text
            AUTH.create_user_with_email_and_password(username+"@su-gest.user", password)
        except Exception as e:
            if type(e) == requests.exceptions.ConnectionError:
                toast("No Internet Connection")
                return
            error = eval(e.strerror)["error"]["message"]
            print(error)
            if error == "INVALID_EMAIL":
                toast("Invalid Username")
            elif error == "EMAIL_EXISTS":
                toast("User already exists")
            else:
                toast(error)
            return

        DB.update({username : ""})
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.re_password.text = ""
        toast("Account Created!")
        print("Account Created")
        self.manager.current = "LoginPage"
        self.manager.transition.direction = "right"


# class WindowManager(ScreenManager):
#
#     def __init__(self, **kwargs):
#         super(WindowManager, self).__init__(**kwargs)
#         Window.bind(on_keyboard=self.on_key)
#
#     def on_key(self, window, key, *args):
#         """Maps Screens to return to on back press"""
#
#         if key == 27:  # the esc key
#             if self.current_screen.name == "LoginPage":
#                 return False  # exit the app from this page


# class LoginApp(MDApp):
#
#     def build(self):
#         self.theme_cls.theme_style = "Dark"
#         self.theme_cls.primary_palette = "Orange"
#         global CREDS, AUTH
#         try:
#             username = CREDS["User"]["username"]
#             password = CREDS["User"]["password"]
#             AUTH.sign_in_with_email_and_password(username + "@su-gest.user", password)
#             MDApp.get_running_app().root.current = "HomePage"
#         except:
#             pass
#         return None
#
#     # def on_start(self):
#
#
#
# if __name__ == '__main__':
#     app = LoginApp()
#     app.run()