# %%
import pandas as pd
csv = pd.read_csv("clean_recipes.csv", sep=';').drop(["RecipeID", "Author"], axis=1)
csv
#%%
def kToInt(x):
    """
    :but: transformer les 1k commentaire en 1000 commentaire
    :type: String -> Int

    :exemple:
    >>> kToInt('9k')
    9000
    """
    if x[-1:] == "k":
        return int(x[:-1])*1000
    else:
        return int(x)

csv["Review Count"] = csv["Review Count"].apply(kToInt)
# %%
def ingredientCleaner(ingredient):
    """
    :but: Determine si un ingredient composé de plusieurs mots indésirables. Si oui les élimines
    :type: String -> String

    :exemple:
    Transformer les : "3 tablespoons fajita seasoning" en "fajita seasoning"
    >>> ingredient_cleaner("3 tablespoons fajita seasoning")
    'fajita seasoning'
    """
    clean_ingredient = ""
    for j in ingredient.split(' '):
        j = j.lower()
        if j in ["powder", "tablespoon", "pound", 'pounds', 'package', 
                'tablespoons', 'cups', 'small', 'large', 'cup', "chopped", 'ounce', 'fluid']:
            # return False
            continue
        elif j == '' or j[0] == "(" or j[0] == "'" or j[-1:] == ")":
            # return False
            continue
        else:
            try:
                int(j[0])
                continue
                # return False
            except:
                clean_ingredient = clean_ingredient + j + " "
    return clean_ingredient[:-1]

##############LIST D'INGREDIENT##############
# %%
def ingredientListOfList2set(ingredients):
    """
    :but:   Dans le csv les ingrédients sont stocké sous forme d'une String, pas pratique pour les parcourirs :/ 
            Ici on les transformes en un gros set comportant tout les ingrédients !
            (qui sera utile pour l'autocomplete)
    :type: List -> Set ; Iteralbe -> Set

    :exemple:
    ["igrd1, irgd2"], ['igrd1, irgd3']] -> {'igrd1','irgd2','irgd3'}
    >>> sorted(list(ingredientListOfList2set(csv['Ingredients'].loc[:1])))
    Taille d'origine de la liste des ingrédients: 15
    ['almond', 'baking powder', 'butter', 'egg', 'flour', 'milk', 'orange juice', 'poppy', 'salt', 'sugar', 'vanilla', 'vegetable oil', 'water', 'white sugar', 'yeast']
    """
    s = set()
    for recipe_ingredients in ingredients:
        l = recipe_ingredients.split(',')
        for i in l:
            i = i.lower()
            s.add(i)
    print("Taille d'origine de la liste des ingrédients:", len(s))
    return s

# %%
def getCleanIngredientList(ingredient_set):
    """
    :but: Prend chaque ingredient d'une liste ou set et le clean pour le mettre dans un nouveau set
    :type: Iterable -> Set

    :exemple:
    >>> getCleanIngredientList(['1/4 cup thousand island dressing', '1/4 fluid ounce blue curacao'])
    Taille de la nouvelle liste des ingrédients: 2
    {'island dressing', 'blue curacao'}
    """
    new_ingredient_set = set()
    for ingredient in ingredient_set:
        new_ingredient = ""
        bol = ingredientCleaner(ingredient)
        if bol:
            new_ingredient_set.add(bol)
    print("Taille de la nouvelle liste des ingrédients:", len(new_ingredient_set))
    return new_ingredient_set
 
##############CLEAN DU CsV##############
# %%
def getCleanCsvIngredientList(csv):
    """
    :but:   Return une liste des ingredients du csv clean
            + On en profite pour faire un nombre d'ocurence de l'ingredient
    :param: Iterable -> list of list

    :exemple:
    >>> getCleanCsvIngredientList(['yeast,water,white sugar,salt,egg,butter,flour,butter', 'flour,salt,baking powder,poppy,butter,vegetable oil,egg,milk,white sugar,vanilla,almond,orange juice,butter,almond,vanilla,sugar'])
    [['yeast', 'water', 'white sugar', 'salt', 'egg', 'butter', 'flour', 'butter'], ['flour', 'salt', 'baking', 'poppy', 'butter', 'vegetable oil', 'egg', 'milk', 'white sugar', 'vanilla', 'almond', 'orange juice', 'butter', 'almond', 'vanilla', 'sugar']]
    """
    lofl, d = list(), dict() #lofl = List Of List
    # d= {"3 tablespoons fajita seasoning": 'fajita seasoning'"
    #     "flour": 'flour'}
    for igrd_list in csv:
        l = []
        for igrd in igrd_list.split(','):
            try:
                l.append(d[igrd])
            except:
                clean_igrd = ingredientCleaner(igrd)
                d[igrd] = clean_igrd
                l.append(clean_igrd)
        lofl.append(l)
    return lofl
#%% 
import doctest
doctest.testmod()
# %%
#Exportation d'une liste d'ingredient netoyé 
clean_ingredient_list = getCleanIngredientList(ingredientListOfList2set(csv['Ingredients']))
pd.Series(list(clean_ingredient_list)).to_csv("clean_ingredient_list.csv", sep=";")
pd.Series(sorted(ingredientListOfList2set(csv['Ingredients']))).to_csv('ingredient_list.csv', sep=';')
# %%
#Exportation d'un csv netoyé
csv['Ingredients'] = getCleanCsvIngredientList(csv['Ingredients']) #Attention ça casse un test
csv.to_csv("cleaner_recipes.csv", sep=";", index_label=["id"])
# %%
#Creation du set test
csv_test = csv.sort_values(by="Review Count", ascending=False).head(5)
csv_test.reset_index(drop=True, inplace=True) #on reindex car c'est trié pas recettes les plus populaire
csv_test.reindex().to_csv("cleaner_recipes_test.csv", sep=";", index_label=["id"])
