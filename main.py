"""An App that helps you decide what dish to have for your meal"""
from kivy.properties import StringProperty
from kivy.uix.screenmanager import NoTransition, SlideTransition, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from random import choice
from kivymd.uix.card import MDCardSwipe, MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.menu import MDDropdownMenu

from login import *

Window.size = (350, 650)
Window.softinput_mode = "below_target"
STORE = JsonStore("database.json")
DATABASE_CHANGED = True
USERNAME = ""
MEALS = []


class MyButton(MDFillRoundFlatButton):
    pass


class MyBoxLayout(BoxLayout):
    pass


class SwipeToDeleteItem(MDCardSwipe):
    pass


class Content(BoxLayout):
    pass


class MD3Card(MDCard, RoundedRectangularElevationBehavior):
    pass


class MyCard(MD3Card):
    title = StringProperty()
    content = StringProperty()


class AccountPage(MDScreen):

    def on_pre_enter(self):
        global CREDS
        self.ids.username.text = "Hi, "+CREDS["User"]["username"]

    def confirm(self, _):
        self.dialog = MDDialog(
            title="[color=ffffff]Confirm Logout?[/color]",
            text="Are you sure you want to logout?",
            buttons=[
                MDFlatButton(text="Cancel", on_release=self.close_confirm),
                MDFlatButton(text="Yes", on_release=self.logout)
            ]

        )
        self.dialog.open()

    def close_confirm(self, _):
        self.dialog.dismiss()

    def logout(self, _):
        global CREDS

        CREDS.clear()
        self.manager.current = "LoginPage"
        self.manager.transition.direction = "right"
        toast("Successfully Logged Out!")
        print("Logged Out")
        self.dialog.dismiss()


class SettingsPage(MDScreen):
    pass


class ChangePasswordPage(MDScreen):
    pass


class HomePage(MDScreen):
    pass


class MealTypeSelectionPage(MDScreen):
    pass


class AddRestaurantMealPage(MDScreen):

    def on_pre_enter(self):
        # Setting Checkbox color
        self.ids.Breakfast.unselected_color = 1, 0.64, 0, 1
        self.ids.Lunch.unselected_color = 1, 0.64, 0, 1
        self.ids.Snacks.unselected_color = 1, 0.64, 0, 1
        self.ids.Dinner.unselected_color = 1, 0.64, 0, 1

    def add_meal(self):
        global DATABASE_CHANGED, STORE
        meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]

        if not (self.ids[meal_ids[0]].active or self.ids[meal_ids[1]].active or
                self.ids[meal_ids[2]].active or self.ids[meal_ids[3]].active):
            toast("Choose at least one meal type")
            return
        if self.ids.dish_name.text == "":
            toast("Dish name cannot be blank")
            return
        if self.ids.restaurant_name.text == "":
            toast("Restaurant name cannot be blank")
            return
        meals = DB.child(USERNAME).get().val()
        if meals != "":
            if self.ids.dish_name.text in meals.keys():
                toast("Dish name already exists")
                return
        if self.ids.restaurant_number.text == "":
            self.ids.restaurant_number.text = "No number provided"
        if self.ids.delivery_links.text == "":
            self.ids.delivery_links.text = "No delivery links provided"

        meal_types = []
        for meal_id in meal_ids:
            if self.ids[meal_id].active:
                meal_types.append(meal_id)
        DB.child(USERNAME).update({self.ids.dish_name.text: {
                                   "meal_type": meal_types,
                                   "restaurant_name": self.ids.restaurant_name.text,
                                   "restaurant_number": self.ids.restaurant_number.text,
                                   "delivery_links": self.ids.delivery_links.text}})

        self.manager.current = "HomePage"
        self.manager.transition.direction = "right"

        for meal_id in meal_ids:
            self.ids[meal_id].active = False
        self.ids.dish_name.text = ""
        self.ids.restaurant_name.text = ""
        self.ids.restaurant_number.text = ""
        self.ids.delivery_links.text = ""

        DATABASE_CHANGED = True
        toast("Dish successfully added!")


class AddHomeMadeMealPage(MDScreen):

    def on_pre_enter(self):
        # Setting Checkbox color
        self.ids.Breakfast.unselected_color = 1, 0.64, 0, 1
        self.ids.Lunch.unselected_color = 1, 0.64, 0, 1
        self.ids.Snacks.unselected_color = 1, 0.64, 0, 1
        self.ids.Dinner.unselected_color = 1, 0.64, 0, 1

    def add_meal(self):
        global DATABASE_CHANGED, DB
        meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]

        if not (self.ids[meal_ids[0]].active or self.ids[meal_ids[1]].active or
                self.ids[meal_ids[2]].active or self.ids[meal_ids[3]].active):
            toast("Choose at least one meal type")
            return
        if self.ids.dish_name.text == "":
            toast("Dish name cannot be blank")
            return
        if self.ids.ingredients.text == "":
            toast("Ingredients name cannot be blank")
            return
        if self.ids.recipe.text == "":
            toast("Recipe name cannot be blank")
            return
        meals = DB.child(USERNAME).get().val()
        if meals != "":
            if self.ids.dish_name.text in meals.keys():
                toast("Dish name already exists")
                return

        meal_types = []
        for meal_id in meal_ids:
            if self.ids[meal_id].active:
                meal_types.append(meal_id)
        DB.child(USERNAME).update({self.ids.dish_name.text: {
                                   "meal_type": meal_types,
                                   "ingredients": self.ids.ingredients.text,
                                   "recipe": self.ids.recipe.text}})

        self.manager.current = "HomePage"
        self.manager.transition.direction = "right"

        for meal_id in meal_ids:
            self.ids[meal_id].active = False
        self.ids.dish_name.text = ""
        self.ids.ingredients.text = ""
        self.ids.recipe.text = ""

        DATABASE_CHANGED = True
        toast("Dish successfully added!")


class ViewMealsPage(MDScreen):

    def on_pre_enter(self):
        global DATABASE_CHANGED, MEALS, DB, USERNAME
        if DATABASE_CHANGED:
            DATABASE_CHANGED = False
            meals = DB.child(USERNAME).get()
            if meals.val() == "" and "no_meal" not in self.ids:
                label = MDLabel(text="No meals to display", size_hint=(1, None), halign="center",
                                     theme_text_color="Custom", text_color=(1, 0.5, 0, 1))
                self.ids["no_meal"] = label
                self.ids.grid.add_widget(label)
            elif meals.val() != "" and "no_meal" in self.ids:
                self.ids.grid.remove_widget(self.ids["no_meal"])
                del self.ids["no_meal"]
            if meals.val() != "" and "delete_all" not in self.ids:
                delete_all = MDRaisedButton(text="Delete all meals",
                                            md_bg_color=(0.75, 0, 0.05, 1),
                                            size_hint=(1, None),
                                            text_color=(0, 0, 0, 0.9),
                                            on_release=self.confirm)
                self.ids["delete_all"] = delete_all
                self.ids.grid.add_widget(delete_all, index=0)
            for meal in meals:
                if meal.key() not in MEALS:
                    MEALS.append(meal.key())
                    list_item = SwipeToDeleteItem()
                    list_item.text = meal.key()
                    if "recipe" in meal.val().keys():
                        function = self.edit_home_made_meal
                    else:
                        function = self.edit_restaurant_meal
                    list_item.children[1].children[0].on_release = partial(self.delete_meal, list_item)
                    list_item.children[0].children[0].on_release = partial(function, meal, list_item)
                    self.ids.grid.add_widget(list_item, index=len(self.ids.grid.children)+1)

    def edit_restaurant_meal(self, meal, list_item):
        if list_item.ids.content.pos[0] != 0:
            return
        Screen = self.manager.get_screen("EditRestaurantMealPage")
        meal_type = meal.val()["meal_type"]
        meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]
        for meal_id in meal_ids:
            Screen.ids[meal_id].active = False
            if meal_id in meal_type:
                Screen.ids[meal_id].active = True
        Screen.ids.dish_name.text = meal.key()
        Screen.ids.restaurant_name.text = meal.val()["restaurant_name"]
        Screen.ids.restaurant_number.text = meal.val()["restaurant_number"]
        Screen.ids.delivery_links.text = meal.val()["delivery_links"]
        self.manager.current = "EditRestaurantMealPage"
        self.manager.transition.direction = "left"

    def edit_home_made_meal(self, meal, list_item):
        if list_item.ids.content.pos[0] != 0:
            return
        Screen = self.manager.get_screen("EditHomeMadeMealPage")
        meal_type = meal.val()["meal_type"]
        self.meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]
        for meal_id in self.meal_ids:
            Screen.ids[meal_id].active = False
            if meal_id in meal_type:
                Screen.ids[meal_id].active = True
        Screen.ids.dish_name.text = meal.key()
        Screen.ids.ingredients.text = meal.val()["ingredients"]
        Screen.ids.recipe.text = meal.val()["recipe"]
        self.manager.current = "EditHomeMadeMealPage"
        self.manager.transition.direction = "left"

    def delete_meal(self, list_item):
        global DATABASE_CHANGED, DB, MEALS
        DB.child(USERNAME).child(list_item.text).remove()
        DATABASE_CHANGED = True
        MEALS.remove(list_item.text)
        self.ids.grid.remove_widget(list_item)
        if len(MEALS) == 0:
            DB.update({USERNAME : ""})
            self.ids.grid.remove_widget(self.ids["delete_all"])
            del self.ids["delete_all"]
            self.label = MDLabel(text="No meals to display", size_hint=(1, None), halign="center",
                                 theme_text_color="Custom", text_color=(1, 0.5, 0, 1))
            self.ids["no_meal"] = self.label
            self.ids.grid.add_widget(self.label)

    def confirm(self, _):
        self.dialog = MDDialog(
            title="[color=ffffff]Confirm Delete?[/color]",
            text="Are you sure you want to delete all meals?",
            buttons=[
                MDFlatButton(text="Cancel", on_release=self.close_confirm),
                MDFlatButton(text="Yes", on_release=self.delete_all_meals)
            ]

        )
        self.dialog.open()

    def close_confirm(self, _):
        self.dialog.dismiss()

    def delete_all_meals(self, _):
        global DATABASE_CHANGED, MEALS, DB
        self.dialog.dismiss()
        DB.update({USERNAME: ""})
        DATABASE_CHANGED = True
        self.ids.grid.clear_widgets()
        del self.ids["delete_all"]
        MEALS = []
        label = MDLabel(text="No meals to display", size_hint=(1, None), halign="center",
                        theme_text_color="Custom", text_color=(1, 0.5, 0, 1))
        self.ids["no_meal"] = label
        self.ids.grid.add_widget(label)


class EditRestaurantMealPage(MDScreen):

    def on_pre_enter(self):
        # Setting Checkbox color
        self.ids.Breakfast.unselected_color = 1, 0.64, 0, 1
        self.ids.Lunch.unselected_color = 1, 0.64, 0, 1
        self.ids.Snacks.unselected_color = 1, 0.64, 0, 1
        self.ids.Dinner.unselected_color = 1, 0.64, 0, 1

        # Storing Dish name
        self.dish_name = self.ids.dish_name.text

        # Setting Textfield focus
        self.ids.dish_name.focus = True
        self.ids.restaurant_name.focus = True
        self.ids.restaurant_number.focus = True
        self.ids.delivery_links.focus = True

    def save_changes(self):
        global DATABASE_CHANGED, DB, MEALS
        meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]

        if not (self.ids[meal_ids[0]].active or self.ids[meal_ids[1]].active or
                self.ids[meal_ids[2]].active or self.ids[meal_ids[3]].active):
            toast("Choose at least one meal type")
            return
        if self.ids.dish_name.text == "":
            toast("Dish name cannot be blank")
            return
        if self.ids.restaurant_name.text == "":
            toast("Restaurant name cannot be blank")
            return

        if self.dish_name != self.ids.dish_name.text:
            if self.ids.dish_name.text in DB.child(USERNAME).get().val().keys():
                toast("Dish name already exists")
                return
            Screen = self.manager.get_screen("ViewMealsPage")
            DB.child(USERNAME).child(self.dish_name).remove()
            Screen.ids.grid.remove_widget(Screen.ids.grid.children[MEALS.index(self.dish_name)+1])
            MEALS.remove(self.dish_name)

        meal_types = []
        for meal_id in meal_ids:
            if self.ids[meal_id].active:
                meal_types.append(meal_id)

        if self.ids.restaurant_number.text == "":
            self.ids.restaurant_number.text = "No number provided"
        if self.ids.delivery_links.text == "":
            self.ids.delivery_links.text = "No delivery links provided"

        DB.child(USERNAME).update({self.ids.dish_name.text: {
                                   "meal_type": meal_types,
                                   "restaurant_name": self.ids.restaurant_name.text,
                                   "restaurant_number": self.ids.restaurant_number.text,
                                   "delivery_links": self.ids.delivery_links.text}})

        DATABASE_CHANGED = True
        self.manager.current = "ViewMealsPage"
        self.manager.transition.direction = "right"


class EditHomeMadeMealPage(MDScreen):

    def on_enter(self):
        # Setting Checkbox color
        self.ids.Breakfast.unselected_color = 1, 0.64, 0, 1
        self.ids.Lunch.unselected_color = 1, 0.64, 0, 1
        self.ids.Snacks.unselected_color = 1, 0.64, 0, 1
        self.ids.Dinner.unselected_color = 1, 0.64, 0, 1

        # Storing Dish name
        self.dish_name = self.ids.dish_name.text

        # Setting Textfield focus
        self.ids.dish_name.focus = True
        self.ids.recipe.focus = True
        self.ids.ingredients.focus = True

    def save_changes(self):
        global DATABASE_CHANGED, DB, MEALS
        meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]

        if not (self.ids[meal_ids[0]].active or self.ids[meal_ids[1]].active or
                self.ids[meal_ids[2]].active or self.ids[meal_ids[3]].active):
            toast("Choose at least one meal type")
            return
        if self.ids.dish_name.text == "":
            toast("Dish name cannot be blank")
            return
        if self.ids.ingredients.text == "":
            toast("Ingredients name cannot be blank")
            return
        if self.ids.recipe.text == "":
            toast("Recipe name cannot be blank")
            return

        if self.dish_name != self.ids.dish_name.text:
            if self.ids.dish_name.text in DB.child(USERNAME).get().val().keys():
                toast("Dish name already exists")
                return
            Screen = self.manager.get_screen("ViewMealsPage")
            DB.child(USERNAME).child(self.dish_name).remove()
            Screen.ids.grid.remove_widget(Screen.ids.grid.children[MEALS.index(self.dish_name) + 1])
            MEALS.remove(self.dish_name)

        meal_types = []
        for meal_id in meal_ids:
            if self.ids[meal_id].active:
                meal_types.append(meal_id)

        DB.child(USERNAME).update({self.ids.dish_name.text: {
                                   "meal_type": meal_types,
                                   "ingredients": self.ids.ingredients.text,
                                   "recipe": self.ids.recipe.text}})

        DATABASE_CHANGED = True
        self.manager.current = "ViewMealsPage"
        self.manager.transition.direction = "right"


class SuggestionPage(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.create_dropdown(0.75, "Choose Meal From", "meal_from", "Home-made", "Restaurant", "Mix")
        self.create_dropdown(0.5, "Choose Meal Type", "meal_type", "Breakfast", "Lunch", "Dinner", "Snacks")


    def create_dropdown(self, y, title, id, *items):
        content = Content()
        for item in items:
            button = MDRaisedButton(size_hint=(1, None), height="70dp", text=item)
            content.add_widget(button)

        dropdown = MDExpansionPanel(
            content=content,
            panel_cls=MDExpansionPanelOneLine(
                text=title,
                theme_text_color="Custom",
                text_color=(0, 0, 0, 0.9)
            ),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5, "center_y": y}
        )
        dropdown.chevron.children[0].theme_text_color = 'Custom'
        dropdown.chevron.children[0].text_color = (0, 0, 0, 1)
        dropdown.panel_cls._txt_left_pad = 10
        self.ids.box.add_widget(dropdown)
        self.ids[id] = dropdown
        for button in dropdown.content.children:
            button.on_release = partial(self.press, dropdown, button.text)

    def press(self, dropdown, text):
        dropdown.children[1].text = text
        dropdown.check_open_panel(dropdown.children[1])

    def result(self):
        global DB, USERNAME
        meal_from = self.ids.meal_from.children[0].text
        if meal_from == "Choose Meal From":
            toast("Please Choose Meal From")
            return
        meal_type = self.ids.meal_type.children[0].text
        if meal_type == "Choose Meal Type":
            toast("Please Choose Meal Type")
            return
        self.options = []

        for meal in DB.child(USERNAME).get():
            if meal_type in meal.val()["meal_type"]:
                if meal_from == "Home-made" and ("ingredients" in meal.val().keys()):
                    self.options.append(meal)
                elif meal_from == "Restaurant" and ("restaurant_name" in meal.val().keys()):
                    self.options.append(meal)
                elif meal_from == "Mix":
                    self.options.append(meal)

        if self.options == []:
            toast("No meals for this category")
        else:
            self.manager.current = "ResultPage"
            self.manager.transition.direction = "left"


class ResultPage(MDScreen):

    def on_enter(self):
        self.options = self.manager.get_screen("SuggestionPage").options
        meal = choice(self.options)
        self.ids.dish_name.text = meal.key()
        self.ids.meal_details.clear_widgets()
        if "ingredients" in meal.val().keys():  # Home-made
            ingredients = MyCard(title="Ingredients", content=meal.val()["ingredients"])
            recipe = MyCard(title="Recipe", content=meal.val()["recipe"])
            self.ids.meal_details.add_widget(ingredients)
            self.ids.meal_details.add_widget(recipe)
        else:  # Restaurant
            restaurant_name = MyCard(title="Restaurant Name", content=meal.val()["restaurant_name"])
            restaurant_number = MyCard(title="Restaurant Number", content=meal.val()["restaurant_number"])
            delivery_links = MyCard(title="Delivery Links", content=meal.val()["delivery_links"])
            self.ids.meal_details.add_widget(restaurant_name)
            self.ids.meal_details.add_widget(restaurant_number)
            self.ids.meal_details.add_widget(delivery_links)

    def change(self):
        if len(self.options) == 1:
            toast("Only 1 meal added for this category")
            return
        self.on_enter()


class WindowManager(ScreenManager):

    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)
        self.transition = NoTransition()

    def on_key(self, window, key, *args):
        """Maps Screens to return to on back press"""

        if key == 27:  # the esc key
            if self.current_screen.name == "LoginPage":
                return False  # exit the app from this page
            if self.current_screen.name == "SignUpPage":
                self.current = "LoginPage"
                self.transition.direction = "right"
                return True  # do not exit the app
            if self.current_screen.name == "AccountPage":
                self.current = MealSuggestionApp.previous
                self.transition.direction = "right"
                return True  # do not exit the app
            if self.current_screen.name == "SettingsPage":
                self.current = MealSuggestionApp.previous
                self.transition.direction = "right"
                return True  # do not exit the app
            if self.current_screen.name == "HomePage":
                return False  # exit the app from this page
            elif self.current_screen.name == "MealTypeSelectionPage":
                self.current = "HomePage"
                self.transition.direction = "right"
                return True  # do not exit the app
            elif self.current_screen.name == "AddRestaurantMealPage":
                self.current = "MealTypeSelectionPage"
                self.transition.direction = "right"
                return True  # do not exit the app
            elif self.current_screen.name == "AddHomeMadeMealPage":
                self.current = "MealTypeSelectionPage"
                self.transition.direction = "right"
                return True  # do not exit the app
            elif self.current_screen.name == "ViewMealsPage":
                self.current = "HomePage"
                self.transition.direction = "right"
                return True  # do not exit the app
            elif self.current_screen.name == "EditRestaurantMealPage":
                self.current = "ViewMealsPage"
                self.transition.direction = "right"
                return True  # do not exit the app
            elif self.current_screen.name == "EditHomeMadeMealPage":
                self.current = "ViewMealsPage"
                self.transition.direction = "right"
                return True  # do not exit the app
            elif self.current_screen.name == "SuggestionPage":
                self.current = "HomePage"
                self.transition.direction = "right"
                return True  # do not exit the app
            elif self.current_screen.name == "ResultPage":
                self.current = "SuggestionPage"
                self.transition.direction = "right"
                return True  # do not exit the app


# kv = Builder.load_file("mealsuggestion.kv")


class MealSuggestionApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "A700"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Cyan"
        # self.theme_cls.primary_hue = "100"

        self.check_login()
        self.set_menu()

        return None

    def check_login(self):
        global CREDS, AUTH, USERNAME
        try:
            username = CREDS["User"]["username"]
            password = CREDS["User"]["password"]
            AUTH.sign_in_with_email_and_password(username + "@su-gest.user", password)
            USERNAME = username
            MDApp.get_running_app().root.current = "HomePage"
        except Exception as e:
            print("Exception", e)
        WindowManager.transition = SlideTransition()

    def set_menu(self):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Account",
                "height": dp(50),
                "on_release": lambda x=f"AccountPage": self.menu_callback(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Settings",
                "height": dp(50),
                "on_release": lambda x=f"SettingsPage": self.menu_callback(x),
            }
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=1.8,
        )

    def callback(self, button):
        if not self.menu.caller:
            self.menu.caller = button  # Required to open the menu
        self.menu.open()

    def menu_callback(self, page):
        MealSuggestionApp.previous = MDApp.get_running_app().root.current
        MDApp.get_running_app().root.current = page
        self.menu.dismiss()



if __name__ == "__main__":
    MealSuggestionApp().run()
