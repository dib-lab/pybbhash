"Test BBHashTable."
import random
import tempfile
import os.path
from collections import defaultdict

import pytest

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


def test_create_fill_default():
    # default value should be int32 max
    all_hashes = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_hashes))

    table = BBHashTable()
    # don't specify default value -
    table.initialize(all_hashes)

    # retrieve - what do we get?
    for hashval, i in zip(all_hashes, range(100, 200)):
        assert table[hashval] == 2**32 - 1


def test_create_fill_specify():
    # test specifying a default value
    all_hashes = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_hashes))

    table = BBHashTable()
    # specify a default value...
    table.initialize(all_hashes, fill=5)

    # retrieve - what do we get?
    for hashval, i in zip(all_hashes, range(100, 200)):
        assert table[hashval] == 5


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

    # since we're using random, we have to make sure the non-existent hashes
    # are not present in all_hashes. Convoluted, yes... but saves us from
    # that one in a bajillion chance of collision making the test fail! :)
    noexist_hashes = set([ random.randint(100, 2**32) for i in range(100) ])
    noexist_hashes -= set(all_hashes)
    all_hashes += list(noexist_hashes)
    value_counts = table.get_unique_values(all_hashes)
    assert value_counts[1] == 20
    assert value_counts[2] == 20
    assert value_counts[3] == 20
    assert value_counts[4] == 20
    assert value_counts[5] == 20
    assert len(list(value_counts)) == 5

    # compare get_unique_values with boring old for loop
    value_counts = defaultdict(int)
    for hashval in all_hashes:
        value = table[hashval]
        value_counts[value] += 1

    assert value_counts[None] == len(noexist_hashes)
    assert value_counts[1] == 20
    assert value_counts[2] == 20
    assert value_counts[3] == 20
    assert value_counts[4] == 20
    assert value_counts[5] == 20


def test_get_unique_values_noexist_fail():
    # test requirement that hashes exist
    all_hashes = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_hashes))

    table = BBHashTable()
    table.initialize(all_hashes)

    for hashval, value in zip(all_hashes, [1, 2, 3, 4, 5]*20):
        table[hashval] = value

    noexist_hash = all_hashes[0] + 1
    while noexist_hash in all_hashes:
        noexist_hash += 1

    value_counts = table.get_unique_values([ noexist_hash ])
    assert not value_counts

    with pytest.raises(ValueError) as exc:
        value_counts = table.get_unique_values([ noexist_hash ],
                                               require_exist=True)
    print(str(exc))


def test_get_unique_values_set():
    # try passing in a set, instead of list
    all_hashes = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_hashes))

    table = BBHashTable()
    table.initialize(all_hashes)

    for hashval, value in zip(all_hashes, [1, 2, 3, 4, 5]*20):
        table[hashval] = value

    hashvals_set = set(all_hashes)

    value_counts = table.get_unique_values(hashvals_set)
    assert value_counts


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
