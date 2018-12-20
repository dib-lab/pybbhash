from bbhash_table import BBHashTable
import random

def test_basic():
    all_kmers = [ random.randint(100, 2**32) for i in range(100) ]
    print(len(all_kmers))

    table = BBHashTable(all_kmers)

    for kmer_hash, i in zip(all_kmers, range(100, 200)):
        table[kmer_hash] = i

    for kmer_hash, i in zip(all_kmers, range(100, 200)):
        assert table[kmer_hash] == i
