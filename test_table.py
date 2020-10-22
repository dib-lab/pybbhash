from bbhash_table import BBHashTable
import random
import numpy


def test_create():
    all_kmers = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_kmers))

    table = BBHashTable()
    table.initialize(all_kmers)

    for kmer_hash, i in zip(all_kmers, range(100, 200)):
        table[kmer_hash] = i

    for kmer_hash, i in zip(all_kmers, range(100, 200)):
        assert table[kmer_hash] == i


def test_get_unique_values():
    all_kmers = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_kmers))

    table = BBHashTable()
    table.initialize(all_kmers)

    for kmer_hash, value in zip(all_kmers, [1, 2, 3, 4, 5]*20):
        table[kmer_hash] = value

    for kmer_hash, value in zip(all_kmers, [1, 2, 3, 4, 5]*20):
        assert table[kmer_hash] == value

    value_count = table.get_unique_values(all_kmers)
    assert value_count[1] == 20
    assert value_count[2] == 20
    assert value_count[3] == 20
    assert value_count[4] == 20
    assert value_count[5] == 20


def test_get_unique_values_noexist():
    all_kmers = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_kmers))

    table = BBHashTable()
    table.initialize(all_kmers)

    for kmer_hash, value in zip(all_kmers, [1, 2, 3, 4, 5]*20):
        table[kmer_hash] = value

    for kmer_hash, value in zip(all_kmers, [1, 2, 3, 4, 5]*20):
        assert table[kmer_hash] == value

    noexist_kmers = set([ random.randint(100, 2**32) for i in range(100) ])
    noexist_kmers -= set(all_kmers)
    all_kmers += list(noexist_kmers)
    value_count = table.get_unique_values(all_kmers)
    assert value_count[1] == 20
    assert value_count[2] == 20
    assert value_count[3] == 20
    assert value_count[4] == 20
    assert value_count[5] == 20
    assert len(list(value_count)) == 5


def test_save_load():
    all_kmers = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_kmers))

    table = BBHashTable()
    table.initialize(all_kmers)

    for kmer_hash, i in zip(all_kmers, range(100, 200)):
        table[kmer_hash] = i

    table.save('xxx', 'yyy')

    table2 = BBHashTable.load('xxx', 'yyy')

    for kmer_hash, i in zip(all_kmers, range(100, 200)):
        assert table2[kmer_hash] == i
