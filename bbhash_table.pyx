import numpy
import bbhash
import os

class BBHashTable(object):
    """\
    Retrieve values by MPHF lookup.

    Handles the situation where the query hash may not be in the table.
    """
    def __init_(self):
        pass

    def initialize(self, all_hashes, fill=0, dtype=numpy.uint32):
        # MPHF -> hash
        self.mphf_to_hash = numpy.zeros(len(all_hashes), numpy.uint64)
        # MPHF -> stored value 
        self.mphf_to_value = numpy.full(len(all_hashes), fill, dtype)
        self.mphf = bbhash.PyMPHF(all_hashes, len(all_hashes), 4, 1.0,)

        for k in all_hashes:
            mp_hash = self.mphf.lookup(k)
            self.mphf_to_hash[mp_hash] = k

    def __len__(self):
        return len(self.mphf_to_hash)

    def __getitem__(self, hashval, default_val=None):
        mp_hash = self.mphf.lookup(hashval)
        if mp_hash is None:
            return default_val
        elif self.mphf_to_hash[mp_hash] == hashval:   # found!
            return self.mphf_to_value[mp_hash]
        return default_val

    def __setitem__(self, hashval, value):
        mp_hash = self.mphf.lookup(hashval)
        if mp_hash is None or self.mphf_to_hash[mp_hash] != hashval:
            raise ValueError("given hashval is unknown to mphf")

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
                                   mphf_to_hash=self.mphf_to_hash,
                                   mphf_to_value=self.mphf_to_value)

    @classmethod
    def load(cls, mphf_filename, array_filename):
        if not os.path.exists(mphf_filename):
            raise FileNotFoundError(mphf_filename)
        mphf = bbhash.load_mphf(mphf_filename)
        with open(array_filename, "rb") as fp:
            np_dict = numpy.load(fp)
            mphf_to_hash = np_dict["mphf_to_hash"]
            mphf_to_value = np_dict["mphf_to_value"]

        obj = cls()
        obj.mphf = mphf
        obj.mphf_to_hash = mphf_to_hash
        obj.mphf_to_value = mphf_to_value

        return obj
