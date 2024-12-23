# Exercice 9 - Le plus court trajet possible
# Objectif - Créer un algorithme qui est capable de déterminer le chemin le plus court entre 5 points.

#Importations des librairies nécessaires (voir requirements.txt pour trouver les modules à télécharger)
import itertools
from screen import afficher_animation
import tkinter as tk

#------------------Récupération de données---------------------------
def individual_data(nb_pts):
    """Cette fonction récupère les cordonnées des points que l'on cherche"""
    data = [[0., 0., 0.]] #Mise en place du point 0, 0, 0
    for i in range(nb_pts):
        while True: #Tentative de récupérer les bonnes valeurs, sauf si c'est une valeur invalide
            try:
                print("-" * 50)
                print(f"Entrez les valeurs (x, y et z) du point {i + 1}")
                x = float(input("X -> ").replace(",", ".")) #Change les virgules en points pour permettre
                y = float(input("Y -> ").replace(",", ".")) #son utilisation pour les décimales
                z = float(input("Z -> ").replace(",", "."))
                data.append([x, y, z])
                break
            except ValueError: #Si c'est une mauvaise valeur, la boucle recommence au point qu'il était rendu
                print("Valeur incorrecte, veuillez réessayer.")
    return data

#---------------------------Calcul de distances et permutations----------------------------------
def distance(data, un, deux):
    """Cette fonction calcule la distance entre 2 points spécifiques"""
    x1, y1, z1 = data[un][0], data[un][1], data[un][2]
    x2, y2, z2 = data[deux][0], data[deux][1], data[deux][2]
    temp = [(x2 - x1), (y2 - y1), (z2 - z1)]
    return ((temp[0] ** 2) + (temp[1] ** 2) + (temp[2] ** 2)) ** (1/2)

def permutations_centre(nb_pts):
    """Cette fonction calcule le nombre de permutations (excluant le 0) à faire entre des points"""
    list_nb_pts = [_ for _ in range(1, nb_pts + 1)]
    return list(itertools.permutations(list_nb_pts, nb_pts)) #Utilise itertools pour créer toutes les permutations
                                                             #possibles avec

def sommes_distances_centre(permutation, data):
    """Cette fonction calcule, selon les coordonnées données, la distance totale de chaque permutation"""
    list_dist = []
    dist_temp = 0.
    for i in range(len(permutation)):
        for j in range(len(permutation[i])):
            if j == 0: #Cas limite avec le point 0, absent des permutations
                dist_temp += distance(data, 0, permutation[i][j])
                continue
            dist_temp += distance(data, permutation[i][j-1], permutation[i][j])
        list_dist.append(dist_temp)
        dist_temp = 0.
    return list_dist

#---------------------------Analyse et ordre--------------------------------------------------
def min_order(total_distances):
    """Cette fonction trouve la ou les distances les plus courtes, puis donne l'index de la permutation qui est lié"""
    min = None
    min_list = []
    for arg in total_distances: #Calcul de la valeur la plus courte
        if min is None or arg <= min:
            min = arg
    for a in range(len(total_distances)): #Trouve tous les index qui correspondent à la valeur la plus courte
        if min == total_distances[a]:
            min_list.append(a)
    return min, min_list

#--------------------------Programme principal-------------------------------------------
if __name__ == "__main__":
    #Attribution des variables à l'aide des fonctions ci-dessus
    nombre_points = None
    while nombre_points is None or nombre_points <= 0:
        try:
            nombre_points = int(input("Combien de points voulez-vous calculer (en plus du point 0) : "))
            break
        except ValueError:
            print("Erreur - Veuillez utiliser un nombre entier positif pour représenter le nombre de points")
            print("-" * 50)
    coords = individual_data(nombre_points)
    perm = permutations_centre(nombre_points)
    dist_total = sommes_distances_centre(permutations_centre(nombre_points), coords)
    minimum, id_perm = min_order(dist_total)

    #Affichage des résultats demandés
    print("-" * 50)
    print(f"La distance la plus courte est : {minimum} unités")
    print("Voici le(s) chemin(s) qui correspond(ent) à cela :")
    for elem in id_perm:
        print(f"P0 -> {" -> ".join([f"P{p}" for p in perm[elem]])}")

    #GUI pour afficher le graphique
    root = tk.Tk()
    root.title("SpaceMap Go v.0.1.0")
    root.geometry("600x600")
    afficher_animation(root, coords, [perm[elem] for elem in id_perm])
    root.mainloop()