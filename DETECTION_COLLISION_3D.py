##################################################################################################################################
##################################### code fonctionnant pareil qu'en 2D############################################################
##################################################################################################################################
from RESOL_3D import resolution
import numpy as np


def position_liste(L, value):
    k = 0
    while L[k] != value:
        k += 1
    return k


def detection(V0, time_max, nb_values, Nb_corps, Mass_corps):
    '''np array int,int,int,int,np array int->list 
    permet de lister toute les collisions qui ont lieu en 3D'''
    mass_vol = 5000  # kg/m3
    rayon_corps = [(((3*Mass_corps[i])/(4*np.pi*mass_vol))**(1/3))/(1.5E11)
                   for i in range(Nb_corps)]  # rayon des masses en UA
    solution = resolution(V0, time_max, nb_values, Nb_corps, Mass_corps)
    pos_x = []
    pos_y = []
    pos_z = []
    for i in range(Nb_corps):
        pos_x.append(solution.y[3*i])
        pos_y.append(solution.y[3*i+1])
        pos_z.append(solution.y[3*i+2])
    colision = []
    L = []
    for t in range(nb_values):
        for i in range(1, Nb_corps):
            for j in range(i):
                dist_mass = (pos_x[i][t]-pos_x[j][t])**2 + (pos_y[i]
                                                            [t]-pos_y[j][t])**2 + (pos_z[i][t]-pos_z[j][t])**2
                somme_rayon = (rayon_corps[i]+rayon_corps[j])**2
                # (Facteur 100 car il y a une distance minimale de 10^(-3) UA entre les planètes pour éviter de diviser par 0)
                if dist_mass <= somme_rayon*100:
                    if (i, j) not in L:
                        colision.append([t, i, j])
                        L.append((i, j))
                else:
                    if (i, j) in L:
                        k = position_liste(L, (i, j))
                        L = L[:k]+L[k+1:]
    return (colision)
