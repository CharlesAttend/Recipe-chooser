import tkinter as tk
import tkinter.messagebox
import pandas as pd
import webbrowser

from III_Autocomplete import recherche
from II_Recipe_chooser import recipe_chooser

__all__ = ["Autocomplete"]

NO_RESULTS_MESSAGE = "No results found for '{}'"

class Autocomplete(tk.Frame, object):
    DEFAULT_LISTBOX_HEIGHT = 5
    DEFAULT_LISTBOX_WIDTH = 25
    DEFAULT_ENTRY_WIDTH = 25

    def __init__(self, *args, **kwargs):

        super(Autocomplete, self).__init__(*args, **kwargs)
        self.text = tk.StringVar()
        self.result = False
        self.entry_widget = tk.Entry(
            self,
            textvariable=self.text,
            width=self.DEFAULT_ENTRY_WIDTH
        )
        self.listbox_widget = tk.Listbox(
            self,
            height=self.DEFAULT_LISTBOX_HEIGHT,
            width=self.DEFAULT_LISTBOX_WIDTH
        )

    def build(self, no_results_message=NO_RESULTS_MESSAGE):
        """
        Set up quelque variable importante pour la Class
        """
        self._no_results_message = no_results_message

        self.entry_widget.bind("<KeyRelease>", self._update_autocomplete)
        self.entry_widget.focus_set()
        self.entry_widget.grid(column=0, row=0)

        self.listbox_widget.bind("<<ListboxSelect>>", self._select_entry)
        self.listbox_widget.grid(column=0, row=1)
        self.listbox_widget.grid_forget()



    def _update_autocomplete(self, event):
        """
        Fonction qui est appelé à chaque appuis de touche
        """
        self.listbox_widget.delete(0, tk.END)
        self.listbox_widget["height"] = self.DEFAULT_LISTBOX_HEIGHT

        #La comparaison se fait ici
        text = self.text.get().lower()
        if not text:
            self.listbox_widget.grid_forget()
        else:
            self.result = recherche(text)
            if self.result:
                for mot in self.result:
                    self.listbox_widget.insert(tk.END, mot)
    


        #Section qui gère la taille de la boite qui display les sugestions
        listbox_size = self.listbox_widget.size()
        if not listbox_size:
            if self._no_results_message is None:
                self.listbox_widget.grid_forget()
            else:
                try:
                    self.listbox_widget.insert(
                        tk.END,
                        self._no_results_message.format(text)
                    )
                except UnicodeEncodeError:
                    self.listbox_widget.insert(
                        tk.END,
                        self._no_results_message.format(
                            text.encode("utf-8")
                        )
                    )
                if listbox_size <= self.listbox_widget["height"]:

                    self.listbox_widget["height"] = listbox_size
                self.listbox_widget.grid()
        else:
            if listbox_size <= self.listbox_widget["height"]:
                self.listbox_widget["height"] = listbox_size
            self.listbox_widget.grid()

    def _select_entry(self, event):
        """
        fait la selection d'un mpt 
        """
        widget = event.widget
        value = widget.get(int(widget.curselection()[0]))
        self.text.set(value)

def addIgrd(event=None):
    found = autocomplete.result
    if found:
        text = autocomplete.text.get()
        if text in igrd_list:
            consigne.config(text='Ingredient already entered')
        else:
            igrd_list.append(text)
            print(text)
            list_igrd.insert(tk.END,text)
            autocomplete.text.set('')
    else:
        print("Ingredient not found")
        consigne.config(text= "Ingredient not found")

def printRecipe():
    recipe = recipe_chooser(igrd_list, rd.get())
    print('Creating HTML page for your recipe')
    recipe.to_html('recipe.html', escape=False)
    webbrowser.open('recipe.html')


root = tk.Tk()

autocomplete = Autocomplete(root)
autocomplete["width"] = 50
autocomplete.build(no_results_message="<No results for '{}'>")
autocomplete.pack()   
autocomplete.entry_widget.bind("<Return>", addIgrd)
autocomplete.listbox_widget.bind("<Return>", addIgrd)

tk.Button(text='Find Recipe!', command=printRecipe).pack()
tk.Button(text='Add Ingredient', command=addIgrd).pack()
rd = tk.IntVar()
rd.set(1)
tk.Radiobutton(root, text='Method 1 : Ratio', variable=rd, value=0).pack()
tk.Radiobutton(root, text="Method 2 : Comptage simple", variable=rd, value=1).pack()
tk.Radiobutton(root, text="Method 3 : Recette comportant tous les ingrédients", variable=rd, value=2).pack()

consigne = tk.Label(root, text='Entrer un ingredient')
consigne.pack()

list_igrd = tk.Listbox()
list_igrd.pack()

igrd_list = list()

root.mainloop()