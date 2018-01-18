import bbhash

x = bbhash.PyMPHF(list(range(10)), 10, 1, 1.0)

print(x.lookup(9))

