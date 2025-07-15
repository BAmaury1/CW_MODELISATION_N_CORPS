from tkinter import *
from ANIM_2D import Anim_2D
from ANIM_3D import Anim_3D
import numpy as np
import matplotlib.pyplot as plt
from systeme_solaire import Anim_2D_solaire
from comete_syst import Anim_2D_comete
import webbrowser as wb


##################################################################################################################################
######################### Conditions initiales système solaire ###################################################################
##################################################################################################################################


tf_sol = 10
nb_valeurs_sol = 100000

m_sol = np.array([1.9891e30, 3.302e23, 4.8685e24, 5.9736e24,
                  6.4185e23, 1.8986e27, 5.6846e26, 8.6810e25, 1.0243e26])
N_sol = len(m_sol)
pos0_sol = np.array([0, 0, 3.52236e10, -4.5987e10, 0, 1.08208930e11, -1.495978875e11, 0, 0, -2.27936637e11,
                     7.78412027e11, 0, 0, 1.421179772e12, -2.876679082e12, 0, 0, -4.503443661e12])
pos0_sol = pos0_sol*(1/149597870700)
# changment d'unité
vit0_sol = np.array([0, 0, 3.08175e4, 2.686828e4, -3.502e4, 0, 0, -29291, 24077,
                     0, 0, 13057.2, -9644.6, 0, 0, -6.81e3, 5431.7, 0])
vit0_sol = vit0_sol*(365.25*24*3600)*(1/149597870700)  # changment d'unité
V0_sol = np.append(pos0_sol, vit0_sol)  # Vecteur à l'instant 0

pc = np.array([0.5, 0.5])
pos0_sol_comete = np.append(pos0_sol, pc)

theta = np.arctan(pc[0]/pc[1])
norme_vit = 10.43
vit_com = np.array([-np.cos(theta), np.sin(theta)])*norme_vit
vit0_sol_comete = np.append(vit0_sol, vit_com)

c = 1E14

# Avec la comète :
tf_sol_comete = 80
nb_valeurs_sol_comete = 1000000
# Vecteur à l'instant 0
V0_sol_comete = np.append(pos0_sol_comete, vit0_sol_comete)
m_sol_comete = np.append(m_sol, c)

root = Tk()
root.attributes('-fullscreen', True)

##################################################################################################################################
######################### Listes des variables ###################################################################################
##################################################################################################################################


nb_corps = IntVar(value=2)      # Variable donnant le nombre de corps souhaité
Is_2D_or_3D = IntVar(value=2)   # Variable valant 2 pour la 2D et 3 pour la 3D
# Variable valant 1 si on veut qu'une comète traverse le système solaire, 0 sinon
Var_comete = IntVar(value=0)

# On initialise 4 listes de variables, une pour la masse de chacun des 20 potentiels
# astres considérés et 3 pour leur position initiale (Z_init_var est utilisée seulement pour la 3D)
Masses_var = [IntVar() for i in range(20)]
X_init_var = [IntVar() for i in range(20)]
Y_init_var = [IntVar() for i in range(20)]
Z_init_var = [IntVar() for i in range(20)]

nb = nb_corps.get()
# Peut être augmenté pour un meilleur rendu avec un bon ordinateur
nb_valeurs = 500
# Durée de l'animation (équivalent en année pour les astres)
tf = 10
# Variable qui définit la largeur de la fenêtre des positions (aléatoires) possibles
rint_pos = 5
rint_vit = 1                # Idem avec la vitesse initiale
# Masses des astres séléctionnées aléatoirement par défaut
m_random = np.random.uniform(1E27, 1E30, 20)

# 2D - La position et la vitesse initiales sont sélectionnées aléatoirement par défaut
pos0_random_2D = np.random.uniform(-rint_pos, rint_pos, 2*20)
vit0_random_2D = np.random.uniform(-rint_vit, rint_vit, 2*20)
V0_2D = np.array([])
# 3D - La position et la vitesse initiales sont sélectionnées aléatoirement par défaut
pos0_random_3D = np.random.uniform(-rint_pos, rint_pos, 3*20)
vit0_random_3D = np.random.uniform(-rint_vit, rint_vit, 3*20)
V0_3D = np.array([])

# La liste des masses des astres est aléatoire par défaut et contient nb éléments
Mass = m_random[:nb]

# La liste des positions initiales des astres en 2D est aléatoire par défaut et contient 2*nb éléments
pos0_2D = pos0_random_2D[:2*nb]
# La liste des vitesses initiales des astres en 2D est aléatoire par défaut et contient 2*nb éléments
vit0_2D = vit0_random_2D[:2*nb]

# La liste des positions initiales des astres en 3D est aléatoire par défaut et contient 3*nb éléments
pos0_3D = pos0_random_3D[:3*nb]
# La liste des vitesses initiales des astres en 3D est aléatoire par défaut et contient 3*nb éléments
vit0_3D = vit0_random_3D[:3*nb]

# Rand_pos est une liste de variables qui valent 1 ou 0 en fonction de si on veut que la position du corps i soit générée aléatoirement ou non (random par défaut)
Rand_pos = [IntVar(value=1) for i in range(20)]
Rand_mass = [IntVar(value=1) for i in range(20)]        # Idem avec sa masse
# Idem avec sa vitesse initiale
Rand_speed = [IntVar(value=1) for i in range(20)]


##################################################################################################################################
############################### Fonctions appelées par les boutons ###############################################################
##################################################################################################################################


def MAJ_nb_corps():
    """Fait apparaître les interfaces de choix de données pour chaque corps considéré"""
    plt.close('all')
    global Is_2D_or_3D
    Frame_left.config(bd=1)
    Frame_right.config(bd=1)
    nb = nb_corps.get()
    # La fenêtre est divisée en 2 (left et right) pour plus de lisibilité
    for widgets in Frame_left.winfo_children():
        # On supprime les widgets dans ces fenêtres pour pouvoir réduire le nombre de corps considérés
        widgets.destroy()
    for widgets in Frame_right.winfo_children():
        widgets.destroy()
    for i in range(nb):
        # Disjonction de cas selon la parité de i pour placer le widget à gauche ou à droite
        if Is_2D_or_3D.get() == 2:  # Disjonction de cas si on est en 2D ou en 3D
            if i % 2 == 0:
                # Une fenêtre est créée pour mettre plusieurs widgets pour chaque corps
                New_frame = Frame(Frame_left, height=40, relief='solid')
                Label(New_frame, text="Corps "+str(i+1)).pack(side=LEFT)
                Frame_checkbuttons = Frame(
                    New_frame, relief='solid')
                Checkbutton(Frame_checkbuttons, text='Position aléatoire',
                            variable=Rand_pos[i]).grid(row=0, column=0)     # Bouton cochable avec pour valeur Rand_pos[i-1] valant 1 par défaut (case précochée)
                Checkbutton(Frame_checkbuttons, text='Vitesse aléatoire  ',
                            variable=Rand_speed[i]).grid(row=1, column=0)   # Idem avec la vitesse initiale aléatoire ou nulle
                Checkbutton(Frame_checkbuttons, text='Masse aléatoire',
                            variable=Rand_mass[i]).grid(row=0, column=1)    # Idem avec la masse aléatoire ou non
                if i == 0:                              # Label seulement pour le premier de la colonne
                    Scale(New_frame, from_=1, to=1000, label='Masse (E27)', orient='h', variable=Masses_var[i]).pack(
                        side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='x',
                          orient='h', variable=X_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='y',
                          orient='h', variable=Y_init_var[i]).pack(side=LEFT)
                else:
                    Scale(New_frame, from_=1, to=1000, orient='h', variable=Masses_var[i]).pack(
                        side=LEFT)
                    Scale(New_frame, from_=-5, to=5,
                          orient='h', variable=X_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5,
                          orient='h', variable=Y_init_var[i]).pack(side=LEFT)
                Frame_checkbuttons.pack(side=LEFT)
                New_frame.grid(row=i//2, column=0)
            else:               # Idem fenêtre de droite
                New_frame = Frame(Frame_right, height=40, relief='solid')

                Label(New_frame, text="Corps "+str(i+1)).pack(side=LEFT)
                Frame_checkbuttons = Frame(
                    New_frame, relief='solid')
                Checkbutton(Frame_checkbuttons, text='Position aléatoire',
                            variable=Rand_pos[i]).grid(row=0, column=0)
                Checkbutton(Frame_checkbuttons, text='Vitesse aléatoire  ',
                            variable=Rand_speed[i]).grid(row=1, column=0)
                Checkbutton(Frame_checkbuttons, text='Masse aléatoire',
                            variable=Rand_mass[i]).grid(row=0, column=1)
                if i == 1:                              # Label seulement pour le premier de la colonne
                    Scale(New_frame, from_=1, to=1000, label='Masse (E27)', orient='h', variable=Masses_var[i]).pack(
                        side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='x',
                          orient='h', variable=X_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='y',
                          orient='h', variable=Y_init_var[i]).pack(side=LEFT)
                else:
                    Scale(New_frame, from_=1, to=1000, orient='h', variable=Masses_var[i]).pack(
                        side=LEFT)
                    Scale(New_frame, from_=-5, to=5,
                          orient='h', variable=X_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5,
                          orient='h', variable=Y_init_var[i]).pack(side=LEFT)

                Frame_checkbuttons.pack(side=LEFT)
                New_frame.grid(row=i//2, column=0)

        else:           # Idem en 3D
            if i % 2 == 0:
                New_frame = Frame(Frame_left, height=40,
                                  relief='solid')       # Idem 3D
                Label(New_frame, text="Corps "+str(i+1)).pack(side=LEFT)
                Frame_checkbuttons = Frame(
                    New_frame, relief='solid')
                Checkbutton(Frame_checkbuttons, text='Position aléatoire',
                            variable=Rand_pos[i]).grid(row=0, column=0)
                Checkbutton(Frame_checkbuttons, text='Vitesse aléatoire  ',
                            variable=Rand_speed[i]).grid(row=1, column=0)
                Checkbutton(Frame_checkbuttons, text='Masse aléatoire',
                            variable=Rand_mass[i]).grid(row=0, column=1)
                if i == 0:
                    Scale(New_frame, from_=1, to=1000, length=75, label='Masse (E27)', orient='h', variable=Masses_var[i]).pack(
                        side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='x', length=75,
                          orient='h', variable=X_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='y', length=75,
                          orient='h', variable=Y_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='z', length=75,
                          orient='h', variable=Z_init_var[i]).pack(side=LEFT)
                else:
                    Scale(New_frame, from_=1, to=1000, length=75, orient='h', variable=Masses_var[i]).pack(
                        side=LEFT)
                    Scale(New_frame, from_=-5, to=5, length=75,
                          orient='h', variable=X_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, length=75,
                          orient='h', variable=Y_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, length=75,
                          orient='h', variable=Z_init_var[i]).pack(side=LEFT)

                Frame_checkbuttons.pack(side=LEFT)
                New_frame.grid(row=i//2, column=0)
            else:
                New_frame = Frame(Frame_right, height=40, relief='solid')

                Label(New_frame, text="Corps "+str(i+1)).pack(side=LEFT)
                Frame_checkbuttons = Frame(
                    New_frame, relief='solid')
                Checkbutton(Frame_checkbuttons, text='Position aléatoire',
                            variable=Rand_pos[i]).grid(row=0, column=0)
                Checkbutton(Frame_checkbuttons, text='Vitesse aléatoire  ',
                            variable=Rand_speed[i]).grid(row=1, column=0)
                Checkbutton(Frame_checkbuttons, text='Masse aléatoire',
                            variable=Rand_mass[i]).grid(row=0, column=1)
                if i == 1:
                    Scale(New_frame, from_=1, to=1000, length=75, label='Masse (E27)', orient='h', variable=Masses_var[i]).pack(
                        side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='x', length=75,
                          orient='h', variable=X_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='y', length=75,
                          orient='h', variable=Y_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, label='z', length=75,
                          orient='h', variable=Z_init_var[i]).pack(side=LEFT)
                else:
                    Scale(New_frame, from_=1, to=1000, orient='h', length=75, variable=Masses_var[i]).pack(
                        side=LEFT)
                    Scale(New_frame, from_=-5, to=5, length=75,
                          orient='h', variable=X_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, length=75,
                          orient='h', variable=Y_init_var[i]).pack(side=LEFT)
                    Scale(New_frame, from_=-5, to=5, length=75,
                          orient='h', variable=Z_init_var[i]).pack(side=LEFT)

                Frame_checkbuttons.pack(side=LEFT)
                New_frame.grid(row=i//2, column=0)


def Anim(V0_2, V0_3, rint_pos, tf, nb_valeurs, nb, Mass):
    """(int np.array, int np.array, int, int, int, int, float np.array) -> Matplotlib object    /   Lance l'animation 2D ou 3D selon le choix de l'utilisateur"""
    global Is_2D_or_3D, V0_2D, V0_3D
    if Is_2D_or_3D.get() == 2:
        Anim_2D(V0_2, rint_pos, tf, nb_valeurs, nb, Mass)
    else:
        Anim_3D(V0_3, rint_pos, tf, nb_valeurs, nb, Mass)


def Anim_systeme_solaire(V0_sol, V0_sol_comete, tf_sol, tf_sol_comete, nb_valeurs_sol, nb_valeurs_sol_comete, N_sol, m_sol, m_sol_comete):
    """(int np.array, int np.array, int, int, int, int, float np.array) -> Matplotlib object    /   Lance l'animation 2D ou 3D selon le choix de l'utilisateur"""
    global Var_comete
    if Var_comete.get() == 0:
        Anim_2D_solaire(V0_sol, tf_sol, nb_valeurs_sol, N_sol, m_sol)
    else:
        Anim_2D_comete(V0_sol_comete, tf_sol_comete,
                       nb_valeurs_sol_comete, N_sol + 1, m_sol_comete)


def MAJ_info_corps():
    """Met à jour les conditions initiales renseignées par l'utilisateur via les curseurs et boutons"""
    global nb, V0_2D, V0_3D, rint_pos, Mass, Is_2D_or_3D
    # Initialisé à 0 si toutes les positions initiales sont rentrées et non aléatoires
    rint_pos = 0
    nb = nb_corps.get()
    Mass = m_random[:nb]
    if Is_2D_or_3D.get() == 2:      # Condition 2D
        pos0_2D = pos0_random_2D[:2*nb]     # Valeurs aléatoires par défaut
        vit0_2D = vit0_random_2D[:2*nb]
        for i in range(nb):
            # Si la case "Position aléatoire" est décochée, on remplace les valeurs aléatoires par les valeurs des curseurs
            if Rand_pos[i].get() != 1:
                pos0_2D[2*i] = X_init_var[i].get()
                pos0_2D[2*i + 1] = Y_init_var[i].get()
            else:
                # Sinon, on reste en aléatoire avec un fenêtre de positionnement de 10x10
                rint_pos = 5
            if Rand_mass[i].get() != 1:     # Idem avec la masse
                Mass[i] = Masses_var[i].get()*10**27
            if Rand_speed[i].get() != 1:    # Idem avec la vitesse
                vit0_2D[2*i] = 0
                vit0_2D[2*i + 1] = 0
        V0_2D = np.append(pos0_2D, vit0_2D)
    else:
        pos0_3D = pos0_random_3D[:3*nb]     # Idem en 3D
        vit0_3D = vit0_random_3D[:3*nb]
        for i in range(nb):
            if Rand_pos[i].get() != 1:
                pos0_3D[3*i] = X_init_var[i].get()
                pos0_3D[3*i + 1] = Y_init_var[i].get()
                pos0_3D[3*i + 2] = Z_init_var[i].get()
            else:
                rint_pos = 5
            if Rand_mass[i].get() != 1:
                Mass[i] = Masses_var[i].get()*10**27
            if Rand_speed[i].get() != 1:
                vit0_3D[3*i] = 0
                vit0_3D[3*i + 1] = 0
                vit0_3D[3*i + 2] = 0
        V0_3D = np.append(pos0_3D, vit0_3D)


##################################################################################################################################
#################################### Visuel de l'interface #######################################################################
##################################################################################################################################


# Fenêtre Haut
Frame_top = Frame(root, relief='solid', height=50, bg='#FFE4B5')
Label(Frame_top, text='            Problème à N+1 corps            ',
      font=("Courier", 36), bg='#FFE4B5').pack(side=LEFT)

# Fenêtre Nombre de corps (Bandeau du haut)
Frame_nb_corps = Frame(root, bd=1, relief='solid', bg='#FFE4B5')
Frame_nb_corps_left = Frame(Frame_nb_corps, bd=1, relief='solid', bg='#FFE4B5')
Frame_nb_corps_right = Frame(
    Frame_nb_corps, bd=1, relief='solid', bg='#FFE4B5')

Frame_vide_left = Frame(Frame_nb_corps_left, height=80, width=50, bg='#FFE4B5')
Frame_vide_left.pack(side=LEFT)         # Fenêtre vide pour espacer les widgets

Frame_Bouton_2D_to_3D = Frame(
    Frame_nb_corps_left, height=80, width=100, bg='#FFE4B5')    # Fenêtre contenant les boutons 2D et 3D
Bouton_2D = Radiobutton(Frame_Bouton_2D_to_3D, text='2D',
                        variable=Is_2D_or_3D, value=2, bg='#FFE4B5').pack()
Bouton_3D = Radiobutton(Frame_Bouton_2D_to_3D, text='3D',
                        variable=Is_2D_or_3D, value=3, bg='#FFE4B5').pack()
Frame_Bouton_2D_to_3D.pack(side=LEFT)

Frame_vide_top_1 = Frame(
    Frame_nb_corps_left, height=80, width=100, bg='#FFE4B5').pack(side=LEFT)

Scale_nb_corps = Scale(Frame_nb_corps_left, from_=2, to=20, orient='h', label='Nombre de corps', variable=nb_corps,
                       bd=1, relief='solid', length=110)    # Selection du nombre de corps pour l'animation (variable nb_corps)
Scale_nb_corps.pack(side=LEFT)

Frame_vide_top_2 = Frame(
    Frame_nb_corps_left, height=80, width=100, bg='#FFE4B5').pack(side=LEFT)

Bouton_nb_corps = Button(
    Frame_nb_corps_left, text='Enregistrer', height=3, relief='raised', bd=3, command=MAJ_nb_corps, width=14)       # Bouton qui met à jour l'affichage selon le nombre de corps considérés
# Bouton qui enregistre la sélection et affiche l'interface plus détaillée
Bouton_nb_corps.pack(side=LEFT)

Frame_vide_top_3 = Frame(
    Frame_nb_corps_left, height=80, width=100, bg='#FFE4B5').pack(side=LEFT)


Bouton_simulation = Button(
    Frame_nb_corps_left, text="Lancer simulation", width=15, height=2, bd=5, font=(10), relief='raised', command=lambda: [MAJ_nb_corps(), MAJ_info_corps(), Anim(V0_2D, V0_3D, rint_pos, tf, nb_valeurs, nb, Mass)]).pack(side=LEFT)
# Bouton qui permet de lancer l'animation

Frame_vide_top_4 = Frame(
    Frame_nb_corps_left, height=80, width=50, bg='#FFE4B5').pack(side=LEFT)

Frame_nb_corps_left.pack(side=LEFT)

Frame_comete = Frame(Frame_nb_corps_right, height=80, width=100, bg='#FFE4B5')
Radiobutton(Frame_comete, text='Comète        ', value=1,
            variable=Var_comete, bg='#FFE4B5').pack()
Radiobutton(Frame_comete, text='Sans comète', value=0,
            variable=Var_comete, bg='#FFE4B5').pack()
Frame_comete.pack(side=LEFT)

Bouton_systeme_solaire = Button(
    Frame_nb_corps_right, text='Système solaire 2D', height=3, relief='raised', bd=3, command=lambda: Anim_systeme_solaire(V0_sol, V0_sol_comete, tf_sol, tf_sol_comete, nb_valeurs_sol, nb_valeurs_sol_comete, N_sol, m_sol, m_sol_comete)).pack(side=LEFT)
# Bouton qui lance l'animation en 2D avec les conditions initiales du système solaire

Frame_vide_top_5 = Frame(
    Frame_nb_corps_right, height=80, width=50, bg='#FFE4B5').pack(side=LEFT)

Bouton_quit = Button(Frame_nb_corps_right, text='Quitter', bd=5,
                     relief='raised', command=quit, font=(10), width=10).pack(side=LEFT)       # Bouton qui permet de quitter l'interface

Frame_vide_right = Frame(Frame_nb_corps_right,
                         height=80, width=100, bg='#FFE4B5')
Frame_vide_right.pack(side=LEFT)
Frame_nb_corps_right.pack(side=LEFT)

Frame_top.grid(row=0, column=0)
Frame_nb_corps.grid(row=1, column=0)

# Fenêtre Corps où les conditions initiales pour chaque corps considérés pourront être renseignées
Frame_corps = Frame(root)
Frame_quit = Frame(root)

# Les corps considérés de numéro pair s'affichent dans cette fenêtre
Frame_left = Frame(Frame_corps, height=450, width=510, bd=0, relief='solid')

# Les corps considérés de numéro impair s'affichent dans cette fenêtre
Frame_right = Frame(Frame_corps, height=450, width=510, bd=0, relief='solid')

# 2 fenêtres qui permettent d'espacer les widgets
Frame_corps_1 = Frame(Frame_left, height=50, width=510, relief='solid')
Frame_corps_2 = Frame(Frame_right, height=50, width=510, relief='solid')

# Positionnement des widgets
Frame_corps_1.grid(row=0, column=0)
Frame_corps_2.grid(row=1, column=0)
Frame_left.pack(side=LEFT)
Frame_right.pack(side=LEFT)
Frame_corps.grid(row=2, column=0)

# Consignes en haut de la page
menubar = Menu(root)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Fonctionnement du programme :")
menu1.add_command(label="(1) Choisir entre 2D et 3D")
menu1.add_command(label="(2) Choisir le nombre de corps")
menu1.add_command(label="(3) Appuyer sur 'Enregistrer'")
menu1.add_command(
    label="(4) Renseigner les conditions initiales ou utiliser les conditions aléatoires par défaut")
menu1.add_command(label="(5) Presser 'Lancer la simulation'")
menu1.add_command(
    label="(6) Si vous refermez la simulation, pressez 'Enregistrer' avant de relancer la simulation")
menu1.add_command(
    label="(7) Appuyer sur 'Système solaire 2D' pour utiliser les conditions initiales du système solaire")
menubar.add_cascade(label="Fonctionnement du programme", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Participants", menu=menu2)
menu2.add_command(label="Titouan Brunel", command=lambda: wb.open(
    'https://www.linkedin.com/in/titouan-brunel-0653b6261/'))
menu2.add_command(label="Périg Gatel", command=lambda: wb.open(
    'https://www.linkedin.com/in/p%C3%A9rig-gatel-363915297/'))
menu2.add_command(label="Paul Bineau", command=lambda: wb.open(
    'https://www.linkedin.com/in/paul-bineau-11a654250/'))
menu2.add_command(label="Amaury Burtin", command=lambda: wb.open(
    'https://www.linkedin.com/in/amaury-burtin-a07b7a217/'))
menu2.add_command(label="Baptiste Soriano", command=lambda: wb.open(
    'https://www.linkedin.com/in/baptiste-soriano-860308290/'))
menu2.add_command(label="Imanol Lacroix", command=lambda: wb.open(
    'https://www.linkedin.com/in/imanol-lacroix-57a404293/'))
root.config(menu=menubar)

root.mainloop()
