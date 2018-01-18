# pybbhash

This is a Python (Cython) wrapper for the
[BBHash codebase](https://github.com/rizkg/BBHash) for building
[minimal perfect hash functions](https://en.wikipedia.org/wiki/Perfect_hash_function#Minimal_perfect_hash_function).

Right now, this is being used for some k-mer-based hashing foo that we 
have in [khmer](http://github.com/dib-lab/khmer).  As such, I am focused
on building MPHF for 64-bit hashes and am wrapping only that bit of the
interface; the rest should be ~straightforward (hah!).

## Big TODO items

The two remaining Big Items are:

* I would like to be able to use generic Python iterators in the PyMPHF
  construction. Right now there is a round of memory-inefficient copying of
  hashes, which is bad when you have a lot of k-mers!
  
* I would like to be able to save to/load from strings, not just files.

I also need to investigate thread safety.

## Usage:

```
import bbhash

# some collection of 64-bit (or smaller) hashes
uint_hashes = [10, 20, 50, 80]

num_threads = 1 # hopefully self-explanatory :)
gamma = 1.0     # internal gamma parameter for BBHash

mph = bbhash.PyMPHF(uint_hashes, len(uint_hashes), num_threads, gamma)

for val in uint_hashes:
    print('{} now hashes to {}'.format(val, mph.lookup(val)))

# can also use 'mph.save(filename)' and 'mph = bbhash.load_mphf(filename)'.
```

----

CTB 1/2018
