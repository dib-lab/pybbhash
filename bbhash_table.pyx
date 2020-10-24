from libc.stdint cimport UINT32_MAX, UINT64_MAX, uint64_t, uint32_t
from cython.operator cimport dereference as deref
from libcpp.memory cimport unique_ptr

import numpy
import bbhash
import os
from collections import defaultdict

class BBHashTable(object):
    """\
    Retrieve values by MPHF lookup.

    Handles the situation where the query hash may not be in the table.
    """
    dtype = numpy.uint32

    def __init_(self):
        pass

    def initialize(self, all_hashes, fill=None):
        "Initialize table with set of hashes."
        if fill is None:
            fill = numpy.iinfo(self.dtype).max   # @CTB test

        # MPHF -> hash
        self.mphf_to_hash = numpy.zeros(len(all_hashes), numpy.uint64)
        # MPHF -> stored value 
        self.mphf_to_value = numpy.full(len(all_hashes), fill, self.dtype)
        self.mphf = bbhash.PyMPHF(all_hashes, len(all_hashes), 4, 1.0,)

        for k in all_hashes:
            mp_hash = self.mphf.lookup(k)
            self.mphf_to_hash[mp_hash] = k

    def __len__(self):
        "Size of table."
        return len(self.mphf_to_hash)

    def __getitem__(self, hashval, default_val=None):
        "Retrieve value for item."
        mp_hash = self.mphf.lookup(hashval)
        if mp_hash is None:
            return default_val
        elif self.mphf_to_hash[mp_hash] == hashval:   # found!
            return self.mphf_to_value[mp_hash]
        return default_val

    def __setitem__(self, hashval, value):
        "Save value."
        mp_hash = self.mphf.lookup(hashval)
        if mp_hash is None or self.mphf_to_hash[mp_hash] != hashval:
            raise ValueError("given hashval is unknown to mphf")

        self.mphf_to_value[mp_hash] = value

    def get_unique_values(self, hashes, require_exist=False):
        "Retrieve unique values for item."
        values = defaultdict(int)

        if type(hashes) != numpy.ndarray:
            hashes = numpy.fromiter(hashes, numpy.uint64, len(hashes))
        cdef uint64_t[:] hashes_view = hashes
        cdef uint32_t c_hashes_len = len(hashes)

        mp_hashes = self.mphf.lookup_many(hashes)
        cdef uint64_t[:] mp_hashes_view = mp_hashes

        cdef uint64_t[:] mphf_to_hash_view = self.mphf_to_hash
        cdef uint32_t[:] mphf_to_value_view = self.mphf_to_value

        cdef uint64_t c_mp_hash
        cdef uint32_t c_value

        cdef uint32_t i = 0
        while i < c_hashes_len:
            c_hashval = hashes_view[i]
            c_mp_hash = mp_hashes_view[i]
 
            if c_mp_hash != UINT64_MAX and \
               mphf_to_hash_view[c_mp_hash] == c_hashval:   # found!
                c_value = mphf_to_value_view[c_mp_hash]
                values[c_value] += 1
            elif require_exist:
                raise ValueError("hash at position {} does not exist".format(i))
            i += 1

        return values

    def save(self, mphf_filename, array_filename):
        "Save to disk."
        self.mphf.save(mphf_filename)
        with open(array_filename, "wb") as fp:
            numpy.savez_compressed(fp,
                                   mphf_to_hash=self.mphf_to_hash,
                                   mphf_to_value=self.mphf_to_value)

    @classmethod
    def load(cls, mphf_filename, array_filename):
        "Load from disk."
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
