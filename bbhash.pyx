from libcpp.vector cimport vector

# distutils: language = c++
cdef extern from "bbhash-wrap.hh" namespace "boomphf":
    cdef cppclass mphf[T,U]:
        mphf() except +

cdef extern from "bbhash-wrap.hh":
    cdef cppclass kmer_mphf:
        kmer_mphf(vector[unsigned long long] kmers, int nelem, int num_thread, float gamma)
        int lookup(int)

cdef class PyMPHF:
    cdef kmer_mphf * c_mphf
    def __cinit__(self, list kk, int nelem, int num_thread, float gamma):
        cdef vector[unsigned long long] kmers = kk;
        self.c_mphf = new kmer_mphf(kmers, nelem, num_thread, gamma);

    def lookup(self, int kmer):
        return self.c_mphf.lookup(kmer)
