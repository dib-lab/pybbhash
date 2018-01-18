# distutils: language = c++
from libcpp.vector cimport vector

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

### import C++ wrapper in bbhash-wrap

cdef extern from "bbhash-wrap.hh" namespace "boomphf":
    cdef cppclass mphf[T,U]:
        mphf() except +

cdef extern from "bbhash-wrap.hh":
    cdef cppclass kmer_mphf:
        kmer_mphf(vector[unsigned long long] kmers, int nelem, int num_thread, float gamma)
        int lookup(int)
        void load(ifstream *)
        void save(ofstream *)

### provide a Python wrapper.

cdef class PyMPHF:
    cdef kmer_mphf * c_mphf

    def __cinit__(self, list kk, int nelem, int num_thread, float gamma):
        cdef vector[unsigned long long] kmers = kk;
        self.c_mphf = new kmer_mphf(kmers, nelem, num_thread, gamma);

    def lookup(self, unsigned long long kmer):
        return self.c_mphf.lookup(kmer)

    def save(self, str filename):
        cdef ofstream* outputter
        outputter = new ofstream(filename.encode(), binary)
        try:
            self.c_mphf.save(outputter)
        finally:
            del outputter

    def load(self, str filename):
        cdef ifstream* inputter
        inputter = new ifstream(filename.encode(), binary)
        try:
            self.c_mphf.load(inputter)
        finally:
            del inputter

def load_mphf(filename):
    m = PyMPHF([], 0, 1, 1.0)
    m.load(filename)

    return m
