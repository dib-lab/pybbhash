# distutils: language = c++
from libcpp.vector cimport vector
from libcpp.memory cimport unique_ptr
from libc.stdint cimport UINT32_MAX, uint64_t, uint32_t, UINT64_MAX
from cython.operator cimport dereference as deref

import numpy

### wrap iostream stuff

# iostream stuff taken from:
#   https://stackoverflow.com/questions/30984078/cython-working-with-c-streams
cdef extern from "<iostream>" namespace "std":
    cdef cppclass ostream:
        ostream& write(const char*, int) except +

    cdef cppclass istream:
        istream& read(char *, int) except +

# obviously std::ios_base isn't a namespace, but this lets
# Cython generate the correct C++ code
cdef extern from "<iostream>" namespace "std::ios_base":
    cdef cppclass open_mode:
        pass
    cdef open_mode binary
    # you can define other constants as needed

cdef extern from "<fstream>" namespace "std":
    cdef cppclass ofstream(ostream):
        # constructors
        ofstream(const char*) except +
        ofstream(const char*, open_mode) except+

    cdef cppclass ifstream(istream):
        # constructors
        ifstream(const char*) except +
        ifstream(const char*, open_mode) except+

### Wrap the headers from BBhash

cdef extern from "BooPHF.h" namespace "boomphf":
    cdef cppclass SingleHashFunctor[T]:
        uint64_t operator ()

    cdef cppclass mphf[T,U]:
        mphf(unsigned long long, vector[T], int, float, bool, bool) except +
        uint64_t lookup(uint64_t)
        void save(ofstream)
        void load(ifstream)

### provide a Python wrapper.

ctypedef SingleHashFunctor[uint64_t] hasher_t
ctypedef mphf[uint64_t, hasher_t] mphf_t

cdef class PyMPHF:
    cdef unique_ptr[mphf_t] c_mphf

    def __cinit__(self, list kk, unsigned long long nelem, int num_thread, float gamma):
        cdef vector[uint64_t] kmers = kk
        self.c_mphf.reset(new mphf_t(nelem, kmers, num_thread, gamma, False, False))

    def lookup(self, uint64_t kmer):
        cdef uint64_t value = deref(self.c_mphf).lookup(kmer)
        if value != UINT64_MAX:
            return value
        return None

    def lookup_many(self, hashes):
        if type(hashes) != numpy.ndarray:
            hashes = numpy.fromiter(hashes, numpy.uint64, len(hashes))
        cdef uint32_t c_hashes_len = len(hashes)
        cdef uint64_t[:] hashes_view = hashes

        mp_hashes = numpy.ndarray(c_hashes_len, dtype=numpy.uint64)
        cdef uint64_t[:] mp_hashes_view = mp_hashes

        cdef uint32_t i = 0
        while i < c_hashes_len:
            mp_hashes_view[i] = deref(self.c_mphf).lookup(hashes_view[i])
            i += 1

        return mp_hashes

    def save(self, str filename):
        cdef ofstream* outputter
        outputter = new ofstream(filename.encode(), binary)
        try:
            deref(self.c_mphf).save(deref(outputter))
        finally:
            del outputter

    def load(self, str filename):
        cdef ifstream* inputter
        inputter = new ifstream(filename.encode(), binary)
        try:
            deref(self.c_mphf).load(deref(inputter))
        finally:
            del inputter

def load_mphf(filename):
    m = PyMPHF([], 0, 1, 1.0)
    m.load(filename)

    return m
