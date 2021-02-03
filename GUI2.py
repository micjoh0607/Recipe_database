from Ingredient_Class import ingredient  # creates ingredients as an object and uses methods to extract from database
from Recipe_Class import recipe  # creates recipes as an object and uses methods to extract from database
from General_applications import general  # finds general database results that fall between ingredients and recipes
from Initialiser import Initialise  # clears and initialises the database
import tkinter as tk
import re


class TkinterShell(tk.Frame):
    def __init__(self, master):
        self.master = master  # creates main window
        self.data = general()
        self.master.resizable(0, 0)
        self.master.title("Recipe Maker")
        self.search_type = ["Ingredients", "Recipes"]  # Search filter options
        self.search_flag = 0
        self.master.bind("<Key>", self.key_update)  # binds all keys to function that updates the main scroll list

        self.introduction_text = tk.Label(self.master, text="Welcome Back User!")
        self.introduction_text.grid(row=0, column=0, sticky="nw")

        self.master_button_frame = tk.Frame(self.master, bg="grey")  # creates a frame for all the buttons to sit in
        self.master_button_frame.grid(row=3, column=0, sticky="nw", padx=(5, 5), pady=5)

        self.button_instruction_text = tk.Label(self.master, text="What would you like to do?")
        self.button_instruction_text.grid(row=2, column=0, sticky="s")
        self.scroll_instruction_text = tk.Label(self.master, text="You currently have:")
        self.scroll_instruction_text.grid(row=2, column=2)

        self.border_canvas = tk.Canvas(self.master, width=1, height=310, bg="black")

        self.master_search_text = tk.Label(self.master, text="Filter by:")
        self.master_search_text.grid(row=0, column=2, sticky="nw")
        self.master_search_filter_button = tk.Button(self.master, text=self.search_type[self.search_flag],
                                                     command=lambda: self.search_filter())  # flips filter of search box
        self.master_search_filter_button.grid(row=0, column=2)
        self.master_search_box = tk.Entry(self.master)  # search box for the main list
        self.master_search_box.grid(row=1, column=2, pady=10)

        self.main_scroller = ScrollList(self.master, sorted(
            self.data.general_names(self.master_search_box.get(), self.search_type[self.search_flag])), [3, 2], 200,
                                        self.data, self.search_type[self.search_flag], [0, 1, 2])  # creates main list

        self.exit_button = tk.Button(self.master, text="Exit", command=lambda: self.close_programme(1))
        self.exit_button.grid(row=4, column=2, sticky="ne")  # Button that closes main window
        self.clear_button = tk.Button(self.master, text="Clear", command=lambda: self.clear())
        self.clear_button.grid(row=4, column=2, sticky="nw")  # Button that clears the database

        self.new_ingredient_button = tk.Button(self.master_button_frame, text="Add New Ingredient", width=25,
                                               command=lambda: self.new_ingredient("", 2))  # Opens new ingredient tab
        self.new_ingredient_button.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.new_recipe_button = tk.Button(self.master_button_frame, text="Add New Recipe", width=25,
                                           command=lambda: self.new_recipe([], [], "", False))
        self.new_recipe_button.grid(row=1, column=0, sticky="nw", padx=5, pady=5)  # opens new recipe tab
        self.available_recipe_button = tk.Button(self.master_button_frame, text="Search For Available Recipes",
                                                 width=25,
                                                 command=lambda: self.available_recipes())  # opens available recipe tab
        self.available_recipe_button.grid(row=2, column=0, padx=5, pady=5)
        self.shopping_list_button = tk.Button(self.master_button_frame, text="View Shopping List", width=25,
                                              command=lambda: self.view_shopping_list(""))  # opens shopping list tab
        self.shopping_list_button.grid(row=3, column=0, padx=5, pady=5)

    def clear(self):
        Initialise()  # clears database
        self.main_scroller.update_scroll(
            sorted(self.data.general_names(self.master_search_box.get(), self.search_type[self.search_flag])),
            "", 20, self.search_type[self.search_flag], "")

    def key_update(self, event):  # it says parameter "event not used" but it is required for the bound keys to update
        self.main_scroller.update_scroll(
            sorted(self.data.general_names(self.master_search_box.get(), self.search_type[self.search_flag])),
            "", 20, self.search_type[self.search_flag], "")  # updates scroller

    def search_filter(self):
        if self.search_flag == 0:
            self.search_flag += 1
        else:
            self.search_flag -= 1
        self.master_search_filter_button.configure(text=self.search_type[self.search_flag])
        self.main_scroller.update_scroll(
            sorted(self.data.general_names(self.master_search_box.get(), self.search_type[self.search_flag])),
            "", 20, self.search_type[self.search_flag], "")

    def button_decision(self, option, name):
        if option == "Ingredients":
            self.ingredients(name, "")
        if option == "Recipes":
            self.recipes(name, "")

    def ingredients(self, name, window):
        if window == "":
            ingredient_window = tk.Tk()
            ingredient_window.resizable(0, 0)
        else:
            ingredient_window = window

        ingredient_name_lst = [name]
        ingredient_name_lst[0] = ingredient(ingredient_name_lst[0], "existing")

        ingredient_introduction_frame = tk.Frame(ingredient_window)
        ingredient_introduction_frame.grid(row=0, column=0, sticky="nw")
        ingredient_work_frame = tk.Frame(ingredient_window)
        ingredient_work_frame.grid(row=1, column=0, sticky="nw")

        ingredient_id_title = tk.Button(ingredient_introduction_frame,
                                        text="ID: #" + ingredient_name_lst[0].output_id(),
                                        state=tk.DISABLED, width=25)
        ingredient_id_title.grid(row=0, column=0, sticky="nw")
        ingredient_name_title = tk.Button(ingredient_introduction_frame, text="Name: " + str(name),
                                          state=tk.DISABLED,
                                          width=25)
        ingredient_name_title.grid(row=1, column=0, sticky="nw")
        ingredient_quantity_title = tk.Button(ingredient_introduction_frame,
                                              text="Quantity: " + str(
                                                  ingredient_name_lst[0].output_quantity()) + " " + str(
                                                  ingredient_name_lst[0].output_unit()),
                                              state=tk.DISABLED, width=25)
        ingredient_quantity_title.grid(row=2, column=0, sticky="nw")
        ingredient_scroller = ScrollList(ingredient_window,
                                         sorted(ingredient_name_lst[0].linked_recipes(str(name))), [2, 0], 50,
                                         self.data, "Recipes", [0, 1, 2])

        tk.Label(ingredient_work_frame, text="_______________________").grid(row=0, column=0, columnspan=3)
        tk.Label(ingredient_work_frame, text="New Value:").grid(row=1, column=1)
        tk.Button(ingredient_work_frame, text="<<",
                  command=lambda: increment_new_value(update_value.get(), new_value.get(), 1)).grid(
            row=2, column=0, padx=2, pady=1)
        new_value = tk.Entry(ingredient_work_frame, width=5)
        new_value.grid(row=2, column=1)
        new_value.insert(10, ingredient_name_lst[0].output_quantity())
        tk.Button(ingredient_work_frame, text=">>",
                  command=lambda: increment_new_value(update_value.get(), new_value.get(), 2)).grid(
            row=2, column=2, padx=2, pady=1)
        tk.Label(ingredient_work_frame, text="Increment ").grid(row=3, column=0, sticky="sw")
        tk.Label(ingredient_work_frame, text="by: ").grid(row=4, column=0, sticky="nw")
        update_value = tk.Entry(ingredient_work_frame, width=3)
        update_value.grid(row=4, column=0)
        update_value.insert(0, ingredient_name_lst[0].output_increment())
        tk.Button(ingredient_work_frame, text="Confirm", command=lambda: commit_change()).grid(row=4, column=2,
                                                                                               sticky="w")
        tk.Label(ingredient_work_frame, text="_______________________").grid(row=5, column=0, columnspan=3)
        tk.Label(ingredient_work_frame, text="Ingredient used in:").grid(row=6, column=0, columnspan=3)

        ingredient_close_button = tk.Button(ingredient_window, text="Close",
                                            command=lambda: ingredient_window.destroy())
        ingredient_close_button.grid(row=7, column=0, sticky="se", padx=10, pady=10)

        ingredient_edit_button = tk.Button(ingredient_window, text="Edit", command=lambda: edit_ingredient())
        ingredient_edit_button.grid(row=7, column=0, sticky="sw", padx=10, pady=10)

        ingredient_shopping_list_button = tk.Button(ingredient_window, text="Add to List", command=lambda:
                                                    self.add_to_shopping_list(ingredient_name_lst[0].output_name(), ""))
        ingredient_shopping_list_button.grid(row=7, column=0, padx=10, pady=10)

        def edit_ingredient():
            for widget in ingredient_introduction_frame.winfo_children():
                widget.destroy()
            ingredient_scroller.update_scroll(sorted(ingredient_name_lst[0].linked_recipes(str(name))),
                                              "Ingredient_link", 17, "Recipes", name)
            ingredient_edit_button.grid_forget()

            ingredient_edit_id_title = tk.Button(ingredient_introduction_frame,
                                                 text="ID: #" + ingredient_name_lst[0].output_id(),
                                                 state=tk.DISABLED, width=25)
            ingredient_edit_id_title.grid(row=0, column=0, sticky="nw")

            ingredient_edit_name_title = tk.Entry(ingredient_introduction_frame, width=30, justify="center")
            ingredient_edit_name_title.grid(row=1, column=0, sticky="nw")
            ingredient_edit_name_title.insert(0, ingredient_name_lst[0].output_name())

            ingredient_edit_quantity_title = tk.Entry(ingredient_introduction_frame, width=20, justify="center")
            ingredient_edit_quantity_title.grid(row=2, column=0, sticky="nw")
            ingredient_edit_quantity_title.insert(0, ingredient_name_lst[0].output_quantity())

            ingredient_unit_title = tk.Entry(ingredient_introduction_frame, width=10, justify="center")
            ingredient_unit_title.grid(row=2, column=0, sticky="ne")
            ingredient_unit_title.insert(0, ingredient_name_lst[0].output_unit())

            ingredient_save_button = tk.Button(ingredient_window, text="Save", command=lambda: save_changes())
            ingredient_save_button.grid(row=7, column=0, sticky="nw", padx=10, pady=10)

            def save_changes():
                ingredient_name_lst[0].update_name(ingredient_edit_name_title.get().lower())
                ingredient_name_lst[0].change_quantity(ingredient_edit_quantity_title.get())
                ingredient_name_lst[0].update_unit(ingredient_unit_title.get())
                ingredient_name_lst[0].update_increment(update_value.get())

                for edit_widget in ingredient_window.winfo_children():
                    edit_widget.destroy()

                self.main_scroller.update_scroll(
                    sorted(self.data.general_names(self.master_search_box.get(), self.search_type[self.search_flag])),
                    "", 20, self.search_type[self.search_flag], "")
                self.ingredients(ingredient_name_lst[0].output_name(), ingredient_window)

        def commit_change():
            ingredient_name_lst[0].change_quantity(int(new_value.get()))
            ingredient_name_lst[0].update_increment(int(update_value.get()))
            ingredient_quantity_title.configure(
                text="Quantity: " + str(new_value.get()) + " " + str(ingredient_name_lst[0].output_unit()))

        def increment_new_value(current_update_value, current_new_value, format_type):
            new_value.delete(0, 'end')
            if format_type == 1:
                if (int(current_new_value) - int(current_update_value)) >= 0:
                    new_value.insert(0, (int(current_new_value) - int(current_update_value)))
                else:
                    new_value.insert(0, 0)
            else:
                if (int(current_new_value) + int(current_update_value)) >= 0:
                    new_value.insert(0, (int(current_new_value) + int(current_update_value)))
                else:
                    new_value.insert(0, 0)

    def recipes(self, name, window):
        self.close_programme(3)
        if window == "":
            recipe_window = tk.Tk()
            recipe_window.resizable(0, 0)
        else:
            recipe_window = window

        recipe_name_lst = [name]
        recipe_name_lst[0] = recipe(recipe_name_lst[0], "current")

        recipe_introduction_frame = tk.Frame(recipe_window)
        recipe_introduction_frame.grid(row=0, column=0, sticky="nw")
        recipe_work_frame = tk.Frame(recipe_window)
        recipe_work_frame.grid(row=1, column=0, sticky="nw")

        recipe_id_title = tk.Button(recipe_introduction_frame, text="ID: # " + recipe_name_lst[0].output_id(),
                                    state=tk.DISABLED, width=25)
        recipe_id_title.grid(row=0, column=0, sticky="nw")
        recipe_name_title = tk.Button(recipe_introduction_frame, text="Name: " + str(name), state=tk.DISABLED,
                                      width=25)
        recipe_name_title.grid(row=1, column=0, sticky="nw")

        ingredient_title = tk.Label(recipe_window, text="Ingredients Required:", font=('Arial', 9, 'bold', 'underline'))
        ingredient_title.grid(row=2, column=0)
        ingredient_scroller = ScrollList(recipe_window, sorted(recipe_name_lst[0].linked_ingredients(name)),
                                         [3, 0], 100, self.data, "Ingredients", [1, 2, 0])

        instruction_title = tk.Label(recipe_window, text="Recipe Instructions:", font=('Arial', 9, 'bold', 'underline'))
        instruction_title.grid(row=4, column=0)
        instruction_scroller = ScrollList(recipe_window, sorted(recipe_name_lst[0].linked_instructions(name)),
                                          [5, 0], 100, self.data, "Instructions", [0, 1, 2])

        exit_button = tk.Button(recipe_window, text="Close", command=lambda: recipe_window.destroy())
        exit_button.grid(row=6, column=0, sticky="ne", padx=5, pady=5)
        edit_button = tk.Button(recipe_window, text="Edit", command=lambda: edit_recipe())
        edit_button.grid(row=6, column=0, sticky="nw", padx=5, pady=5)
        make_button = tk.Button(recipe_window, text="Make", command=lambda: recipe_name_lst[0].make_recipe())
        make_button.grid(row=6, column=0, padx=5, pady=5)

        def edit_recipe():
            for widget in recipe_introduction_frame.winfo_children():
                widget.destroy()

            recipe_edit_id_title = tk.Button(recipe_introduction_frame, text="ID: # " + recipe_name_lst[0].output_id(),
                                             state=tk.DISABLED, width=25)
            recipe_edit_id_title.grid(row=0, column=0, sticky="nw")

            recipe_edit_name_title = tk.Entry(recipe_introduction_frame, width=30, justify="center")
            recipe_edit_name_title.grid(row=1, column=0, sticky="nw")
            recipe_edit_name_title.insert(0, recipe_name_lst[0].output_name())

            ingredient_scroller.update_scroll(sorted(recipe_name_lst[0].linked_ingredients(str(name))), "Recipe_link",
                                              17, "Recipes", name)
            instruction_scroller.update_scroll(sorted(recipe_name_lst[0].linked_instruction_text(name)),
                                               "Instruction_link", 17, "Recipes", name)

            edit_button.grid_forget()
            save_button = tk.Button(recipe_window, text="Save", command=lambda: save())
            save_button.grid(row=6, column=0, sticky="nw", padx=5, pady=5)

            ingredient_update_button = tk.Button(recipe_window, text="➕", command=lambda: update_recipe(),
                                                 font=('Arial', 9, 'bold'))
            ingredient_update_button.grid(row=2, column=0, sticky="ne")
            instruction_update_button = tk.Button(recipe_window, text="➕", command=lambda: update_recipe(),
                                                  font=('Arial', 9, 'bold'))
            instruction_update_button.grid(row=4, column=0, sticky="ne")

            def update_recipe():
                self.new_recipe(sorted(recipe_name_lst[0].linked_instruction_text(name)),
                                sorted(recipe_name_lst[0].linked_ingredients(name)), recipe_name_lst[0].output_name(),
                                True)
                recipe_window.destroy()

            def save():
                recipe_name_lst[0].update_name(recipe_edit_name_title.get())

                for save_widget in recipe_window.winfo_children():
                    save_widget.destroy()

                self.main_scroller.update_scroll(
                    sorted(self.data.general_names(self.master_search_box.get(), self.search_type[self.search_flag])),
                    "", 20, self.search_type[self.search_flag], "")
                self.recipes(recipe_name_lst[0].output_name(), recipe_window)

    def new_ingredient(self, name, case_type):
        new_ingredient_window = tk.Tk()
        new_ingredient_window.resizable(0, 0)

        new_ingredient_work_frame = tk.Frame(new_ingredient_window)
        new_ingredient_work_frame.grid(row=1, column=0, sticky="nw")

        new_ingredient_introduction = tk.Button(new_ingredient_window, text="Enter the new ingredient below:",
                                                state="disabled")
        new_ingredient_introduction.grid(row=0, column=0, pady=(0, 5), sticky="nw")

        new_ingredient_name_label = tk.Label(new_ingredient_work_frame, text="Name:")
        new_ingredient_name_label.grid(row=0, column=0, sticky="nw")
        new_ingredient_name_entry = tk.Entry(new_ingredient_work_frame)
        new_ingredient_name_entry.grid(row=0, column=1, padx=(0, 5))

        if case_type == 1:
            new_ingredient_name_entry.insert(0, name)

        new_ingredient_quantity_label = tk.Label(new_ingredient_work_frame, text="Current quantity:")
        new_ingredient_quantity_label.grid(row=1, column=0)
        new_ingredient_quantity_entry = tk.Entry(new_ingredient_work_frame)
        new_ingredient_quantity_entry.grid(row=1, column=1, padx=(0, 5))

        new_ingredient_unit_label = tk.Label(new_ingredient_work_frame, text="Unit:")
        new_ingredient_unit_label.grid(row=2, column=0, sticky="nw")
        new_ingredient_unit_entry = tk.Entry(new_ingredient_work_frame)
        new_ingredient_unit_entry.grid(row=2, column=1, padx=(0, 5))

        new_ingredient_confirm = tk.Button(new_ingredient_work_frame, text="Confirm",
                                           command=lambda: confirm())
        new_ingredient_confirm.grid(row=3, column=1, padx=5, pady=5, sticky="ne")

        def confirm():
            if self.data.check_duplicate(new_ingredient_name_entry.get().lower(), 3) == "unique" and not re.match(
                    "^\s*$",
                    (new_ingredient_name_entry.get()).lower()):
                word_lst = [new_ingredient_name_entry.get().lower()]
                word_lst[0] = ingredient(word_lst[0], "new")
                word_lst[0].new_ingredient(new_ingredient_name_entry.get().lower(),
                                           new_ingredient_quantity_entry.get(),
                                           new_ingredient_unit_entry.get())
                self.main_scroller.update_scroll(
                    sorted(self.data.general_names(self.master_search_box.get(), self.search_type[self.search_flag])),
                    "", 20, self.search_type[self.search_flag], "")
                new_ingredient_window.destroy()
            else:
                if not re.match("^\s*$", new_ingredient_name_entry.get()):
                    self.existing_input_error("Ingredients", new_ingredient_name_entry.get(), new_ingredient_window)
                else:
                    self.false_input_error()

    def new_recipe(self, instructions, ingredients, name, overwrite):

        new_recipe_window = tk.Tk()
        new_recipe_window.resizable(0, 0)

        new_recipe_name_label = tk.Label(new_recipe_window, text="Name: ")
        new_recipe_name_label.grid(row=0, column=0, sticky="ne")
        new_recipe_name_entry = tk.Entry(new_recipe_window)
        new_recipe_name_entry.grid(row=0, column=1, sticky="nw")
        new_recipe_name_entry.insert(0, name)

        self.new_recipe_instruction_section = NewRecipe(new_recipe_window, "Instructions", self.data, [1, 0],
                                                        "Instruction", 14, instructions)
        self.new_recipe_ingredient_section = NewRecipe(new_recipe_window, "Ingredients", self.data, [1, 1],
                                                       "Ingredients", 14, ingredients)
        if name != "":
            self.new_recipe_instruction_section.scroll()
            self.new_recipe_ingredient_section.scroll()

        new_recipe_confirm_button = tk.Button(new_recipe_window, text="Confirm", command=lambda: new_recipe_confirm())
        new_recipe_confirm_button.grid(row=2, column=1, sticky="ne", padx=10, pady=10)

        def new_recipe_confirm():
            if overwrite:
                overwrite_lst = [name]
                overwrite_lst[0] = recipe(overwrite_lst[0], "current")
                overwrite_lst[0].total_delete()
                print("success")

            if self.data.check_duplicate(new_recipe_name_entry.get(), 1) == "unique" and not re.match("^\s*$",
                                                                            (new_recipe_name_entry.get()).lower()):
                word_lst = [new_recipe_name_entry.get().lower()]
                word_lst[0] = recipe(word_lst, "new")

                word_lst[0].new_recipe(new_recipe_name_entry.get().lower(),
                                       self.new_recipe_instruction_section.output_list(),
                                       self.new_recipe_ingredient_section.output_list(),
                                       self.new_recipe_ingredient_section.output_list())
                self.main_scroller.update_scroll(
                    sorted(self.data.general_names(self.master_search_box.get(), self.search_type[self.search_flag])),
                    "", 20, self.search_type[self.search_flag], "")
                new_recipe_window.destroy()

            else:
                if not re.match("^\s*$", new_recipe_name_entry.get()):
                    self.existing_input_error("Recipes", new_recipe_name_entry.get(), new_recipe_window)
                else:
                    self.false_input_error()

    '''
    def available(self):
        available_recipe_window = tk.Tk()
        available_recipe_window.resizable(0, 0)
        recipe_list = [self.data.general_names("", "Recipes")[i][0] for i in
                       range(len(self.data.general_names("", "Recipes")))]
        ingredient_list = [self.data.general_names("", "Ingredients")[i][0] for i in
                           range(len(self.data.general_names("", "Ingredients")))]
        amalgamation = {recipe_list[i]: [self.data.linked_ingredients(recipe_list[i])[j][0] for j in
                                         range(len(self.data.linked_ingredients(recipe_list[i])))] for i in
                        range(len(recipe_list))}
        recipe_reject = []
        scores = []

        for i in amalgamation:
            score = 0
            ingredients = amalgamation[i]
            i = recipe(i, "current")
            for j in ingredients:
                j = ingredient(j, "existing")
                if j.output_quantity() < i.output_quantity_required(j.output_name()):
                    recipe_reject.append(i.output_name())
                    score += 1
            if i.output_name() in recipe_reject:
                scores.append(score)
        recipe_list = list(set(recipe_list) ^ set(recipe_reject))

        recipe_list = [[i, "", ""] for i in recipe_list]

        available_recipe_title = tk.Label(available_recipe_window, text="Available Recipes:",
                                          font=('Arial', 9, 'bold', 'underline'))
        available_recipe_title.grid(row=0, column=0)

        available_recipe_divider = tk.Label(available_recipe_window, text="__________________")
        available_recipe_divider.grid(row=1, column=0)

        available_recipe_scroller = ScrollList(available_recipe_window, recipe_list, [2, 0], 100, self.data, "Recipes",
                                               [0, 1, 2])

        print(scores)
    '''

    def available_recipes(self):
        available_recipe_window = tk.Tk()
        available_recipe_window.resizable(0, 0)
        recipe_list = [self.data.general_names("", "Recipes")[i][0] for i in
                       range(len(self.data.general_names("", "Recipes")))]
        ingredient_list = [self.data.general_names("", "Ingredients")[i][0] for i in
                           range(len(self.data.general_names("", "Ingredients")))]
        amalgamation = {recipe_list[i]: [self.data.linked_ingredients(recipe_list[i])[j][0] for j in
                                         range(len(self.data.linked_ingredients(recipe_list[i])))] for i in
                        range(len(recipe_list))}
        recipe_reject = []
        for i in ingredient_list:
            i = ingredient(i, "existing")
            if i.output_min_val() > i.output_quantity():
                for j in range(len(recipe_list)):
                    if i.output_name() in amalgamation[recipe_list[j]]:
                        recipe_reject.append(recipe_list[j])
        recipe_list = list(set(recipe_list) ^ set(recipe_reject))
        amalgamation = {recipe_list[i]: [self.data.linked_ingredients(recipe_list[i])[j][0] for j in
                                         range(len(self.data.linked_ingredients(recipe_list[i])))] for i in
                        range(len(recipe_list))}
        recipe_reject = []

        if recipe_list:
            for i in amalgamation:
                ingredients = amalgamation[i]
                i = recipe(i, "current")
                for j in ingredients:
                    j = ingredient(j, "existing")
                    if j.output_quantity() < i.output_quantity_required(j.output_name()):
                        recipe_reject.append(i.output_name())
            recipe_list = list(set(recipe_list) ^ set(recipe_reject))

        recipe_list = [[i, "", ""] for i in recipe_list]

        available_recipe_title = tk.Label(available_recipe_window, text="Available Recipes:",
                                          font=('Arial', 9, 'bold', 'underline'))
        available_recipe_title.grid(row=0, column=0)

        available_recipe_divider = tk.Label(available_recipe_window, text="__________________")
        available_recipe_divider.grid(row=1, column=0)

        available_recipe_scroller = ScrollList(available_recipe_window, recipe_list, [2, 0], 100, self.data, "Recipes",
                                               [0, 1, 2])

    def view_shopping_list(self, window):

        def show_shopping_list():
            shopping_list_scroll = ScrollList(shopping_list_frame, self.data.shopping_list_items(), [0, 0], 200,
                                              self.data, "", [0, 1, 2])
            shopping_list_scroll.update_scroll(self.data.shopping_list_items(), "Shopping_list", 14, "Ingredients", "")
            shopping_list_add_button = tk.Button(shopping_list_frame, text="New Entry", command=lambda:
                                                 self.add_to_shopping_list("", shopping_list_scroll))
            shopping_list_add_button.grid(row=1, column=0, sticky="nw", padx=10, pady=10)
            shopping_list_complete_button = tk.Button(shopping_list_frame, text="Complete", command=lambda: complete())
            shopping_list_complete_button.grid(row=1, column=0, sticky="ne", padx=10, pady=10)

            def complete():
                for i in self.data.shopping_list_items():
                    format_lst = [i[0], i[1], i[2]]
                    format_lst[0] = ingredient(i[0], "existing")
                    format_lst[0].increment_quantity(i[1])
                self.data.complete_list()
                for widget in shopping_list_window.winfo_children():
                    widget.destroy()
                self.view_shopping_list(shopping_list_window)

        if window == "":
            shopping_list_window = tk.Tk()
            shopping_list_window.resizable(0, 0)
        else:
            shopping_list_window = window

        shopping_list_title = tk.Label(shopping_list_window, text="Shopping List", font=('Arial', 9, 'bold', 'underline'))
        shopping_list_title.grid(row=0, column=0)

        shopping_list_frame = tk.Frame(shopping_list_window, bg="grey")
        shopping_list_frame.grid(row=1, column=0)

        if not self.data.check_shopping_list():
            shopping_list_create = tk.Button(shopping_list_frame, text="Create Shopping\n List", width=20, command=
            lambda: create_shopping_list())
            shopping_list_create.grid(row=0, column=0, padx=5, pady=5)
        else:
            show_shopping_list()

        def create_shopping_list():
            self.data.create_shopping_list()
            shopping_list_create.destroy()
            show_shopping_list()

    def add_to_shopping_list(self, name, scroller):

        add_to_shopping_list_window = tk.Tk()
        add_to_shopping_list_window.resizable(0, 0)

        add_to_shopping_list_work_frame = tk.Frame(add_to_shopping_list_window)
        add_to_shopping_list_work_frame.grid(row=1, column=0, sticky="nw")

        add_to_shopping_list_introduction = tk.Button(add_to_shopping_list_window, text="Enter the ingredient below:",
                                                       state="disabled")
        add_to_shopping_list_introduction.grid(row=0, column=0, pady=(0, 5), sticky="nw")

        add_to_shopping_list_name_label = tk.Label(add_to_shopping_list_work_frame, text="Name:")
        add_to_shopping_list_name_label.grid(row=0, column=0, sticky="nw")
        add_to_shopping_list_name_entry = tk.Entry(add_to_shopping_list_work_frame)
        add_to_shopping_list_name_entry.grid(row=0, column=1, padx=(0, 5))

        add_to_shopping_list_name_entry.insert(0, name)

        add_to_shopping_list_quantity_label = tk.Label(add_to_shopping_list_work_frame, text="Order Quantity:")

        add_to_shopping_list_quantity_entry = tk.Entry(add_to_shopping_list_work_frame)
        add_to_shopping_list_quantity_entry.grid(row=1, column=1, padx=(0, 5))

        add_to_shopping_list_confirm = tk.Button(add_to_shopping_list_work_frame, text="Confirm", command=lambda:
                                                 item_confirm())
        add_to_shopping_list_confirm.grid(row=3, column=1, padx=5, pady=5, sticky="ne")

        def item_confirm():
            if not self.data.check_shopping_list():
                self.data.create_shopping_list()
            self.data.add_to_list(add_to_shopping_list_name_entry.get().lower(),
                                  add_to_shopping_list_quantity_entry.get().lower())
            add_to_shopping_list_window.destroy()
            if scroller != "":
                scroller.update_scroll(self.data.shopping_list_items(), "Shopping_list", 14, "Ingredients", "")

    def false_input_error(self):
        error_window = tk.Tk()
        error_window.resizable(0, 0)

        error_text = "Error: invalid input!"

        error_label = tk.Label(error_window, text=error_text)
        error_label.grid(row=0, column=0)

        error_frame = tk.Frame(error_window)
        error_frame.grid(row=1, column=0)

        error_accept_button = tk.Button(error_frame, text="OK", width=10,
                                        command=lambda: error_window.destroy())
        error_accept_button.grid(row=0, column=1, padx=5, pady=5, sticky="se")

    def existing_input_error(self, error_type, name, window):

        error_window = tk.Tk()
        error_window.resizable(0, 0)

        error_text = "Error: item already exists!"

        error_label = tk.Label(error_window, text=error_text)
        error_label.grid(row=0, column=0)

        error_frame = tk.Frame(error_window)
        error_frame.grid(row=1, column=0)

        new_ingredient_update_button = tk.Button(error_frame, text="Update item",
                                                 width=10, command=lambda: error_update())
        new_ingredient_update_button.grid(row=0, column=0, padx=5, pady=5, sticky="se")
        new_ingredient_accept_button = tk.Button(error_frame, text="OK", width=10,
                                                 command=lambda: error_window.destroy())
        new_ingredient_accept_button.grid(row=0, column=1, padx=5, pady=5, sticky="se")

        def error_update():
            error_window.destroy()
            if error_type == "Recipes":
                self.recipes(name, "")
            if error_type == "Ingredients":
                self.ingredients(name, "")
            window.destroy()

    def information_box(self, information_text):
        information_window = tk.Tk()
        information_window.resizable(0, 0)

        information_label = tk.Label(information_window, text=information_text)
        information_label.grid(row=0, column=0)

        information_frame = tk.Frame(information_window)
        information_frame.grid(row=1, column=0)

        information_accept_button = tk.Button(information_frame, information_window.destroy())
        information_accept_button.grid(row=0, column=1, padx=5, pady=5, sticky="se")

    def delete(self, i, format_list, cancel_list, recipe_type, scroller):
        if recipe_type == "Instructions":
            self.new_recipe_instruction_section.delete(i, format_list, cancel_list)
        if recipe_type == "Ingredients":
            self.new_recipe_ingredient_section.delete(i, format_list, cancel_list)
        if recipe_type == "Ingredient_link":
            format_list[0] = recipe(format_list[0], "current")
            format_list[0].remove_ingredient(cancel_list)
            ingredient_list = [cancel_list]
            ingredient_list[0] = ingredient(ingredient_list[0], "existing")
            scroller.update_scroll(ingredient_list[0].linked_recipes(ingredient_list[0].output_name()),
                                   "Ingredient_link", 17, "Recipes", ingredient_list[0].output_name())
        if recipe_type == "Recipe_link":
            cancel_list = [cancel_list]
            cancel_list[0] = recipe(cancel_list[0], "current")
            cancel_list[0].remove_ingredient(format_list[0])
            format_list[0] = ingredient(format_list[0], "existing")
            scroller.update_scroll(cancel_list[0].linked_ingredients(cancel_list[0].output_name()), "Recipe_link", 17,
                                   "Ingredients", format_list[0].output_name())
        if recipe_type == "Instruction_link":
            cancel_list = [cancel_list]
            cancel_list[0] = recipe(cancel_list[0], "current")
            cancel_list[0].remove_instruction(format_list[0])
            scroller.update_scroll(cancel_list[0].linked_instruction_text(cancel_list[0].output_name()),
                                   "Instruction_link", 17,
                                   "Recipes", format_list[0])

        if recipe_type == "Shopping_list":
            self.data.list_delete(format_list[0])
            scroller.update_scroll(self.data.shopping_list_items(), "Shopping_list", 14, "Ingredients", "")

    def close_programme(self, close_type):
        try:
            if close_type == 1:
                self.master.destroy()
            # if type == 1 or type == 2:
            # self.ingredient_window.destroy()
            # if type == 1 or type == 3:
            # self.recipe_window.destroy()
        except:
            pass


class NewRecipe():
    def __init__(self, window, format_type, data, coordinates, header, width, edit):
        self.format_type = format_type
        self.window = window
        self.data = data
        self.coordinates = coordinates
        self.header = header
        self.new_recipe_list = edit
        self.width = width

        new_recipe_work_frame = tk.Frame(self.window)
        new_recipe_work_frame.grid(row=self.coordinates[0], column=self.coordinates[1])

        new_recipe_label = tk.Label(new_recipe_work_frame, text=self.header)
        new_recipe_label.grid(row=0, column=1)

        self.new_recipe_number = tk.Button(new_recipe_work_frame, text=(self.header + " #1:"), state="disabled")
        self.new_recipe_number.grid(row=1, column=0)

        if self.format_type == "Instructions":
            self.new_recipe_entry = tk.Entry(new_recipe_work_frame, width=28)
        else:
            self.new_recipe_entry = tk.Entry(new_recipe_work_frame, width=22)
            self.new_recipe_quantity = tk.Entry(new_recipe_work_frame, width=6)
            self.new_recipe_quantity.grid(row=1, column=1, sticky="ne")
            self.new_recipe_quantity.bind("<Return>", self.user_input)
        self.new_recipe_entry.grid(row=1, column=1, sticky="nw")
        self.new_recipe_entry.bind("<Return>", self.user_input)
        self.new_recipe_scroller = ScrollList(new_recipe_work_frame, self.new_recipe_list, [2, 1], 100, self.data,
                                              self.header, [0, 1, 2])

    def scroll(self):
        self.new_recipe_scroller.update_scroll(self.new_recipe_list, self.format_type, self.width, self.header, "")

    def user_input(self, event):
        if self.format_type == "Instructions":
            if not re.match("^\s*$", self.new_recipe_entry.get()):
                self.new_recipe_list.append((self.new_recipe_entry.get(), " "))
            else:
                self.false_input_error()
        else:
            if not re.match("^\s*$", self.new_recipe_entry.get()) and not re.match("^\s*$",
                                                                                   self.new_recipe_quantity.get()):
                if self.data.check_duplicate(self.new_recipe_entry.get(), 3) == "unique":
                    main.new_ingredient(self.new_recipe_entry.get().lower(), 1)
                self.new_recipe_list.append(
                    (self.new_recipe_entry.get().lower(), self.new_recipe_quantity.get().lower()))
            else:
                main.false_input_error()
        self.new_recipe_scroller.update_scroll(self.new_recipe_list, self.format_type, self.width, self.header, "")
        self.new_recipe_entry.delete(0, 'end')
        if self.format_type != "Instructions":
            self.new_recipe_quantity.delete(0, 'end')
        self.new_recipe_number["text"] = (self.header + " #" + str(len(self.new_recipe_list) + 1))

    def delete(self, i, format_list, cancel_list):
        self.new_recipe_list.pop(i)
        self.new_recipe_scroller.update_scroll(self.new_recipe_list, self.format_type, self.width, self.header, "")
        self.new_recipe_number["text"] = (self.header + " #" + str(len(self.new_recipe_list) + 1))

    def output_list(self):
        return self.new_recipe_list


class ScrollList():
    def __init__(self, window, button_list, coorindates, height, data, scroll_type, order):
        self.window = window
        self.button_list = button_list
        self.coordinates = coorindates
        self.height = height
        self.data = data
        self.scroll_type = scroll_type
        self.order = order

        self.scroll_label_frame = tk.LabelFrame(self.window)
        self.scroll_label_frame.grid(row=self.coordinates[0], column=self.coordinates[1])

        self.scroll_search_canvas = tk.Canvas(self.scroll_label_frame, width=150, height=self.height)
        self.scroll_search_canvas.grid(row=0, column=0, rowspan=3, columnspan=2)

        self.scroll_y_scrollbar = tk.Scrollbar(self.scroll_label_frame, orient="vertical",
                                               command=self.scroll_search_canvas.yview)
        self.scroll_y_scrollbar.grid(row=0, column=2, rowspan=3, sticky='nws')
        self.scroll_search_canvas.configure(yscrollcommand=self.scroll_y_scrollbar.set)

        self.scroll_search_canvas.bind('<Configure>', lambda e: self.scroll_search_canvas.configure(
            scrollregion=self.scroll_search_canvas.bbox('all')))

        self.scroll_search_frame = tk.Frame(self.scroll_search_canvas)
        self.scroll_search_frame.grid(row=0, column=1)

        self.scroll_search_canvas.create_window((0, 0), window=self.scroll_search_frame, anchor="nw")
        for i in range(len(self.button_list)):
            result_button = tk.Button(self.scroll_search_frame,
                                      text=(str(self.button_list[i][self.order[0]]) + " " + str(
                                          self.button_list[i][self.order[1]])) + " " + str(
                                          self.button_list[i][self.order[2]]), width=20,
                                      command=lambda i=i: main.button_decision(self.scroll_type,
                                                                               self.button_list[i][0])).grid(row=i,
                                                                                                             column=0,
                                                                                                             sticky="nw")

    def update_scroll(self, word_lst, format_type, width, case_type, associated_value):
        self.scroll_search_canvas.yview_moveto(0)
        self.clear_widgets()
        format_list = []
        cancel_list = []
        quantity_list = []

        for i in range(len(word_lst)):
            format_list.append(word_lst[i][0])
            format_list[i] = tk.Button(self.scroll_search_frame, text=str(word_lst[i][0]),
                                       width=width, command=lambda i=i: main.button_decision(case_type, word_lst[i][0]))
            format_list[i].grid(row=i, column=1, sticky="nw")
            if format_type == "Instructions":
                tk.Button(self.scroll_search_frame, text=(str(i + 1) + ".")).grid(row=i, column=0)
                cancel_list.append(i)
                cancel_list[i] = tk.Button(self.scroll_search_frame, text="X",
                                           command=lambda i=i: main.delete(i, [str(word_lst[i][0])], associated_value,
                                                                           format_type, self))
                cancel_list[i].grid(row=i, column=2)

            if format_type == "Ingredient_link" or format_type == "Recipe_link" or format_type == "Instruction_link" or format_type == "shopping_list":
                cancel_list.append(i)
                cancel_list[i] = tk.Button(self.scroll_search_frame, text="X",
                                           command=lambda i=i: main.delete(i, [str(word_lst[i][0])], associated_value,
                                                                           format_type, self))
                cancel_list[i].grid(row=i, column=2)

            if format_type == "Ingredients" or format_type == "Shopping_list":
                cancel_list.append(i)
                quantity_list.append(word_lst[i][1])
                cancel_list[i] = tk.Button(self.scroll_search_frame, text="X",
                                           command=lambda i=i: main.delete(i, [str(word_lst[i][0])], cancel_list, format_type,
                                                                           self))
                cancel_list[i].grid(row=i, column=3)
                quantity_list[i] = tk.Button(self.scroll_search_frame, text=word_lst[i][1], width=2)
                quantity_list[i].grid(row=i, column=2)


        self.scroll_search_frame.bind('<Configure>', self.reset_scroll_region)

    def reset_scroll_region(self, event):  # Event parameter is required but i do not need to call it
        self.scroll_search_canvas.configure(scrollregion=self.scroll_search_canvas.bbox("all"))

    def clear_widgets(self):
        for widget in self.scroll_search_frame.winfo_children():
            widget.destroy()


root = tk.Tk()
main = TkinterShell(root)
root.mainloop()
