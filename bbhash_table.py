import numpy
import bbhash

class BBHashTable(object):
    def __init__(self, all_kmers, fill=0, dtype=numpy.uint32):
        self.mphf_to_kmer = numpy.zeros(len(all_kmers), numpy.uint64)
        self.mphf_to_table = numpy.full(len(all_kmers), fill, dtype)
        self.mphf = bbhash.PyMPHF(all_kmers, len(all_kmers), 4, 1.0)

        for k in all_kmers:
            mp_hash = self.mphf.lookup(k)
            self.mphf_to_kmer[mp_hash] = k

    def __getitem__(self, kmer_hash):
        mp_hash = self.mphf.lookup(kmer_hash)
        if mp_hash is None:
            return None
        elif self.mphf_to_kmer[mp_hash] == kmer_hash:   # found!
            return self.mphf_to_table[mp_hash]
        return None

    def __setitem__(self, kmer_hash, value):
        mp_hash = self.mphf.lookup(kmer_hash)
        if mp_hash is None or self.mphf_to_kmer[mp_hash] != kmer_hash:
            raise ValueError("given kmer_hash is unknown to mphf")

        self.mphf_to_table[mp_hash] = value
