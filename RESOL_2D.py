import numpy as np
import random
from scipy.integrate import solve_ivp

##################################### Donéees####################################
# constante gravitationnelle adaptée aux ua et aux années
G = ((6.67428E-11)*(1/149597870700)**3)*(365.25*24*3600)**(2)

# distance résiduelles (pour éviter de diviser par 0)
e = 1E-2
#################################################################################

# Système différentiel à résoudre


def syst_diff(t, Veck, Nb_corps, Mass_corps):
    """int,list,int,int list-> float np.array
    transforme position et vitesse en vitesse et accélération
    application des lois fondamentales de la physique"""
    # Yk correspond aux positions à l'instant k sous la forme [pos masse 1, pos masse 2,vitesse masse 1, vitesse masse 2]
    vitesse = [Veck[i] for i in range(2*Nb_corps, 4*Nb_corps)]
    acceleration = []
    # acceleration = [0 for _ in range(2*N)]
    # X1, Y1, X2, Y2 = [Yk[i] for i in range(2*N)]
    for i in range(Nb_corps):
        ax = 0
        ay = 0
        for j in range(Nb_corps):
            if j != i:
                projx = Veck[2*i]-Veck[2*j]
                projy = Veck[2*i+1]-Veck[2*j+1]
                dist = ((Veck[2*j]-Veck[2*i])**2 +
                        (Veck[2*j+1]-Veck[2*i+1])**2)**(3/2)+e
                # Somme toute les contributions sur x
                ax += Mass_corps[j]*projx/dist
                # Somme toute les contributions sur y
                ay += Mass_corps[j]*projy/dist
        acceleration.append(ax*(-G))
        acceleration.append(ay*(-G))
    # Vecteur sous la forme [vxm1, vym1,vxm2, vym2,axm1, aym1,axm2, aym2]
    VeckDer = np.append(vitesse, acceleration)
    return VeckDer  # retourne le vecteur dérivé du vecteur Veck


def resolution(V0, time_max, nb_values, Nb_corps, Mass_corps):
    """int list, int,int,int,int->bunch object with the foolowing fields defined: t=ndarray,shape
    y:ndarray,shape
    ...
    résoud le système diff"""
    t = np.linspace(0, time_max, nb_values)
    # Solution du système différentiel
    solution = solve_ivp(
        syst_diff, [t[0], t[-1]], V0, t_eval=t, args=(Nb_corps, Mass_corps))
    return (solution)


################# TEST#################################
tf = 10
nb_valeurs = 500
N = 12
m = np.random.uniform(1E27, 1E30, N)
rint_pos = 5
pos0 = np.random.uniform(-rint_pos, rint_pos, 2*N)
rint_vit = 1
vit0 = np.random.uniform(-rint_vit, rint_vit, 2*N)
V0 = np.append(pos0, vit0)  # Vecteur à l'instant 0
#####################################################

# print(resolution(V0,tf,nb_valeurs,N,m))
