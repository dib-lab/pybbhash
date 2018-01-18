#include "BooPHF.h"
#include <vector>

typedef boomphf::SingleHashFunctor<u_int64_t>  hasher_t;

class kmer_mphf
{
public:
    boomphf::mphf<uint64_t, hasher_t> * bphf;
    kmer_mphf();
    kmer_mphf(std::vector<uint64_t> kmers, size_t nelem, int num_thread,
              double gamma);
    uint64_t lookup(uint64_t kmer);

    void load(std::istream *is) const;
    void save(std::ostream *os) const;
};
