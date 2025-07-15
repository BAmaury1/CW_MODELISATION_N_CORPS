import numpy as np
from DETECTION_COLLISION_2D import detection

def test_detection_no_collision():
    tf = 10
    nb_valeurs = 500
    N = 2
    Mass_corps = np.array([1e27, 2e27, 3e27])
    rint_pos = 5
    pos0 = np.array([0,0,1,0])
    rint_vit = 0
    vit0 =np.array([0,0,0,1])
    V0 = np.append(pos0, vit0)

    collisions = detection(V0, tf, nb_valeurs, N, Mass_corps)

    # Vérifiez qu'il n'y a pas de collision
    assert len(collisions) == 0

def test_detection_with_collision():
    # Créez un scénario avec collision intentionnelle
    tf = 10
    nb_valeurs = 500
    N = 2
    Mass_corps = np.array([1e27, 2e27])
    rint_pos = 5
    pos0 = np.append(np.array([0,0,0,0]),np.random.uniform(-rint_pos, rint_pos, 2 * N-4))
    # Assurez-vous que les positions initiales garantissent une collision
    pos0[2] = pos0[0]
    vit0 = np.random.uniform(-1, 1, 2 * N)
    V0 = np.append(pos0, vit0)

    collisions = detection(V0, tf, nb_valeurs, N, Mass_corps)

    # Vérifiez qu'il y a au moins une collision
    assert len(collisions) > 0
