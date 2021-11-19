"""An App that helps you decide what dish to have for your meal"""

from kivy.app import App
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial
from random import choice

STORE = JsonStore("database.json")
DATABASE_CHANGED = True
MEALS = []


class HomePage(Screen):
    pass


class MealTypeSelectionPage(Screen):
    pass


class AddRestaurantMealPage(Screen):

    def add_meal(self):
        global STORE

        self.meal_types = []
        self.meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]
        for meal_id in self.meal_ids:
            if self.ids[meal_id].active:
                self.meal_types.append(meal_id)

        STORE.put(self.ids.dish_name.text,
                  meal_type=self.meal_types,
                  restaurant_name=self.ids.restaurant_name.text,
                  restaurant_number=self.ids.restaurant_number.text,
                  delivery_links=self.ids.delivery_links.text)

        for meal_id in self.meal_ids:
            self.ids[meal_id].active = False
        self.ids.dish_name.text = ""
        self.ids.restaurant_name.text = ""
        self.ids.restaurant_number.text = ""
        self.ids.delivery_links.text = ""
        global DATABASE_CHANGED
        DATABASE_CHANGED = True


class AddHomeMadeMealPage(Screen):

    def add_meal(self):
        global STORE

        self.meal_types = []
        self.meal_ids = ["Breakfast", "Lunch", "Dinner", "Snacks"]
        for meal_id in self.meal_ids:
            if self.ids[meal_id].active:
                self.meal_types.append(meal_id)

        STORE.put(self.ids.dish_name.text,
                  meal_type=self.meal_types,
                  ingredients=self.ids.ingredients.text,
                  recipe=self.ids.recipe.text)

        for meal_id in self.meal_ids:
            self.ids[meal_id].active = False
        self.ids.dish_name.text = ""
        self.ids.ingredients.text = ""
        self.ids.recipe.text = ""
        global DATABASE_CHANGED
        DATABASE_CHANGED = True


class ViewMealsPage(Screen):

    def on_enter(self):
        global DATABASE_CHANGED, MEALS, STORE
        if DATABASE_CHANGED:
            DATABASE_CHANGED = False
            STORE = JsonStore("database.json")
            meals = STORE.keys()
            for meal in meals:
                if meal not in MEALS:
                    MEALS.append(meal)
                    if "ingredients" in STORE[meal].keys():
                        function = partial(self.edit_home_made_meal, meal)
                    else:
                        function = partial(self.edit_restaurant_meal, meal)
                    self.meal = Button(text=meal, size_hint=(0.9, None), height="50dp", on_release=function)
                    self.ids[meal] = self.meal
                    self.ids.grid.add_widget(self.meal)
                    self.delete = Button(text="x", size_hint=(0.1, None), height="50dp",
                                         on_release=partial(self.delete_meal, meal))
                    self.ids.grid.add_widget(self.delete)

    def edit_restaurant_meal(self, meal, _):
        Screen = self.manager.get_screen("EditRestaurantMealPage")
        meal_type = STORE[meal]["meal_type"]
        Screen.ids.breakfast.active = False
        Screen.ids.lunch.active = False
        Screen.ids.dinner.active = False
        Screen.ids.snacks.active = False
        if "Breakfast" in meal_type:
            Screen.ids.breakfast.active = True
        if "Lunch" in meal_type:
            Screen.ids.lunch.active = True
        if "Dinner" in meal_type:
            Screen.ids.dinner.active = True
        if "Snacks" in meal_type:
            Screen.ids.snacks.active = True
        Screen.ids.dish_name.text = meal
        Screen.ids.restaurant_name.text = STORE[meal]["restaurant_name"]
        Screen.ids.restaurant_number.text = STORE[meal]["restaurant_number"]
        Screen.ids.delivery_links.text = STORE[meal]["delivery_links"]
        self.manager.current = "EditRestaurantMealPage"
        self.manager.transition.direction = "left"

    def edit_home_made_meal(self, meal, _):
        Screen = self.manager.get_screen("EditHomeMadeMealPage")
        meal_type = STORE[meal]["meal_type"]
        Screen.ids.breakfast.active = False
        Screen.ids.lunch.active = False
        Screen.ids.dinner.active = False
        Screen.ids.snacks.active = False
        if "Breakfast" in meal_type:
            Screen.ids.breakfast.active = True
        if "Lunch" in meal_type:
            Screen.ids.lunch.active = True
        if "Dinner" in meal_type:
            Screen.ids.dinner.active = True
        if "Snacks" in meal_type:
            Screen.ids.snacks.active = True
        Screen.ids.dish_name.text = meal
        Screen.ids.ingredients.text = STORE[meal]["ingredients"]
        Screen.ids.recipe.text = STORE[meal]["recipe"]
        self.manager.current = "EditHomeMadeMealPage"
        self.manager.transition.direction = "left"

    def delete_meal(self, id, instance):
        global DATABASE_CHANGED, STORE

        STORE.delete(id)
        DATABASE_CHANGED = True
        MEALS.remove(id)
        self.ids.grid.remove_widget(self.ids[id])
        self.ids.grid.remove_widget(instance)


class EditRestaurantMealPage(Screen):
    meal_types = []

    def on_enter(self):
        self.dish_name = self.ids.dish_name.text

    def get_meal_types(self, _, value, meal_type):
        if value:
            self.meal_types.append(meal_type)
        elif meal_type in self.meal_types:
            self.meal_types.remove(meal_type)

    def save_changes(self):
        global DATABASE_CHANGED, STORE

        if self.dish_name != self.ids.dish_name.text:
            pass
        STORE.put(self.ids.dish_name.text,
                  meal_type=self.meal_types,
                  restaurant_name=self.ids.restaurant_name.text,
                  restaurant_number=self.ids.restaurant_number.text,
                  delivery_links=self.ids.delivery_links.text)
        self.meal_types = []
        DATABASE_CHANGED = True


class EditHomeMadeMealPage(Screen):
    meal_types = []

    def on_enter(self):
        self.dish_name = self.ids.dish_name.text

    def get_meal_types(self, _, value, meal_type):
        if value:
            self.meal_types.append(meal_type)
        elif meal_type in self.meal_types:
            self.meal_types.remove(meal_type)

    def save_changes(self):
        global DATABASE_CHANGED, STORE
        if self.dish_name != self.ids.dish_name.text:
            pass
        STORE.put(self.ids.dish_name.text,
                  meal_type=self.meal_types,
                  ingredients=self.ids.ingredients.text,
                  recipe=self.ids.recipe.text)
        self.meal_types = []
        DATABASE_CHANGED = True


class SuggestionPage(Screen):
    pass


class ResultPage(Screen):

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
            self.ingredients_label = Label(text="Ingredients:", font_size=25, text_size=(self.width, None),
                                           halign="left", size_hint_y=None, height="30dp")
            self.ingredients = Label(text=STORE[self.meal]["ingredients"], size_hint_y=None,
                                     text_size=(self.width, None), halign="left")
            self.ingredients.bind(height=self.ingredients.setter("texture_size[1]"))
            self.recipe_label = Label(text="Recipe:", font_size=25, text_size=(self.width, None), halign="left",
                                      size_hint_y=None, height="30dp")
            self.recipe = Label(text=STORE[self.meal]["recipe"], size_hint_y=None, text_size=(self.width, None),
                                halign="left")
            self.recipe.bind(height=self.recipe.setter("texture_size[1]"))
            self.ids.meal_details.add_widget(self.ingredients_label)
            self.ids.meal_details.add_widget(self.ingredients)
            self.ids.meal_details.add_widget(Label(size_hint_y=None, height="30dp"))
            self.ids.meal_details.add_widget(self.recipe_label)
            self.ids.meal_details.add_widget(self.recipe)
        else:  # Restaurant
            self.restaurant_name_label = Label(text="Restaurant Name:", font_size=25, text_size=(self.width, None),
                                               halign="left", size_hint_y=None, height="30dp")
            self.restaurant_name = Label(text=STORE[self.meal]["restaurant_name"], size_hint_y=None,
                                         text_size=(self.width, None), halign="left")
            self.restaurant_name.bind(height=self.restaurant_name.setter("texture_size[1]"))
            self.restaurant_number_label = Label(text="Restaurant Number:", font_size=25, text_size=(self.width, None),
                                                 halign="left", size_hint_y=None, height="30dp")
            self.restaurant_number = Label(text=STORE[self.meal]["restaurant_number"], size_hint_y=None,
                                           text_size=(self.width, None), halign="left")
            self.restaurant_number.bind(height=self.restaurant_number.setter("texture_size[1]"))
            self.delivery_links_label = Label(text="Order From:", font_size=25, text_size=(self.width, None),
                                              halign="left", size_hint_y=None, height="30dp")
            self.delivery_links = Label(text=STORE[self.meal]["delivery_links"], size_hint_y=None,
                                        text_size=(self.width, None), halign="left")
            self.delivery_links.bind(height=self.delivery_links.setter("texture_size[1]"))
            self.ids.meal_details.add_widget(self.restaurant_name_label)
            self.ids.meal_details.add_widget(self.restaurant_name)
            self.ids.meal_details.add_widget(Label(size_hint_y=None, height="30dp"))
            self.ids.meal_details.add_widget(self.restaurant_number_label)
            self.ids.meal_details.add_widget(self.restaurant_number)
            self.ids.meal_details.add_widget(Label(size_hint_y=None, height="30dp"))
            self.ids.meal_details.add_widget(self.delivery_links_label)
            self.ids.meal_details.add_widget(self.delivery_links)
        self.ids.meal_details.add_widget(Label())


class WindowManager(ScreenManager):

    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        """Maps Screens to return to on back press"""

        if key == 27:  # the esc key
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


class MealSuggestionApp(App):
    pass
    # def build(self):
    #     return kv


if __name__ == "__main__":
    MealSuggestionApp().run()
