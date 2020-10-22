from bbhash_table2 import BBHashTable
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
