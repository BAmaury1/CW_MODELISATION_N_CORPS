from RESOL_2D import resolution
import matplotlib.colors as mcolo
import matplotlib.image as mpimg
from scipy.integrate import solve_ivp
from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.widgets import Slider
import math


def Anim_2D_solaire(V0, time_max, nb_values, Nb_corps, Mass_corps):
    """int np.array,int,int,int,int-> matplolib object
    renvoie une simulation du système solaire avec les paramètres considérés"""

    # couleurs des planètes
    colors_p = ['#FCE570', '#8c8c94', '#ebe0c6', '#6b93d6', '#c67b5c', '#d8ca9d',
                '#c4b08b', '#d1e7e7', '#5b5ddf']  # liste couleurs de nos planètes

    solution = resolution(V0, time_max, nb_values, Nb_corps, Mass_corps)

    long_train = 1000  # taille de la trainée des planètes

    fig = plt.figure()  # création de la figure et des axes
    axes = plt.axes()

    # on calcule la taille de la fenêtre d'affichage

    x0min = min(V0[0:2*Nb_corps:2])
    x0max = max(V0[0:2*Nb_corps:2])
    y0min = min(V0[1:2*Nb_corps:2])
    y0max = max(V0[1:2*Nb_corps:2])

    borne0 = max(abs(x0min), abs(x0max), abs(y0min), abs(y0max))

    axes.set_xlim(-borne0*1.1, 1.1*borne0)
    axes.set_ylim(-borne0*1.1, 1.1*borne0)
    axzoom = plt.axes([0.87, 0.1, 0.02, 0.6])

    szoom = Slider(axzoom, 'Zoom', 0, 100,
                   valinit=1, orientation='vertical', valstep=[n for n in range(1, 101)])  # création d'un curseur pour zoomer dans la simulation

    def MAJ_zoom(val):
        lim = 1.1*borne0
        new_lim = lim/szoom.val
        axes.set_xlim(-new_lim, new_lim)
        axes.set_ylim(-new_lim, new_lim)
        fig.canvas.draw_idle()
    szoom.on_changed(MAJ_zoom)

    plt.xlabel("x (UA)")
    plt.ylabel("y (UA)")

    def anim(k):
        for j in range(Nb_corps):
            # distance entre l'astre et le soleil pour rendre la longueur de la trainée proportionnelle
            dist_sol = math.ceil(
                (solution.y[2*j, k]**2+solution.y[2*j+1, k]**2)**(1/2))
            # permet de tracer les points avec la trainé en traçant la ligne( trainée proportionnelle à la distance au soleil)
            lignes[j].set_data([solution.y[2*j, k:max(1, k-(long_train*dist_sol**2)):-1]],
                               [solution.y[2*j+1, k:max(1, k-(long_train*dist_sol**2)):-1]])
        plt.title("Système solaire à t = " +
                  str(round(solution.t[k], 1)) + " ans", x=-15, y=1.35)

    lignes = [axes.plot([], [], "o-", markersize=10, markevery=1000, color=colors_p[0], lw=1)[0]]+[axes.plot([], [], "o-", markersize=4, markevery=100000, color=colors_p[i], lw=1,)[0]
                                                                                                   for i in range(1, Nb_corps)]  # couleur de chaque planète
    saut = 350  # sauter des frames pour accélérer l'animation
    anim2D = animation.FuncAnimation(
        fig, anim, frames=[k for k in range(0, nb_valeurs, saut)], interval=1, blit=False, cache_frame_data=False)

    img_path = "FOND_CIEL.png"
    img_fond = mpimg.imread(img_path)
    # affichage image de fond
    axes.imshow(img_fond, extent=[-1.1*borne0,
                1.1*borne0, -1.1*borne0, 1.1*borne0])

    plt.legend(lignes, ['Soleil', 'Mercure', 'Venus', 'Terre',
               'Mars', 'Jupiter', 'Saturne', 'Uranus', 'Neptune'], bbox_to_anchor=(-35, 0, 0.5, 1))  # affichage de la légende

    '''#############################Enregistrement GIF####################################
    writergif = animation.PillowWriter(fps=30)
    anim2D.save("./2D_terre_soleil10.gif", writer=writergif)
    ###################################################################################
    '''

    plt.show()
    return


################# TEST#################################
tf = 10
nb_valeurs = 100000

m = np.array([1.9891e30, 3.302e23, 4.8685e24, 5.9736e24,
             6.4185e23, 1.8986e27, 5.6846e26, 8.6810e25, 1.0243e26])
N = len(m)
pos0 = np.array([0, 0, 3.52236e10, -4.5987e10, 0, 1.08208930e11, -1.495978875e11, 0, 0, -2.27936637e11,
                7.78412027e11, 0, 0, 1.421179772e12, -2.876679082e12, 0, 0, -4.503443661e12])
pos0 = pos0*(1/149597870700)
# changment d'unité
vit0 = np.array([0, 0, 3.08175e4, 2.686828e4, -3.502e4, 0, 0, -29291, 24077,
                0, 0, 13057.2, -9644.6, 0, 0, -6.81e3, 5431.7, 0])
vit0 = vit0*(365.25*24*3600)*(1/149597870700)  # changment d'unité
V0 = np.append(pos0, vit0)  # Vecteur à l'instant 0

#####################################################


if __name__ == "__main__":
    Anim_2D_solaire(V0, tf, nb_valeurs, N, m)
