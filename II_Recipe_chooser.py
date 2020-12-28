# %%
from numpy.core.fromnumeric import sort
from I_Prétraitement import clean_ingredient_list, csv_test, csv
import pandas as pd
#csv = csv_test
#créons une de recette avec leur ingredient (on garde le même id de liste par recette) 
#recipes_igrd_list = pd.read_csv("cleaner_recipes.csv", sep=';', usecols=["Ingredients"])["Ingredients"].to_list()
recipes_igrd_list = csv["Ingredients"].to_list()
#.apply(lambda x: x.split(',')).to_list()
#%%
def createRecipesPerIngredient(clean_igrd_list):
    """
    :but:   Retourne un dictionnaire de chaque igredient associer avec un set de chaque recette qui le comporte
            On vas associer chaque ingredient à une liste de recette qui le comporte
    :type: Dict -> Set

    :exemple:
    {'flour', 'egg'} -> {'flour': {1,2,3,4}, 'egg':{2,5}}
    """
    d = dict()
    for igrd in clean_igrd_list:
        s = set()
        for i in range(len(recipes_igrd_list)):
            igrd_list = recipes_igrd_list[i]
            if igrd in igrd_list:
                s.add(i)
        d[igrd] = s
    return d

def getRecipe(id):
    """
    Recipe from id
    :type: Int -> Pandas Series
    
    :exemple:
    >>> type(getRecipe(0))
    <class 'pandas.core.series.Series'>
    """
    return csv.loc[id]

# %%
# Attribuons un score à chaque recette pour savoir laquelle est 
# la plus proche de nos ingredients
def recipeIntersection(igrd_list, igrd_dict):
    """
    :but: Return un dict de recette_id associé à un score : {1:0.5, 2:0.34}
    :type: List, Dict -> Dict
    :method: renvoie donc une recette utlisant TOUT vos ingredients  => Intersection 

    :exemple:
    (['origano', 'flour'], {'origano': {1,2,3,4}, ..., 'flour':{2,5}}) -> {2:0.34}
    """
    s, d = set(), dict()
    for igrd in igrd_list:
        s = s.intersection(igrd_dict[igrd])
    for i in s:
        d[i] = score(i, igrd_list)
    return d

def recipesScore(igrd_list, igrd_dict):
    """
    :but: Return un dict de recette_id associé à un score : {1:0.5, 2:0.34}
    :type: List, Dict -> Dict
    :method: union automatique puis score ratio

    :exemple:
    (['origano', 'flour'], {'origano': {1,2,3,4}, ..., 'flour':{2,5}}) -> {1:0.5, 2:0.34}
    """
    s, d = set(), dict()
    for igrd in igrd_list:
        s = s.union(igrd_dict[igrd])
    for i in s:
        d[i] = score(i, igrd_list)
    return d
    
def recipesScore2(igrd_list, igrd_dict):
    """
    :but: Return un dict de recette_id associé à un score : {1:0.5, 2:0.34}
    :type: List, Dict -> Dict
    :method: union automatique puis score comptage simple 

    :exemple:
    (['origano', 'flour'], {'origano': {1,2,3,4}, ..., 'flour':{2,5}}) -> {1:0.5, 2:0.34}
    """
    s, d = set(), dict()
    for igrd in igrd_list:
        s = s.union(igrd_dict[igrd])
    for i in s:
        d[i] = score2(i, igrd_list)
    return d

def maxRecipeScore(recipe_score_dict):
    """
    :but:   Return le recipe_ID avec le score le plus haut du dictionnaire
    :type: Dict -> Int

    :exemple:
    >>> maxRecipeScore({1:0.5, 2:0.34})
    1
    """
    score_id = 0
    tmp = 0
    for i in recipe_score_dict.keys():
        score = recipe_score_dict[i]
        if score > tmp:
            score_id = i
            tmp = score
    return score_id        

def sortByScore(recipe_score_dict):
    """
    :but: Tri décroissant un dictionnaire en fonction des values
    :type: Dict -> Dict
    :method: python sorted fct

    :exemple:
    >>> sortByScore({1:0.5, 2:0.7})
    {2:0.7, 1:0.5}
    """
    return {key: val for key, val in sorted(recipe_score_dict.items(), key = lambda ele: ele[1], reverse = True)}

def sortByScore2(recipe_score_dict):
    """
    :but: Tri décroissant un dictionnaire en fonction des values
    :type: Dict -> Dict
    :method: Autre

    :exemple:
    >>> sortByScore({1:0.5, 2:0.7})
    {2:0.7, 1:0.5}
    """
    pass

def score(recipe_id, igrd_list):
    """
    :but:   Determine un score par recette pour obtenir la plus proche de notre liste d'ingredient
            Score   = nb d'ingredient disponible pour cette recette/nb total d'ingredient
                    = un ratio
    + evite les duplicates dans les ingredients (ce qui arrive souvent)
    :type: Int, List -> Int

    :exemple:
    avec une recette ['yeast', 'water', 'white sugar', 'salt', 'egg', 'butter', 
    'flour', 'butter']
    =====>  2/7
    >>> score(3, ['flour', 'butter', 'banana'])
    0.2857142857142857
    """
    duplicate = list()
    score = 0
    n = 0
    igrd = recipes_igrd_list[recipe_id]
    for i in igrd_list:
        if i in duplicate:
            continue
        elif i in igrd:
            duplicate.append(i)
            n += 1
            score += 1
    return score/n
    
def score2(recipe_id, igrd_list):
    """
    :but: score = nb d'inggredient dispo dans la recette
    :type: Int, List -> Int

    :exemple: 
    ['pastry', 'butter', 'flour', 'water', 
    'white sugar', 'brown sugar', 'apple']
    =======> 2
    >>> score2(3, ['flour', 'butter', 'banana'])
    2
    """
    score = 0
    igrd = recipes_igrd_list[recipe_id]
    for i in igrd_list:
        if i in igrd:
            score += 1
    return score

def frqIgrd():
    """
    :but: Renvoie un dictionnaire des ingrédient en keys avec leurs nombre d'ocurence en value 
    :type: Dict -> Dict

    :exemple: 
    {'flour': {1,2,3,4}, 'egg':{2,5}} -> {'flour': 4, 'egg': 2}
    """
    igrd_dict = createRecipesPerIngredient(clean_ingredient_list)
    d = dict()
    for key in igrd_dict.keys():
        d[key] = len(igrd_dict[key])
    return d

def recipe_chooser(igrd_list, method):
    """
    :but: prend en entrée une liste d'ingredients et renvoie une liste de recettes les plus proches de ces ingredients en fonction du score et de la méthode souhaité
    :type: List, Int -> pandas.DataFrame 
    :method: Score, Score2, Intersection
    
    :exemple:
    Littéralement un test dans l'interface du programe 
    """
    igrd_dict = createRecipesPerIngredient(clean_ingredient_list)
    if method == 0:
        print('Finding recipes with method 1')
        hey = recipesScore(igrd_list, igrd_dict)
    elif method == 1:
        print('Finding recipes with method 2')
        hey = recipesScore2(igrd_list, igrd_dict)
    else:
        print('Finding recipes with method 3')
        hey = recipeIntersection(igrd_list, igrd_dict)
    sorted_r = pd.DataFrame([getRecipe(i) for i in sortByScore(hey).keys()], columns=csv.columns)[:10]
    #print(sortByScore(hey))
    sorted_r['Recipe Photo'] = sorted_r['Recipe Photo'].apply(lambda x: '<img src="{}">'.format(x))
    print('Recipes Found')
    return sorted_r

# %%
import doctest
doctest.testmod()
