import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from RESOL_3D import resolution
from DETECTION_COLLISION_3D import detection


def attribution_couleur(Mass_corps):
    """int list->(float np.Array) np.Array
    renvoie la liste des couleurs des corps, plus la masse d'un corps est grande, plus elle sera rouge, plus elle est faible, plus elle sera bleue"""
    max = np.max(Mass_corps)
    Mass_normalise = Mass_corps/max  # normalisation pour attribuer les couleurs
    Mass_colors = plt.cm.coolwarm(Mass_normalise)  # attribution des couleurs
    return (Mass_colors)


def Anim_3D(V0, rint_pos, time_max, nb_values, Nb_corps, Mass_corps):
    """int np.array, int,int,int,int,int-> Matplotlib object
    anime en 3D la simulation à N corps sur Matplotlib en fonction des paramètres initiaux"""

    Mass_colors = attribution_couleur(Mass_corps)
    solution = resolution(V0, time_max, nb_values, Nb_corps, Mass_corps)
    collisions = detection(V0, time_max, nb_values, Nb_corps, Mass_corps)

    def nb_collisions(k):
        """int -> string
        permet de compter les colisions avant l'instant k"""
        i = 0
        for e in collisions:
            if e[0] <= k:
                i += 1
        return (str(i))

    rho = 3e3   # masse volumique standart pour un astre tellurique

    def lenght(m, rho):
        """int -> int 
        permet de calculer le rayon de l'astre à partir de sa masse """
        return (m/(rho*4/3*np.pi))**1/3/(1.5e11)

    minimum = np.min([round(np.log(lenght(e, rho)))
                     for e in Mass_corps])   # calcul du min
    # calcul de la taille des markers
    taille = [round(np.log(lenght(e, rho)))-minimum + 2 for e in Mass_corps]

    def sup_inf(taille):
        """np array (int) -> Bool
        verifie que pas de planetre trop grosse et pas de trop petites
        """
        for e in taille:
            if e > 6:   # pas trop grosse
                return False
        for e in taille:
            if e > 3:   # pas trop petite
                return True
        return False

    if not sup_inf(taille):
        taille = [6]*Nb_corps

    fig = plt.figure()  # création figure
    axes = plt.axes(projection='3d')
    long_train = 10  # taille de la trainée

    # graduation des axes
    axes.xaxis.set_major_locator(MultipleLocator(5))
    axes.yaxis.set_major_locator(MultipleLocator(5))
    axes.zaxis.set_major_locator(MultipleLocator(5))

    # couleur des plans xyz
    axes.xaxis.set_pane_color((0, 52/255, 76/255, 1))
    axes.yaxis.set_pane_color((0, 52/255, 76/255, 1))
    axes.zaxis.set_pane_color((0, 52/255, 76/255, 1))

    # si position initiale spécifié parl'utilisateur dans le TKinter (rint_pos=0)
    if rint_pos == 0:

        # définition des valeurs initiales extremales pour configurer la fenetre
        x0min = min(V0[0:3*Nb_corps:3])
        x0max = max(V0[0:3*Nb_corps:3])
        y0min = min(V0[1:3*Nb_corps:3])
        y0max = max(V0[1:3*Nb_corps:3])
        z0min = min(V0[2:3*Nb_corps:3])
        z0max = max(V0[2:3*Nb_corps:3])

        # valeur de l'extremal des positions initiales pour les bon positionnement
        borne0 = max(abs(x0min), abs(x0max), abs(y0min),
                     abs(y0max), abs(z0min), abs(z0max), 1)      # LE 1 est là pour éviter d'avoir une fenêtre de taille 0

        # limite des axes
        axes.set_xlim3d(-2*borne0, 2*borne0)
        axes.set_ylim3d(-2*borne0, 2*borne0)
        axes.set_zlim3d(-2*borne0, 2*borne0)

        # légende des axes
        axes.set_xlabel("x (UA)")
        axes.set_ylabel("y (UA)")
        axes.set_zlabel("z (UA)")

        # texte pour le compteur de collision (création d'un boite et position)
        boite = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        txt = axes.text(1, -0.12, 0, '', transform=axes.transAxes,
                        ha='center', bbox=boite)

        # enlever la grille
        axes.grid(False)

        def anim(k):
            for j in range(Nb_corps):
                # trace les deux premières coordonnées de la ligne
                lignes[j].set_data(solution.y[3*j, k:max(1, k-long_train):-1],
                                   solution.y[3*j+1, k:max(1, k-long_train):-1])
                # pour tracer la dernière coordonée de la lign e
                lignes[j].set_3d_properties(
                    solution.y[3*j+2, k:max(1, k-long_train):-1])
            # pour faire tourner le graphique à la bonne vitesse (1/4 de tour pendant l'entièreté du temps de la simulation)
            axes.view_init(azim=k*90/nb_values)
            # titre du graphique qui change au fil du temps
            plt.title("Problème à " + str(Nb_corps) +
                      " corps à t = " + str(round(solution.t[k], 1)) + " ans")
            # texte pour le nombre de collisions
            txt.set_text('nombre de collisions : ' + nb_collisions(k))

        # tracé des points et des trainées de chaque planètes en fonction de leur couleur
        lignes = [axes.plot([], [], "o-", markersize=taille[i], markevery=1000, color=Mass_colors[i], lw=1,)[0]
                  for i in range(Nb_corps)]  # couleur de chaque planète

        # création de l'animation
        anim3D = ani.FuncAnimation(
            fig, anim, frames=len(solution.t), interval=10)

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

    else:  # On passe cette condition si les valeurs sont fournies au hasard dans le TKinter
        axes.set_xlim3d(-2*rint_pos, 2*rint_pos)
        axes.set_ylim3d(-2*rint_pos, 2*rint_pos)
        axes.set_zlim3d(-2*rint_pos, 2*rint_pos)

        axes.set_xlabel("x (UA)")
        axes.set_ylabel("y (UA)")
        axes.set_zlabel("z (UA)")

        # texte pour le compteur de collision
        boite = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        txt = axes.text(1, -0.12, 0, '', transform=axes.transAxes,
                        ha='center', bbox=boite)

        axes.grid(False)

        def anim(k):
            for j in range(Nb_corps):
                lignes[j].set_data(solution.y[3*j, k:max(1, k-long_train):-1],
                                   solution.y[3*j+1, k:max(1, k-long_train):-1])
                lignes[j].set_3d_properties(
                    solution.y[3*j+2, k:max(1, k-long_train):-1])
            axes.view_init(azim=k*90/nb_values)
            plt.title("Problème à " + str(Nb_corps) +
                      " corps à t = " + str(round(solution.t[k], 1)) + " ans")
            txt.set_text('Nombre de collisions : '+nb_collisions(k))

        lignes = [axes.plot([], [], "o-", markersize=taille[i], markevery=1000, color=Mass_colors[i], lw=1,)[0]
                  for i in range(Nb_corps)]  # couleur de chaque planète

        anim3D = ani.FuncAnimation(
            fig, anim, frames=len(solution.t), interval=10)

        '''
        #############################Enregistrement GIF####################################
        writergif = animation.PillowWriter(fps=30)
        anim2D.save("./2D_terre_soleil10.gif", writer=writergif)
        ###################################################################################
        '''
        cbar = plt.colorbar(axes.scatter([], [], c=[], cmap='coolwarm', s=0))
        cbar.set_ticks([])
        cbar.set_label('Masse (kg)')

        plt.show()


################# TEST#################################
tf = 10
nb_valeurs = 500
N = 12
m = np.random.uniform(1E27, 1E30, N)
rint_pos = 5
pos0 = np.random.uniform(-rint_pos, rint_pos, 3*N)
rint_vit = 1
vit0 = np.random.uniform(-rint_vit, rint_vit, 3*N)
V0 = np.append(pos0, vit0)  # Vecteur à l'instant 0
#####################################################

if __name__ == "__main__":
    Anim_3D(V0, rint_pos, tf, nb_valeurs, N, m)
