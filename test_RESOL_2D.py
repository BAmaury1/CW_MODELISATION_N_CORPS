# test_resolution.py
import numpy as np
import pytest
from RESOL_2D import resolution

def test_resolution():
    tf = 10
    nb_valeurs = 500
    N = 12
    m = np.random.uniform(1E27, 1E30, N)
    rint_pos = 5
    pos0 = np.random.uniform(-rint_pos, rint_pos, 2 * N)
    rint_vit = 1
    vit0 = np.random.uniform(-rint_vit, rint_vit, 2 * N)
    V0 = np.append(pos0, vit0)

    result = resolution(V0, tf, nb_valeurs, N, m)

    assert len(result.t) == nb_valeurs
    assert result.y.shape == (4 * N, nb_valeurs)
