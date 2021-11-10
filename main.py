"""An App that helps you decide what dish to have for your meal"""

from kivy.app import App
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from functools import partial

DATABASE_CHANGED = True
MEALS = []

class HomePage(Screen):
    pass


class MealTypeSelectionPage(Screen):
    pass


class AddRestaurantMealPage(Screen):

    meal_types = []

    def __init__(self, **kwargs):
        super(AddRestaurantMealPage, self).__init__(**kwargs)
        self.store = JsonStore("database.json")

    def get_meal_types(self, _, value, meal_type):
        if value:
            self.meal_types.append(meal_type)
        else:
            self.meal_types.remove(meal_type)

    def add_meal(self):
        self.store.put(self.ids.dish_name.text,
                       meal_type=self.meal_types,
                       restaurant_name=self.ids.restaurant_name.text,
                       restaurant_number=self.ids.restaurant_number.text,
                       delivery_links=self.ids.delivery_links.text)
        global DATABASE_CHANGED
        DATABASE_CHANGED = True


class AddHomeMadeMealPage(Screen):

    meal_types = []

    def __init__(self, **kwargs):
        super(AddHomeMadeMealPage, self).__init__(**kwargs)
        self.store = JsonStore("database.json")

    def get_meal_types(self, _, value, meal_type):
        if value:
            self.meal_types.append(meal_type)
        else:
            self.meal_types.remove(meal_type)

    def add_meal(self):
        self.store.put(self.ids.dish_name.text,
                       meal_type=self.meal_types,
                       ingredients=self.ids.ingredients.text,
                       receipe=self.ids.recipe.text)
        global DATABASE_CHANGED
        DATABASE_CHANGED = True


class ViewMealsPage(Screen):
    def __init__(self, **kwargs):
        super(ViewMealsPage, self).__init__(**kwargs)

    def on_enter(self):
        global DATABASE_CHANGED, MEALS
        if DATABASE_CHANGED:
            DATABASE_CHANGED = False
            self.store = JsonStore("database.json")
            meals = self.store.keys()
            for meal in meals:
                if meal not in MEALS:
                    MEALS.append(meal)
                    self.meal = Button(text=meal, size_hint=(0.9, None), height="50dp", on_release=self.edit_meal)
                    self.ids[meal] = self.meal
                    self.ids.grid.add_widget(self.meal)
                    self.delete = Button(text = "x", size_hint=(0.1, None), height="50dp",
                                         on_release=partial(self.delete_meal, meal))
                    self.ids[meal+"_del"] = self.meal
                    self.ids.grid.add_widget(self.delete)

    def edit_meal(self, _):
        self.manager.current = "EditRestaurantMealPage"
        self.manager.transition.direction = "left"

    def delete_meal(self, id, instance):
        self.store.delete(id)
        MEALS.remove(id)
        self.ids.grid.remove_widget(self.ids[id])
        self.ids.grid.remove_widget(instance)


class EditRestaurantMealPage(Screen):
    pass


class SuggestionPage(Screen):
    pass


class ResultPage(Screen):
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
            elif self.current_screen.name == "SuggestionPage":
                self.current = "HomePage"
                self.transition.direction = "right"
                return True  # do not exit the app
            elif self.current_screen.name == "ResultPage":
                self.current = "SuggestionPage"
                self.transition.direction = "right"
                return True  # do not exit the app


kv = Builder.load_file("mealsuggestion.kv")


class MealSuggestionApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MealSuggestionApp().run()
