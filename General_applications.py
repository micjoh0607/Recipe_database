import sqlite3 as sql
connection = sql.connect('recipefour.db')
c = connection.cursor()
import datetime

class general():
    def __init__(self):
        pass
    def general_names(self, word, type):
        if type == "Ingredients":
            c.execute('''SELECT ingredient_name, ingredients_blank, ingredients_blank
                         from ingredients 
                         where ingredient_name 
                         like "{}%"'''.format(word))
            mylist = c.fetchall()
            return mylist
        else:
            c.execute('''SELECT recipe_name , recipes_blank, recipes_blank
                         from recipes
                         where recipe_name 
                         like "{}%"'''.format(word))
            mylist = c.fetchall()
            return mylist

    def check_duplicate(self, word, type):
        status = "unique"
        if type == 1:
            c.execute('''SELECT recipe_name from recipes where recipe_name = ?''', (word,))
            if c.fetchall() != []:
                status = "duplicate"
        if type == 2:
            c.execute('''select instruction_text from instructions where instruction_text = ?''', (str(word),))
            if c.fetchall() != []:
                status = "duplicate"
        if type == 3:
            c.execute('''select ingredient_name from ingredients where ingredient_name = ?''', (word,))
            if c.fetchall() != []:
                status = "duplicate"
        return status

    def linked_ingredients(self, name):
        c.execute('''select ingredient_name
                     from recipes,recipe_ingredients, ingredients 
                     where recipes.recipe_id = recipe_ingredients.recipe_id 
                     and recipe_ingredients.ingredient_id = ingredients.ingredient_id 
                     and recipes.recipe_name = ?''', (name,))
        return c.fetchall()

    def check_max(self, ingredient):
        c.execute('''select max_val
                     from ingredients
                     where ingredient_name = ?''', (ingredient,))
        return c.fetchall()[0][0]

    def check_min(self, ingredient):
        c.execute('''select min_val
                     from ingredients
                     where ingredient_name = ?''', (ingredient,))
        return c.fetchall()[0][0]

    def check_recipe_id(self, name):
        c.execute('''SELECT recipe_id
                      FROM recipes
                      WHERE recipe_name = ?''', (name,))
        return c.fetchall()

    def check_ingredient_id(self, name):
        c.execute('''SELECT ingredient_id
                      FROM ingredients
                      WHERE ingredient_name = ?''', (name,))
        return c.fetchall()

    def check_instruction_id(self, name):
        c.execute('''SELECT instruction_id
                     FROM instructions
                     WHERE instruction_text = ?''', (name,))
        return c.fetchall()

    def check_shopping_list(self):
        c.execute('''SELECT shopping_list_id
                     FROM shopping_list
                     WHERE status == ?''', ("incomplete",))
        return c.fetchall()

    def shopping_list_items(self):
        c.execute('''SELECT ingredient_name, quantity, list_items_blank
                     FROM list_items
                     WHERE shopping_list_id = ? ''', (self.check_shopping_list()[0][0],))
        return c.fetchall()
        
    def create_shopping_list(self):
        c.execute('''INSERT 
                     INTO shopping_list (start_date, end_date, status, shopping_list_blank)
                     VALUES(?, ?, ?, ?)''', (datetime.datetime.now().strftime("%x"), "", "incomplete", ""))
        connection.commit()

    def add_to_list(self, name, quantity):
        c.execute('''INSERT
                     INTO list_items (shopping_list_id, ingredient_name, quantity, list_items_blank)
                     VALUES(?,?,?,?)''', (self.check_shopping_list()[0][0], name, quantity, ""))
        connection.commit()

    def list_delete(self, name):
        c.execute('''DELETE 
                     FROM list_items
                     WHERE ingredient_name = ?''', (name, ))
        connection.commit()

    def complete_list(self):
        c.execute('''UPDATE shopping_list
                     SET status = ?
                     AND end_date = ?
                     WHERE status = ?''', ("complete", datetime.datetime.now().strftime("%x"), "incomplete"))
        connection.commit()


