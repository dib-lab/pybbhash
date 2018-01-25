import bbhash

def test_all(tmpdir):
    x = bbhash.PyMPHF(list(range(10)), 10, 1, 1.0)
    assert x.lookup(9) == 8

    output = tmpdir.join('xxx')
    x.save(str(output))

    y = bbhash.load_mphf(str(output))
    assert y.lookup(9) == 8


def test_lookup():
    x = bbhash.PyMPHF(list(range(10)), 10, 1, 1.0)
    assert all(x.lookup(y) is not None for y in range(10))
    assert x.lookup(200) is None
