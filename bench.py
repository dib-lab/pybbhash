import random, time
from bbhash_table import BBHashTable
from collections import defaultdict

all_kmers = [ random.randint(100, 2**32) for i in range(100) ]*10000
    
table = BBHashTable()
table.initialize(all_kmers)

for kmer_hash in all_kmers:
    table[kmer_hash] = kmer_hash          # as good a value as any ;)

# old style
start = time.time()
value_count = defaultdict(int)
for kmer_hash in all_kmers:
    value = table[kmer_hash]
    value_count[value] += 1
end = time.time()
old_time = end - start
print('old:', end - start)

# new style
start = time.time()
value_count = table.get_unique_values(all_kmers)
end = time.time()
print('new:', end - start)
new_time = end - start

print('speedup:', old_time / new_time)
