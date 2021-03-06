import numpy as np
from mahotas.features import texture
import mahotas.features._texture
from nose.tools import raises

def test__cooccurence():
    cooccurence = mahotas.features._texture.cooccurence
    f = np.array([
          [0,1,1,1],
          [0,0,1,1],
          [2,2,2,2],
        ])
    Bc = np.zeros((3,3), f.dtype)
    Bc[1,2] = 1
    res = np.zeros((5,5), np.int32)
    cooccurence(f, res, Bc, 0)
    assert res[0,0] == 1
    assert res[0,1] == 2
    assert res[1,0] == 0
    assert res[1,1] == 3
    assert res[2,2] == 3
    assert not np.any(res[2,:2])
    assert not np.any(res[:2,2])
    res[:3,:3] = 0
    assert not np.any(res)

    res = np.zeros((5,5), np.int32)
    Bc = np.zeros((3,3), f.dtype)
    Bc[2,2] = 1
    cooccurence(f, res, Bc, 0)
    assert res[0,0] == 1
    assert res[0,1] == 0
    assert res[0,2] == 2
    assert res[1,0] == 0
    assert res[1,1] == 2
    assert res[1,2] == 1
    res[:3,:3] = 0
    assert not np.any(res)

def test_cooccurence_errors():
    f2 = np.zeros((6,6), np.uint8)
    f3 = np.zeros((6,6,6), np.uint8)
    f4 = np.zeros((6,6,6,6), np.uint8)
    @raises(ValueError)
    def c_1():
        texture.cooccurence(f2, -2)
    yield c_1

    @raises(ValueError)
    def c_1():
        texture.cooccurence(f3, -2)
    yield c_1

    @raises(ValueError)
    def c_2_10():
        texture.cooccurence(f2, 10)
    yield c_2_10

    @raises(ValueError)
    def c_3_17():
        texture.cooccurence(f3, 17)
    yield c_3_17

    @raises(ValueError)
    def c_4_1():
        texture.cooccurence(f4, 1)
    yield c_4_1



def brute_force(f, dy, dx):
    res = np.zeros((f.max()+1, f.max() + 1), np.double)
    for y in range(f.shape[0]):
        for x in range(f.shape[1]):
            if 0 <= y + dy < f.shape[0] and \
                0 <= x + dx < f.shape[1]:
                res[f[y,x], f[y +dy,x+dx]] += 1
    return res

def brute_force3(f, dy, dx, dz):
    res = np.zeros((f.max()+1, f.max() + 1), np.double)
    for y in range(f.shape[0]):
        for x in range(f.shape[1]):
            for z in range(f.shape[2]):
                if 0 <= y + dy < f.shape[0] and \
                    0 <= x + dx < f.shape[1] and \
                    0 <= z + dz < f.shape[2]:
                    res[f[y,x,z], f[y +dy,x+dx,z+dz]] += 1
    return res


def brute_force_sym(f, dy, dx):
    cmat = brute_force(f, dy, dx)
    return (cmat + cmat.T)

def test_cooccurence():
    np.random.seed(222)
    f = np.random.rand(32, 32)
    f = (f * 255).astype(np.int32)

    assert np.all(texture.cooccurence(f, 0, symmetric=False) == brute_force(f, 0, 1))
    assert np.all(texture.cooccurence(f, 1, symmetric=False) == brute_force(f, 1, 1))
    assert np.all(texture.cooccurence(f, 2, symmetric=False) == brute_force(f, 1, 0))
    assert np.all(texture.cooccurence(f, 3, symmetric=False) == brute_force(f, 1, -1))

    assert np.all(texture.cooccurence(f, 0, symmetric=1) == brute_force_sym(f, 0, 1))
    assert np.all(texture.cooccurence(f, 1, symmetric=1) == brute_force_sym(f, 1, 1))
    assert np.all(texture.cooccurence(f, 2, symmetric=1) == brute_force_sym(f, 1, 0))
    assert np.all(texture.cooccurence(f, 3, symmetric=1) == brute_force_sym(f, 1, -1))

def test_cooccurence3():
    np.random.seed(222)
    f = np.random.rand(32, 32, 8)
    f = (f * 255).astype(np.int32)

    for di, (d0,d1,d2) in enumerate(texture._3d_deltas):
        assert np.all(texture.cooccurence(f, di, symmetric=False) == brute_force3(f, d0, d1, d2))

def test_haralick():
    np.random.seed(123)
    f = np.random.rand(1024, 1024)
    f = (f * 255).astype(np.int32)
    feats = texture.haralick(f)
    assert not np.any(np.isnan(feats))

def test_haralick3():
    np.random.seed(123)
    f = np.random.rand(34, 12, 8)
    f = (f * 255).astype(np.int32)
    feats = texture.haralick(f)
    assert not np.any(np.isnan(feats))


def test_single_point():
    A = np.zeros((5,5), np.uint8)
    A[2,2]=12
    assert not np.any(np.isnan(texture.cooccurence(A,0)))

@raises(TypeError)
def test_float_cooccurence():
    A = np.zeros((5,5), np.float32)
    A[2,2]=12
    texture.cooccurence(A,0)

@raises(TypeError)
def test_float_haralick():
    A = np.zeros((5,5), np.float32)
    A[2,2]=12
    texture.haralick(A)

def test_haralick3d():
    np.random.seed(22)
    img = mahotas.stretch(255*np.random.rand(20,20,4))
    features = texture.haralick(img)
    assert features.shape == (13,13)

    features = texture.haralick(img[:,:,0])
    assert features.shape == (4,13)

    features = texture.haralick(img.max(0), ignore_zeros=True, preserve_haralick_bug=True, compute_14th_feature=True)
    assert features.shape == (4,14)


def test_zeros():
    zeros = np.zeros((64,64), np.uint8)
    feats = texture.haralick(zeros)
    assert not np.any(np.isnan(feats))

    feats = texture.haralick(zeros, ignore_zeros=True)
    assert not np.any(np.isnan(feats))

@raises(ValueError)
def test_4d_image():
    texture.haralick(np.arange(4**5).reshape((4,4,4,4,4)))

