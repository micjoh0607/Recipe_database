import sqlite3 as sql
import math

connection = sql.connect('recipefour.db')
c = connection.cursor()


class ingredient():
    def __init__(self, new_ingredient_name, type):
        if type == "existing":
            c.execute('''SELECT ingredient_id, ingredient_quantity, ingredient_unit, ingredient_increment, max_val, 
                                min_val
                         FROM ingredients 
                         WHERE ingredient_name = ?''', (new_ingredient_name,))

            values = c.fetchall()
            self.ingredient_id = values[0][0]
            self.ingredient_name = new_ingredient_name
            self.ingredient_quantity = values[0][1]
            self.ingredient_unit = values[0][2]
            self.ingredient_increment = values[0][3]
            self.ingredient_max_val = values[0][4]
            self.ingredient_min_val = values[0][5]

        if type == "new":
            self.ingredient_id = None
            self.ingredient_name = None
            self.ingredient_quantity = None
            self.ingredient_unit = None

    def new_ingredient(self, name, quantity, unit):
        c.execute('''INSERT INTO ingredients (ingredient_name, ingredient_quantity,ingredient_unit, ingredient_increment, min_val, max_val, ingredients_blank) 
                     VALUES(?,?,?,?,?,?,?)''',(name, quantity, unit, 1, 999999, -999999, " "))
        connection.commit()
        c.execute('''SELECT ingredient_id FROM ingredients WHERE ingredient_name = ?''',(name,))
        self.ingredient_id = c.fetchall()[0][0]
        self.ingredient_name = name
        self.ingredient_quantity = quantity
        self.ingredient_unit = unit

    def update_name(self, new_name):
        c.execute('''UPDATE ingredients
                     SET ingredient_name = ?
                     WHERE ingredient_name = ?''',(new_name, self.ingredient_name))
        self.ingredient_name = new_name
    def change_quantity(self, final_value):
        c.execute('''UPDATE ingredients 
                     SET ingredient_quantity = ? 
                     WHERE ingredient_name = ?''',(final_value,self.ingredient_name))
        connection.commit()
        self.ingredient_quantity = final_value
        return float(self.ingredient_quantity)

    def increment_quantity(self, value):
        c.execute('''UPDATE ingredients
                     SET ingredient_quantity = ?
                     WHERE ingredient_name = ?''', (self.ingredient_quantity + value, self.ingredient_name))
        connection.commit()

    def update_unit(self, new_unit):
        c.execute('''UPDATE ingredients 
                     SET ingredient_unit = ? 
                     WHERE ingredient_name = ?''',(new_unit, self.ingredient_name))
        connection.commit()

    def update_increment(self, new_increment):
        c.execute('''UPDATE ingredients
                     SET ingredient_increment = ?
                     WHERE ingredient_name = ?''',(new_increment, self.ingredient_name))
        connection.commit()

    def output_name(self):
        return self.ingredient_name

    def output_quantity(self):
        return self.ingredient_quantity

    def output_id(self):
        return str(self.ingredient_id)

    def output_unit(self):
        return str(self.ingredient_unit)

    def output_increment(self):
        return int(self.ingredient_increment)

    def output_max_val(self):
        return int(self.ingredient_max_val)

    def output_min_val(self):
        return int(self.ingredient_min_val)

    def linked_recipes(self, word):
        c.execute('''select recipe_name, recipes_blank, recipes_blank
                     from recipes,recipe_ingredients, ingredients 
                     where recipes.recipe_id = recipe_ingredients.recipe_id 
                     and recipe_ingredients.ingredient_id = ingredients.ingredient_id 
                     and ingredients.ingredient_name = ?''',(word,))
        test = c.fetchall()
        print("success")
        print(test)
        return test




