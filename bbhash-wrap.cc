#include "bbhash-wrap.hh"

using namespace std;

kmer_mphf::kmer_mphf(std::vector<uint64_t> kmers, size_t nelem, int num_thread,
                     double gamma)
{
    bphf = new boomphf::mphf<uint64_t, hasher_t>(nelem, kmers, num_thread, gamma);
}

uint64_t kmer_mphf::lookup(uint64_t kmer) { return bphf->lookup(kmer); }
