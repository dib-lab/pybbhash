import bbhash

# some collection of 64-bit (or smaller) hashes
uint_hashes = [10, 20, 50, 80]

num_threads = 1 # hopefully self-explanatory :)
gamma = 1.0     # internal gamma parameter for BBHash

mph = bbhash.PyMPHF(uint_hashes, len(uint_hashes), num_threads, gamma)

for val in uint_hashes:
    print('{} now hashes to {}'.format(val, mph.lookup(val)))

# can also use 'mph.save(filename)' and 'mph = bbhash.load_mphf(filename)'.
