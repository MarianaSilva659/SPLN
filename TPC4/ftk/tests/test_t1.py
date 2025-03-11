from ftk.probability import AbsoluteProbability, ratio

def test_ratio():
    f1 = {
        'a': AbsoluteProbability(493, 1000),
        'b': AbsoluteProbability(784, 1000),
    }
    f2 = {
        'a': AbsoluteProbability(493, 1000),
        'c': AbsoluteProbability(1000, 1000),
    }
    f = ratio(f1, f2)
    print(f)
    assert f['a'].value == 1
