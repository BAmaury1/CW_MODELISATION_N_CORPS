import numpy as np
import random
from scipy.integrate import solve_ivp

#####################################Donéees####################################
# constante gravitationnelle adaptée aux ua et aux années 
G = ((6.674E-11)*(6.684E-12)**3)*(365.25*24*3600)**(2)

# distance résiduelles (pour éviter de diviser par 0)
e = 1E-2
#################################################################################

# Système différentiel à résoudre
def syst_diff(t, Veck,Nb_corps,Mass_corps):
    """int,float np.array, int,int-> float np.Array
    transforme position et vitesse en vitesse et accélération"""
    # Yk correspond aux positions à l'instant k sous la forme [pos masse 1, pos masse 2,vitesse masse 1, vitesse masse 2]
    vitesse = [Veck[i] for i in range(3*Nb_corps, 6*Nb_corps)]
    acceleration = []
    for i in range(Nb_corps):
        ax = 0
        ay = 0
        az = 0
        for j in range(Nb_corps):
            if j != i:
                projx=Veck[3*i]-Veck[3*j]
                projy=Veck[3*i+1]-Veck[3*j+1]
                projz=Veck[3*i+2]-Veck[3*j+2]
                dist=(projx**2+projy**2+projz**2)**(3/2)+e
                ax += Mass_corps[j]*projx/dist #Somme toute les contributions sur x
                ay += Mass_corps[j]*projy/dist
                az += Mass_corps[j]*projz/dist#Somme toute les contributions sur y
        acceleration.append(ax*(-G))
        acceleration.append(ay*(-G))
        acceleration.append(az*(-G))
    VeckDer =np.append(vitesse,acceleration) #Vecteur sous la forme [vxm1, vym1,vxm2, vym2,axm1, aym1,axm2, aym2]
    return VeckDer #retourne le vecteur dérivé du vecteur Veck

def resolution(V0,time_max,nb_values,Nb_corps, Mass_corps):
    """int np.Array,int,int,int,int list-> bunch object (solve_ivp)"""
    t=np.linspace(0, time_max, nb_values)
    solution = solve_ivp(syst_diff, [t[0], t[-1]], V0, t_eval=t, args=(Nb_corps, Mass_corps)) #Solution du système différentiel 
    return(solution)


#################TEST#################################
tf = 10
nb_valeurs = 500
N = 12
m = np.random.uniform(1E27, 1E30, N)
rint_pos=5
pos0 = np.random.uniform(-rint_pos, rint_pos, 3*N)
rint_vit=1
vit0 = np.random.uniform(-rint_vit, rint_vit, 3*N)
V0 = np.append(pos0, vit0) #Vecteur à l'instant 0
#####################################################

#print(resolution(V0,tf,nb_valeurs,N,m))
