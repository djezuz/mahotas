import mahotas
import numpy as np
from mahotas.colors import rgb2xyz, rgb2lab, xyz2rgb, rgb2grey

def test_colors():
    f = mahotas.imread('mahotas/demos/data/luispedro.jpg')
    lab = rgb2lab(f)
    assert np.max(np.abs(lab)) <= 100.
    assert np.max(np.abs(xyz2rgb(rgb2xyz(f)) - f)) < 1.

    lab8 = rgb2lab(f, dtype=np.uint8)
    assert lab.dtype != np.uint8
    assert lab8.dtype == np.uint8

    xyz = rgb2xyz(f, dtype=np.uint8)
    assert xyz.shape == f.shape
    assert xyz.dtype == np.uint8


def test_rgb2grey():
    f = mahotas.imread('mahotas/demos/data/luispedro.jpg')
    fg = rgb2grey(f)
    fg8 = rgb2grey(f, dtype=np.uint8)
    assert f.ndim == 3
    assert fg.ndim == 2
    assert fg8.ndim == 2
    assert fg.shape[0] == f.shape[0]
    assert fg.shape[1] == f.shape[1]
    assert fg.shape == fg8.shape
    assert fg8.dtype == np.uint8

