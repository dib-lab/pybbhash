"Test BBHashTable."
import random
import tempfile
import os.path

from bbhash_table import BBHashTable


def test_create():
    # try creating and using a BBHashTable to store hashes and associated vals.
    all_hashes = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_hashes))

    table = BBHashTable()
    table.initialize(all_hashes)

    for hashval, i in zip(all_hashes, range(100, 200)):
        table[hashval] = i

    for hashval, i in zip(all_hashes, range(100, 200)):
        assert table[hashval] == i


def test_get_unique_values():
    # test the 'get_unique_values' functionality.
    all_hashes = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_hashes))

    table = BBHashTable()
    table.initialize(all_hashes)

    for hashval, value in zip(all_hashes, [1, 2, 3, 4, 5]*20):
        table[hashval] = value

    for hashval, value in zip(all_hashes, [1, 2, 3, 4, 5]*20):
        assert table[hashval] == value

    value_count = table.get_unique_values(all_hashes)
    assert value_count[1] == 20
    assert value_count[2] == 20
    assert value_count[3] == 20
    assert value_count[4] == 20
    assert value_count[5] == 20


def test_get_unique_values_noexist():
    # check to see what happens when we add in hashes that don't exist.
    all_hashes = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_hashes))

    table = BBHashTable()
    table.initialize(all_hashes)

    for hashval, value in zip(all_hashes, [1, 2, 3, 4, 5]*20):
        table[hashval] = value

    for hashval, value in zip(all_hashes, [1, 2, 3, 4, 5]*20):
        assert table[hashval] == value

    noexist_hashes = set([ random.randint(100, 2**32) for i in range(100) ])
    noexist_hashes -= set(all_hashes)
    all_hashes += list(noexist_hashes)
    value_count = table.get_unique_values(all_hashes)
    assert value_count[1] == 20
    assert value_count[2] == 20
    assert value_count[3] == 20
    assert value_count[4] == 20
    assert value_count[5] == 20
    assert len(list(value_count)) == 5


def test_save_load(tmpdir):
    # test save & load!
    all_hashes = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_hashes))

    table = BBHashTable()
    table.initialize(all_hashes)

    for hashval, i in zip(all_hashes, range(100, 200)):
        table[hashval] = i

    mphf_filename = os.path.join(tmpdir, 'table.mphf')
    array_filename = os.path.join(tmpdir, 'table.array')

    table.save(mphf_filename, array_filename)

    table2 = BBHashTable.load(mphf_filename, array_filename)

    for hashval, i in zip(all_hashes, range(100, 200)):
        assert table2[hashval] == i
