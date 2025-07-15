from RESOL_2D import resolution
import numpy as np


def position_liste(L, value):
    '''list,tupple->int 
    permet de retourner la position de la première occurence de la valeur recherché dans la liste'''
    k = 0
    while L[k] != value:
        k += 1
    return k


def detection(V0, time_max, nb_values, Nb_corps, Mass_corps):
    '''np array int,int,int,int,np array int->list 
    permet de lister toute les collisions qui ont lieu en 2D'''
    mass_vol = 5000  # masse volumique d'une planète telurique en kg/m3
    rayon_corps = [(((3*Mass_corps[i])/(4*np.pi*mass_vol))**(1/3))/(1.5E11)
                   for i in range(Nb_corps)]  # rayon des masses en UA
    # valeurs qui sont examinés pour rechercher les collisions
    solution = resolution(V0, time_max, nb_values, Nb_corps, Mass_corps)
    pos_x = []
    pos_y = []
    colision = []
    L = []

    # remplissage des listes de positions
    for i in range(Nb_corps):
        pos_x.append(solution.y[2*i])
        pos_y.append(solution.y[2*i+1])

    # test des collisions
    for t in range(nb_values):
        for i in range(1, Nb_corps):  # premier parcour sur liste des planètes
            for j in range(i):  # deuxième parcours (en triangle pour minimiser la complexité)
                # distance au carré des masses
                dist_mass = (pos_x[i][t]-pos_x[j][t])**2 + \
                    (pos_y[i][t]-pos_y[j][t])**2
                # somme des rayons au carré
                somme_rayon = (rayon_corps[i]+rayon_corps[j])**2
                # on regarde si les planètes se rapprochent trop (Facteur 100 car il y a une distance minimale de 10^(-3) UA entre les planètes pour éviter de diviser par 0)
                if dist_mass <= somme_rayon*100:
                    if (i, j) not in L:  # verifier si deja ensemble à l'instant d'avant
                        # on rajoute la collision suivante
                        colision.append([t, i, j])
                        # on change la liste de la dernière collision qui a eu lieu
                        L.append((i, j))
                else:  # si les panètes ne se touchent pas
                    if (i, j) in L:  # si elles se touchaient au moment d'avant
                        # on regarde a qu'elle position première occurence
                        k = position_liste(L, (i, j))
                        L = L[:k]+L[k+1:]  # on refait la liste sans elle
    return (colision)
