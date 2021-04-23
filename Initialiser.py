import sqlite3 as sql
import math
connection = sql.connect('recipefour.db')

connection.execute('''PRAGMA foreign_keys = 1''')

c = connection.cursor()

def initialise():
    try:
        c.execute('''DROP TABLE recipe_ingredients''')
        c.execute('''DROP TABLE recipe_instructions''')
        c.execute('''DROP TABLE instructions''')
        c.execute('''DROP TABLE ingredients''')
        c.execute('''DROP TABLE recipes''')
        c.execute('''DROP TABLE shopping_list''')
        c.execute('''DROP TABLE list_items''')
    except:
        pass

    #creating the database tables
    try:
        c.execute('''CREATE TABLE recipes (recipe_id integer PRIMARY KEY, recipe_name text, serving_size integer, recipes_blank text) ''')
        c.execute('''CREATE TABLE instructions (instruction_id integer PRIMARY KEY, instruction_text text, 
                     instructions_blank text)''')
        c.execute('''CREATE TABLE ingredients (ingredient_id integer PRIMARY KEY, ingredient_name text, ingredient_quantity 
                     float, ingredient_unit text, ingredient_increment integer, max_val integer, min_val integer, 
                     ingredients_blank text) ''')
        c.execute('''CREATE TABLE recipe_instructions (recipe_instruction_id integer PRIMARY KEY, recipe_id integer 
                     references recipes(recipe_id) on update cascade on delete cascade, instruction_id integer references 
                     instructions(instruction_id) on update cascade on delete cascade , ordernum integer, 
                     recipe_instructions_blank text)''')
        c.execute('''CREATE TABLE recipe_ingredients (recipe_ingredient_id integer PRIMARY KEY, recipe_id integer 
                     references recipes(recipe_id) on update cascade on delete cascade, ingredient_id integer references 
                     ingredients(ingredient_id) on update cascade on delete cascade, quantitynum integer, 
                     recipe_ingredients_blank text)''')
        c.execute('''CREATE TABLE shopping_list (shopping_list_id integer PRIMARY KEY, start_date text, end_date text, status text, shopping_list_blank text)''')
        c.execute('''CREATE TABLE list_items (list_item_id integer PRIMARY KEY, shopping_list_id integer, ingredient_name integer, quantity integer, list_items_blank text)''')



    except:
        pass

    c.execute('''INSERT INTO ingredients 
             (ingredient_name, ingredient_quantity, ingredient_unit, ingredient_increment, max_val, min_val, ingredients_blank)
             VALUES(?,?,?,?,?,?,?)''', ("water", math.inf, "ml", 1, -9999999, 9999999, ""))
    connection.commit()
