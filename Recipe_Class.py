import sqlite3 as sql
from General_applications import general
from Ingredient_Class import ingredient
import math

connection = sql.connect('recipefour.db')
c = connection.cursor()


class recipe():
    def __init__(self, new_recipe_name, type):
        self.data = general()
        if type == "current":
            c.execute('''SELECT recipe_id, serving_size
                         from recipes
                         where recipe_name = ?''', (new_recipe_name,))
            result = c.fetchall()
            self.recipe_id = result[0][0]
            self.recipe_name = new_recipe_name
            self.serving_size = result[0][1]

            c.execute('''select instruction_text, ordernum
                         from recipes, recipe_instructions, instructions
                         where recipes.recipe_id = recipe_instructions.recipe_id
                         and instructions.instruction_id = recipe_instructions.instruction_id
                         and recipes.recipe_name = ?''', (new_recipe_name,))

    def linked_ingredients(self, name):
        c.execute('''select ingredient_name, quantitynum, ingredient_unit
                     from recipes,recipe_ingredients, ingredients 
                     where recipes.recipe_id = recipe_ingredients.recipe_id 
                     and recipe_ingredients.ingredient_id = ingredients.ingredient_id 
                     and recipes.recipe_name = ?''', (name,))
        return c.fetchall()

    def linked_instructions(self, name):
        c.execute('''SELECT ordernum, instruction_text, recipes_blank
                     from instructions, recipe_instructions, recipes
                     where recipes.recipe_id = recipe_instructions.recipe_id
                     and recipe_instructions.instruction_id = instructions.instruction_id
                     and recipes.recipe_name = ?''', (name,))
        return c.fetchall()

    def linked_instruction_text(self, name):
        c.execute('''SELECT instruction_text, recipes_blank, recipes_blank
                     from instructions, recipe_instructions, recipes
                     where recipes.recipe_id = recipe_instructions.recipe_id
                     and recipe_instructions.instruction_id = instructions.instruction_id
                     and recipes.recipe_name = ?''', (name,))
        return c.fetchall()

    def total_delete(self):
        c.execute(
            '''select instruction_id from recipe_instructions, recipes where recipe_instructions.recipe_id = recipes.recipe_id and recipes.recipe_name = ?  ''',
            (self.recipe_name,))
        related_ins = c.fetchall()
        for i in range(len(related_ins)):
            c.execute('''select recipe_id from recipe_instructions where instruction_id = ? ''',
                      (((related_ins[i])[0]),))
            if len(c.fetchall()) > 1:
                pass
            else:
                c.execute('''DELETE FROM instructions where instruction_id = ?''', (((related_ins[i])[0]),))
        c.execute('''SELECT recipe_id FROM recipes where recipe_name = ?''', (self.recipe_name,))
        c.execute('''DELETE FROM recipe_ingredients where recipe_id = ?''', ((c.fetchall()[0])[0],))
        c.execute('''DELETE FROM recipes where recipe_name = ?''', (self.recipe_name,))
        c.execute('''DELETE FROM recipe_instructions where recipe_id = ?''', (self.recipe_id,))
        connection.commit()

    def output_serving_size(self):
        return str(self.serving_size)

    def output_id(self):
        return str(self.recipe_id)

    def output_name(self):
        return str(self.recipe_name)

    def update_serving_size(self, value):
        c.execute('''UPDATE recipes set serving_size = ? where recipe_name = ?''', (value, self.recipe_name))

    def update_max(self, value, ingredient):
        c.execute('''UPDATE ingredients set max_val = ? where ingredient_name = ?''', (value, ingredient))
        connection.commit()

    def update_min(self, value, ingredient):
        c.execute('''UPDATE ingredients set min_val = ? where ingredient_name = ?''', (value, ingredient))
        connection.commit()

    def update_name(self, new_name):
        c.execute('''UPDATE recipes set recipe_name = ? where recipe_name = ?''', (new_name, self.recipe_name))
        connection.commit()
        self.recipe_name = new_name

    def output_quantity_required(self, ingredient_name):
        c.execute('''select quantitynum
                     from recipe_ingredients, ingredients
                     where ingredients.ingredient_id = recipe_ingredients.ingredient_id
                     and ingredients.ingredient_name = ?
                     and recipe_id = ?''', (ingredient_name, int(self.recipe_id)))
        return c.fetchall()[0][0]

    def remove_ingredient(self, ingredient_name):
        c.execute('''DELETE from recipe_ingredients
                     WHERE recipe_id = ?
                     AND ingredient_id = ?''', (self.recipe_id, self.data.check_ingredient_id(ingredient_name)[0][0]))
        connection.commit()

    def remove_instruction(self, instruction_name):
        c.execute('''DELETE from recipe_instructions
                     WHERE recipe_id = ?
                     AND instruction_id = ?''',
                  (self.recipe_id, self.data.check_instruction_id(instruction_name)[0][0]))
        connection.commit()

    def new_recipe(self, name, instructions, ingredients, quantity, serving):
        c.execute('''INSERT INTO recipes (recipe_name, serving_size, recipes_blank) VALUES(?,?,?)''',
                  (name, serving, " "))
        connection.commit()
        c.execute('''select recipe_id from recipes where recipe_name = ?''', (name,))
        self.recipe_id = c.fetchall()[0][0]
        for i in range(len(instructions)):
            if self.data.check_duplicate(instructions[i][0], 2) == "unique":
                c.execute('''INSERT INTO instructions (instruction_text, instructions_blank) VALUES(?,?)''',
                          (instructions[i][0], " "))
                connection.commit()
            c.execute('''select instruction_id 
                         from instructions 
                         where instruction_text = ?''', (instructions[i][0],))
            instruction_id = c.fetchall()[0][0]
            c.execute(
                '''INSERT INTO recipe_instructions (recipe_id, instruction_id, ordernum, recipe_instructions_blank) VALUES(?,?,?,?)''',
                (self.recipe_id, instruction_id, str((int(i + 1))) + ".", " "))
            connection.commit()
        for i in range(len(ingredients)):
            c.execute('''select ingredient_id from ingredients where ingredient_name  = ?''', (ingredients[i][0],))
            ingredient_id = c.fetchall()[0][0]
            c.execute(
                '''INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantitynum, recipe_ingredients_blank) VALUES (?,?,?,?)''',
                (self.recipe_id, ingredient_id, quantity[i][1], " "))
            connection.commit()

            if int(self.data.check_max(ingredients[i][0])) < int(quantity[i][1]):
                self.update_max(quantity[i][1], ingredients[i][0])

            if int(self.data.check_min(ingredients[i][0])) > int(quantity[i][1]):
                self.update_min(quantity[i][1], ingredients[i][0])

    def make_recipe(self):
        flag = True
        lst = self.linked_ingredients(self.recipe_name)
        for i in lst:
            if flag:
                format_lst = [i[0]]
                format_lst[0] = ingredient(format_lst[0], "existing")
                if i[1] > format_lst[0].output_quantity():
                    flag = False
            else:
                break
        if flag:
            for i in lst:
                format_lst = [i[0]]
                format_lst[0] = ingredient(format_lst[0], "existing")
                format_lst[0].change_quantity(format_lst[0].output_quantity() - i[1])
            return True
        if not flag:
            return False
