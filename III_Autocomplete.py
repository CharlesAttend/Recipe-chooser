# %%
from I_Prétraitement import clean_ingredient_list
from II_Recipe_chooser import frqIgrd, sortByScore


class Node():
    """
    Classe qui représente un noeud de la Trie
    """
    def __init__(self, lettre, word=False, frq=None):
        self.lettre = lettre
        self.children = dict()
        self.word = word
        self.frq = frq

    def appendChild(self, childNode):
        self.children[childNode.lettre] = childNode
        return childNode
    
def getWord(node:Node, l):
    """
    :but:   Fonction récursive qui explore toutes les sous node de celle en paramètre et qui renvoie une liste de mot trouvé.
            Obtenir une liste des sous mots possible de la node.
    :type: Node, List -> List

    :exemple:
    liste des mots : ['abc', 'acb', 'acc']
    getWord(Node du mot ac) -> ['acb', 'acc']
    """
    if node.word:
        l.append(node.word)
    else:
        for child in node.children:
            getWord(node.children[child], l)
    return l


def rechercheNode(trie, mot):
    """
    :but:   Return la node représentant la dernière lettre du mot en paramètre
            Si elle n'existe pas return False
    :method: A des fin d'optimisation, si le mot n'est pas trouvé, retourne la node précédentea ce mot 
    :type: Node, String -> Node

    :exemple:
    liste des mots : ['abc', 'acb', 'acc']
    rechercheNode(masterNode, 'ac') -> Node du mot ac
    """
    actualNode = trie
    for lettre in mot:
        try:
            actualNode = actualNode.children[lettre]
        except KeyError:
            return actualNode, False
    return actualNode, True

def printTrie(trie, lvl=0):
    """
    :but: Afficher une trie avec indentation
    :type: Node, Int -> None

    :exemple: 
    >>> printTrie(buildTrie(['abc', 'acb', 'acc'], {'abc':1, 'acb':1, 'acc':1}))
    a
    _b
    __c
    ___
    _c
    __b
    ___
    __c
    ___
    """
    for child in trie.children.values():
        print("_"*lvl + child.lettre)
        printTrie(child, lvl+1)

def buildTrie(liste_mot, frq):
    """
    :but: Créer une trie node par node à partir d'une liste ordonée alphabétiquement
    :type: Liste, Dict -> Node

    :exemple:
    >>> printTrie(buildTrie(['abc', 'acb', 'acc'], {'abc':1, 'acb':1, 'acc':1}))
    a
    _b
    __c
    ___
    _c
    __b
    ___
    __c
    ___
    """
    masterNode = Node("")
    for mot in liste_mot:
        for i in range(len(mot)):
            lettre = mot[i]
            node, found = rechercheNode(masterNode, mot[:i+1])
            if found:
                last_child = node
            else:
                last_child = node.appendChild(Node(lettre))
        last_child.appendChild(Node('', mot, frq[mot]))
    return masterNode  
      
def buildTrie2(liste_mot, frq):
    """
    Buil Trie mais avec une complexité O(mn)
    
    >>> printTrie(buildTrie(['abc', 'acb', 'acc'], {'abc':1, 'acb':1, 'acc':1}))
    a
    _b
    __c
    ___
    _c
    __b
    ___
    __c
    ___
    """
    last_child = Node("")
    masterNode = last_child
    for mot in liste_mot:
        last_child = masterNode
        for i in mot:
            if i not in last_child.children:
                last_child = last_child.appendChild(Node(i))
            else:
                last_child = last_child.children[i]
        last_child.appendChild(Node('', mot, frq[mot]))
    return masterNode 

def recherche(mot):
    """
    :but: recherche purement et simplement le mot dans la trie et renvoie la liste des sous mot à celui-ci, trié en fonction du nombre d'occurence dans les recettes 
    :type: String -> List or Bool

    :exemple:
    Liste des mots : ['abc', 'acb', 'acc']
        recherche('ac') -> ['acb', 'acc']
        recherche('ax') -> False
    """
    d = dict()
    node, found = rechercheNode(trie, mot)
    if found:
        l = getWord(node, [])
        for i in l:
            d[i] = frq[i]
        return list(sortByScore(d))
    else:
        return False
# %%
frq = frqIgrd()
clean_ingredient_list = sorted(clean_ingredient_list)
trie = buildTrie(clean_ingredient_list, frq)
len(getWord(trie, []))

#%% 
import doctest
doctest.testmod()