# test_simulation.py
import numpy as np
import pytest
from RESOL_3D import syst_diff, resolution

def test_syst_diff():
    # Testons la fonction syst_diff avec des valeurs spécifiques
    t = 0
    Veck = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    Nb_corps = 2
    Mass_corps = np.array([1e25, 2e25])
    
    result = syst_diff(t, Veck, Nb_corps, Mass_corps)

    # Vérifions que la longueur du résultat est correcte
    assert len(result) == len(Veck)

def test_resolution():
    # Testons la fonction resolution avec des valeurs spécifiques
    tf = 10
    nb_valeurs = 500
    N = 2
    Mass_corps = np.array([1e25, 2e25])
    rint_pos = 5
    pos0 = np.random.uniform(-rint_pos, rint_pos, 3 * N)
    rint_vit = 1
    vit0 = np.random.uniform(-rint_vit, rint_vit, 3 * N)
    V0 = np.append(pos0, vit0)

    result = resolution(V0, tf, nb_valeurs, N, Mass_corps)

    # Vérifions que la longueur des résultats est correcte
    assert len(result.t) == nb_valeurs
    assert result.y.shape == (6 * N, nb_valeurs)

