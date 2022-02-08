"""An App that helps you decide what dish to have for your meal"""

from kivy.uix.screenmanager import NoTransition, SlideTransition, ScreenManager
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from random import choice
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.label import MDLabel

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


class HomePage(MDScreen):
    pass


class MealTypeSelectionPage(MDScreen):
    pass


class AddRestaurantMealPage(MDScreen):

    def on_pre_enter(self):
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

        for meal_id in meal_ids:
            self.ids[meal_id].active = False
        self.ids.dish_name.text = ""
        self.ids.restaurant_name.text = ""
        self.ids.restaurant_number.text = ""
        self.ids.delivery_links.text = ""

        DATABASE_CHANGED = True
        toast("Dish successfully added!")
        self.manager.current = "HomePage"
        self.manager.transition.direction = "right"


class AddHomeMadeMealPage(MDScreen):

    def on_pre_enter(self):
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

        for meal_id in meal_ids:
            self.ids[meal_id].active = False
        self.ids.dish_name.text = ""
        self.ids.ingredients.text = ""
        self.ids.recipe.text = ""

        DATABASE_CHANGED = True
        toast("Dish successfully added!")
        self.manager.current = "HomePage"
        self.manager.transition.direction = "right"


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
                                            on_release=self.delete_all_meals)
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

    def delete_all_meals(self, _):
        global DATABASE_CHANGED, MEALS, DB
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

    def on_enter(self):
        self.dish_name = self.ids.dish_name.text

    def save_changes(self):
        global DATABASE_CHANGED, STORE
        self.meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]

        if not (self.ids[self.meal_ids[0]].active or self.ids[self.meal_ids[1]].active or
                self.ids[self.meal_ids[2]].active or self.ids[self.meal_ids[3]].active):
            toast("Choose at least one meal type")
            return
        if self.ids.dish_name.text == "":
            toast("Dish name cannot be blank")
            return
        if self.ids.restaurant_name.text == "":
            toast("Restaurant name cannot be blank")
            return
        if self.ids.restaurant_number.text == "":
            self.ids.restaurant_number.text = "No number provided"
        if self.ids.delivery_links.text == "":
            self.ids.delivery_links.text = "No delivery links provided"

        self.meal_types = []
        for meal_id in self.meal_ids:
            if self.ids[meal_id].active:
                self.meal_types.append(meal_id)

        if self.dish_name != self.ids.dish_name.text:
            if self.ids.dish_name.text in STORE.keys():
                toast("Dish name already exists")
                return
            Screen = self.manager.get_screen("ViewMealsPage")
            Screen.delete_meal(self.dish_name, self)

        STORE.put(self.ids.dish_name.text,
                  meal_type=self.meal_types,
                  restaurant_name=self.ids.restaurant_name.text,
                  restaurant_number=self.ids.restaurant_number.text,
                  delivery_links=self.ids.delivery_links.text)

        DATABASE_CHANGED = True
        self.manager.current = "ViewMealsPage"
        self.manager.transition.direction = "right"


class EditHomeMadeMealPage(MDScreen):

    def on_enter(self):
        self.dish_name = self.ids.dish_name.text

    def save_changes(self):
        global DATABASE_CHANGED, STORE
        self.meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]

        if not (self.ids[self.meal_ids[0]].active or self.ids[self.meal_ids[1]].active or
                self.ids[self.meal_ids[2]].active or self.ids[self.meal_ids[3]].active):
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

        self.meal_types = []
        for meal_id in self.meal_ids:
            if self.ids[meal_id].active:
                self.meal_types.append(meal_id)

        if self.dish_name != self.ids.dish_name.text:
            if self.ids.dish_name.text in STORE.keys():
                toast("Dish name already exists")
                return
            Screen = self.manager.get_screen("ViewMealsPage")
            Screen.delete_meal(self.dish_name, self)

        STORE.put(self.ids.dish_name.text,
                  meal_type=self.meal_types,
                  ingredients=self.ids.ingredients.text,
                  recipe=self.ids.recipe.text)

        DATABASE_CHANGED = True
        self.manager.current = "ViewMealsPage"
        self.manager.transition.direction = "right"


class SuggestionPage(MDScreen):

    def result(self):
        global STORE
        self.meal_type = self.manager.get_screen("SuggestionPage").ids.meal_type.text
        self.meal_from = self.manager.get_screen("SuggestionPage").ids.meal_from.text
        self.options = []
        for meal in STORE:
            if self.meal_type in STORE[meal]["meal_type"]:
                if self.meal_from == "Home-made" and ("ingredients" in STORE[meal].keys()):
                    self.options.append(meal)
                elif self.meal_from == "Restaurant" and ("restaurant_name" in STORE[meal].keys()):
                    self.options.append(meal)
                elif self.meal_from == "Mix":
                    self.options.append(meal)
        if self.options == []:
            toast("No meals for this category")
        else:
            self.manager.current = "ResultPage"
            self.manager.transition.direction = "left"


class ResultPage(MDScreen):

    def on_enter(self):
        global STORE
        self.meal_type = self.manager.get_screen("SuggestionPage").ids.meal_type.text
        self.meal_from = self.manager.get_screen("SuggestionPage").ids.meal_from.text
        self.options = []
        for meal in STORE:
            if self.meal_type in STORE[meal]["meal_type"]:
                if self.meal_from == "Home-made" and ("ingredients" in STORE[meal].keys()):
                    self.options.append(meal)
                elif self.meal_from == "Restaurant" and ("restaurant_name" in STORE[meal].keys()):
                    self.options.append(meal)
                elif self.meal_from == "Mix":
                    self.options.append(meal)
        self.meal = choice(self.options)
        self.ids.dish_name.text = self.meal
        self.ids.meal_details.clear_widgets()
        if "ingredients" in STORE[self.meal].keys():  # Home-made
            self.ingredients_label = Label(text="Ingredients:", font_size="25dp", size_hint_y=None, padding_y="10dp")
            self.set_label(self.ingredients_label)
            self.ingredients = Label(text=STORE[self.meal]["ingredients"], size_hint_y=None)
            self.set_label(self.ingredients)
            self.ids.meal_details.add_widget(Label(size_hint_y=None, height="30dp"))
            self.recipe_label = Label(text="Recipe:", font_size="25dp", size_hint_y=None, padding_y="10dp")
            self.set_label(self.recipe_label)
            self.recipe = Label(text=STORE[self.meal]["recipe"], size_hint_y=None)
            self.set_label(self.recipe)
        else:  # Restaurant
            self.restaurant_name_label = Label(text="Restaurant Name:", font_size="25dp", size_hint_y=None,
                                               padding_y="10dp")
            self.set_label(self.restaurant_name_label)
            self.restaurant_name = Label(text=STORE[self.meal]["restaurant_name"], size_hint_y=None)
            self.set_label(self.restaurant_name)
            self.ids.meal_details.add_widget(Label(size_hint_y=None, height="30dp"))
            self.restaurant_number_label = Label(text="Restaurant Number:", font_size="25dp", size_hint_y=None,
                                                 padding_y="10dp")
            self.set_label(self.restaurant_number_label)
            self.restaurant_number = Label(text=STORE[self.meal]["restaurant_number"], size_hint_y=None)
            self.set_label(self.restaurant_number)
            self.delivery_links_label = Label(text="Order From:", font_size="25dp", size_hint_y=None,
                                              padding_y="10dp")
            self.ids.meal_details.add_widget(Label(size_hint_y=None, height="30dp"))
            self.set_label(self.delivery_links_label)
            self.delivery_links = Label(text=STORE[self.meal]["delivery_links"], size_hint_y=None)
            self.set_label(self.delivery_links)
        self.ids.meal_details.add_widget(Label())

    def set_label(self, label):
        label.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))
        label.bind(texture_size=label.setter('size'))
        self.ids.meal_details.add_widget(label)

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
        return None


if __name__ == "__main__":
    MealSuggestionApp().run()
