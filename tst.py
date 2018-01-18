import bbhash

x = bbhash.PyMPHF(list(range(10)), 10, 1, 1.0)

print(x.lookup(9))
x.save('xxx')

y = bbhash.load_mphf('xxx')

print(y.lookup(9))
