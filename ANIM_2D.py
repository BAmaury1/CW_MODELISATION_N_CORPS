# importation des modules
# importation des modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.image as mpimg
from RESOL_2D import resolution
from DETECTION_COLLISION_2D import detection


def attribution_couleur(Mass_corps):
    """int list-> ((float array) np.array) 
    renvoie une liste attribuant les couleurs, plus la masse d'une planète est grande, plus sa couleur
    sera rouge, plus elle est faible, plus elle est bleue"""
    max = np.max(Mass_corps)
    Mass_normalise = Mass_corps/max
    Mass_colors = plt.cm.coolwarm(Mass_normalise)

    return (Mass_colors)


def Anim_2D(V0, rint_pos, time_max, Nb_values, Nb_corps, Mass_corps):
    """"int np.array,int,int,int,int,int list->matplotlib object
    affiche la simulation en 2D suivant les paramètres de la simulatoin choisis par l'utilisateurhelp"""

    # image de fond
    img_path = "FOND_CIEL.png"
    img_fond = mpimg.imread(img_path)

    # attribution des couleurs en fonction des masses
    Mass_colors = attribution_couleur(Mass_corps)
    # utilise la résolution par solve_ivp
    solution = resolution(V0, time_max, Nb_values, Nb_corps, Mass_corps)
    # utilise le programme de detection des collisions
    collisions = detection(V0, time_max, Nb_values, Nb_corps, Mass_corps)

    def nb_collisions(k):
        """int -> string
        permet de compter les colisions avant l'instant k"""
        i = 0
        for e in collisions:
            if e[0] <= k:
                i += 1
        return (str(i))

    rho = 3e3  # masse volumique standart pour un astre tellurique

    def lenght(m):
        """int -> int 
        permet de calculer le rayon de l'astre à partir de sa masse """
        return (m/(rho*4/3*np.pi))**1/3/(1.5e11)

    minimum = np.min([round(np.log(lenght(e)))
                     for e in Mass_corps])  # calcul du min
    # calcul de la taille des markers
    taille = [round(np.log(lenght(e)))-minimum + 2 for e in Mass_corps]

    def sup_inf(taille):
        """np array (int) -> Bool
        verifie que pas de planetre trop grosse et pas de trop petites
        """
        for e in taille:
            if e > 6:  # pas trop grosse
                return False
        for e in taille:
            if e > 3:  # pas trop petite
                return True
        return False

    if not sup_inf(taille):
        taille = [6]*Nb_corps

    fig = plt.figure()  # création figure
    axes = plt.axes()
    long_train = 10  # taille de la trainée pour les planètes

    # si position initiale pas au hasard dans ce cas rint_pos=0 (dépend du TKinter qui reçoit les valeurs)
    if rint_pos == 0:
        x0min = min(V0[0:2*Nb_corps:2])
        x0max = max(V0[0:2*Nb_corps:2])
        y0min = min(V0[1:2*Nb_corps:2])
        y0max = max(V0[1:2*Nb_corps:2])

        # Le 1 est pour éviter d'avoir une fenêtre de taille 0
        borne0 = max(abs(x0min), abs(x0max), abs(y0min), abs(y0max), 1)

        # on place les limites des axes en conséquences
        axes.set_xlim(-2*borne0, 2*borne0)
        axes.set_ylim(-2*borne0, 2*borne0)

        # boite contenant le texte pour le comptage du nombre de collision
        boite = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        txt = axes.text(1, -0.12, '', transform=axes.transAxes,
                        ha='center', bbox=boite)

        # légende des axes
        plt.xlabel("x (UA)")
        plt.ylabel("y (UA)")

        def anim(k):
            for j in range(Nb_corps):
                # permet de tracer les points avec la trainé en traçant la ligne
                lignes[j].set_data([solution.y[2*j, k:max(1, k-long_train):-1]],
                                   [solution.y[2*j+1, k:max(1, k-long_train):-1]])
            plt.title("Problème à " + str(Nb_corps) +
                      " corps à t = " + str(round(solution.t[k], 1)) + " ans")
            txt.set_text('Nombre de collisions : '+nb_collisions(k))

        # tracé des points et des trainées de chaque planètes en fonction de leur couleur
        lignes = [axes.plot([], [], "o-", markersize=taille[i], markevery=1000, color=Mass_colors[i], lw=1,)[0]
                  for i in range(Nb_corps)]

        # Création de l'animation
        anim2D = animation.FuncAnimation(
            fig, anim, frames=len(solution.t), interval=10)

        # affichage image de fond
        axes.imshow(img_fond, extent=[-2*borne0,
                    2*borne0, -2*borne0, 2*borne0])
        '''
        #############################Enregistrement GIF####################################
        writergif = animation.PillowWriter(fps=30)
        anim2D.save("./2D_terre_soleil10.gif", writer=writergif)
        ###################################################################################
        '''

        # affichage et configuration de la colorbar associée à la masse des astres
        cbar = plt.colorbar(axes.scatter([], [], c=[], cmap='coolwarm', s=0))
        cbar.set_ticks([])
        cbar.set_label('Masse (kg)')

        plt.show()

    else:  # Si on choisit des positions avec les curseurs du TKinter

        # configuration de la limite des axes
        axes.set_xlim(-2*rint_pos, 2*rint_pos)
        axes.set_ylim(-2*rint_pos, 2*rint_pos)

        # configuration de la boite contenant le compteur de colision
        boite = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        txt = axes.text(1, -0.12, '', transform=axes.transAxes,
                        ha='center', bbox=boite)

        # légende des axes
        plt.xlabel("x (UA)")
        plt.ylabel("y (UA)")

        def anim(k):
            for j in range(Nb_corps):
                # permet de tracer les points avec la trainé en traçant la ligne
                lignes[j].set_data([solution.y[2*j, k:max(1, k-long_train):-1]],
                                   [solution.y[2*j+1, k:max(1, k-long_train):-1]])
            plt.title("Problème à " + str(Nb_corps) +
                      " corps à t = " + str(round(solution.t[k], 1)) + " ans")
            txt.set_text('Nombre de colision : '+nb_collisions(k))

        # tracé des points et des trainées de chaque planètes en fonction de leur couleur
        lignes = [axes.plot([], [], "o-", markersize=taille[i], markevery=1000, color=Mass_colors[i], lw=1,)[0]
                  for i in range(Nb_corps)]

        # tracé de la zone d'apparition des planètes
        Zone_app = plt.Rectangle((-rint_pos, -rint_pos), 2*rint_pos, 2*rint_pos, fill=False,
                                 linestyle='dashed', color='red', label="zone d'apparition des planètes")
        axes.add_patch(Zone_app)

        # création de l'animation
        anim2D = animation.FuncAnimation(
            fig, anim, frames=len(solution.t), interval=10)

        # affichage de l'image de fond
        axes.imshow(img_fond, extent=[-2*rint_pos,
                    2*rint_pos, -2*rint_pos, 2*rint_pos])
        '''
        #############################Enregistrement GIF####################################
        writergif = animation.PillowWriter(fps=30)
        anim2D.save("./2D_terre_soleil10.gif", writer=writergif)
        ###################################################################################
        '''
        # position de la légende
        plt.legend(loc='upper right')

        # affichage et configuration de la colorbar associée à la masse des astres
        cbar = plt.colorbar(axes.scatter([], [], c=[], cmap='coolwarm', s=0))
        cbar.set_ticks([])
        cbar.set_label('Masse (kg)')

        plt.show()


################# TEST#################################
tf = 10
nb_valeurs = 500
N = 28
m = np.random.uniform(1E27, 1E30, N)
rint_pos = 5
pos0 = np.random.uniform(-rint_pos, rint_pos, 2*N)
rint_vit = 1
vit0 = np.random.uniform(-rint_vit, rint_vit, 2*N)
V0 = np.append(pos0, vit0)  # Vecteur à l'instant 0
#####################################################

if __name__ == "__main__":
    Anim_2D(V0, rint_pos, tf, nb_valeurs, N, m)
