import numpy
import bbhash
import os

class BBHashTable(object):
    def __init_(self):
        pass

    def initialize(self, all_kmers, fill=0, dtype=numpy.uint32):
        self.mphf_to_kmer = numpy.zeros(len(all_kmers), numpy.uint64)
        self.mphf_to_value = numpy.full(len(all_kmers), fill, dtype)
        self.mphf = bbhash.PyMPHF(all_kmers, len(all_kmers), 4, 1.0,)

        for k in all_kmers:
            mp_hash = self.mphf.lookup(k)
            self.mphf_to_kmer[mp_hash] = k

    def __len__(self):
        return len(self.mphf_to_kmer)

    def __getitem__(self, kmer_hash, default_val=None):
        mp_hash = self.mphf.lookup(kmer_hash)
        if mp_hash is None:
            return default_val
        elif self.mphf_to_kmer[mp_hash] == kmer_hash:   # found!
            return self.mphf_to_value[mp_hash]
        return default_val

    def __setitem__(self, kmer_hash, value):
        mp_hash = self.mphf.lookup(kmer_hash)
        if mp_hash is None or self.mphf_to_kmer[mp_hash] != kmer_hash:
            raise ValueError("given kmer_hash is unknown to mphf")

        self.mphf_to_value[mp_hash] = value

    def get_unique_values(self, hashes):
        values = set()
        for hashval in hashes:
            values.add(self[hashval])
        return values

    def save(self, mphf_filename, array_filename):
        self.mphf.save(mphf_filename)
        with open(array_filename, "wb") as fp:
            numpy.savez_compressed(fp,
                                   mphf_to_kmer=self.mphf_to_kmer,
                                   mphf_to_value=self.mphf_to_value)

    @classmethod
    def load(cls, mphf_filename, array_filename):
        if not os.path.exists(mphf_filename):
            raise FileNotFoundError(mphf_filename)
        mphf = bbhash.load_mphf(mphf_filename)
        with open(array_filename, "rb") as fp:
            np_dict = numpy.load(fp)
            mphf_to_kmer = np_dict["mphf_to_kmer"]
            mphf_to_value = np_dict["mphf_to_value"]

        obj = cls()
        obj.mphf = mphf
        obj.mphf_to_kmer = mphf_to_kmer
        obj.mphf_to_value = mphf_to_value

        return obj
