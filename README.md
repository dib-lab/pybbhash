# pybbhash

<a href="https://pypi.org/project/bbhash/"><img alt="PyPI" src="https://badge.fury.io/py/bbhash.svg"></a>
<a href="https://github.com/dib-lab/pybbhash/blob/latest/LICENSE.txt"><img alt="License: 3-Clause BSD" src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg"></a>

This is a Python (Cython) wrapper for the
[BBHash codebase](https://github.com/rizkg/BBHash) for building
[minimal perfect hash functions](https://en.wikipedia.org/wiki/Perfect_hash_function#Minimal_perfect_hash_function).

Right now, this is supporting k-mer-based hashing needs from
[spacegraphcats](https://github.com/spacegraphcats/spacegraphcats),
using hash values generated (mostly) by murmurhash, e.g. from
[khmer's Nodetable](https://github.com/dib-lab/khmer/) and
[sourmash](https://github.com/dib-lab/sourmash/) hashing.  As such, I
am focused on building MPHF for 64-bit hashes and am wrapping only
that bit of the interface; the rest should be ~straightforward (hah!).

I've also added a Python-accessible "values table", `BBHashTable`, in
the `bbhash_table` module. This is a table that supports a dictionary-like
feature where you can associate a hash with a value, and then query the
table with the hash to retrieve the value. The only tricky bit here is
that unlike the bbhash module, this table supports queries with hashes
that are *not* in the MPHF.

## Thoughts for further improvement.

* I would like to be able to use generic Python iterators in the PyMPHF
  construction. Right now there is a round of memory-inefficient copying of
  hashes, which is bad when you have a lot of k-mers!
  
* I would like to be able to save to/load from strings, not just files.

I also need to investigate thread safety.

## Usage

### Usage of core bbhash functionality:

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

### Usage of BBHashTable

```
import random
from collections import defaultdict
from bbhash_table import BBHashTable

all_hashes = [ random.randint(100, 2**32) for i in range(200) ]
half_hashes = all_hashes[:100]

table = BBHashTable()

# hash the first 100 of the hashes
table.initialize(half_hashes)

# store associated values
for hashval, value in zip(half_hashes, [ 1, 2, 3, 4, 5 ] *20):
   table[hashval] = value
   
# retrieve & count for all (which will include hashes not in MPHF)
d = defaultdict(int)
for hashval in all_hashes:
   value = table[hashval]
   d[value] += 1

assert d[1] == 20
assert d[None] == 100
```

The last for loop can be done quickly, in Cython, using

```
d = table.get_unique_values(all_hashes)
```

Motivation: the table is a useful way to (just for one hypothetical
example :) store a mapping from k-mers to compact De Bruijn graph node
IDs.  (We use this in several places in spacegraphcats!)

----

CTB Oct 2020
