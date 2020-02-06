import random

random.seed(5)
r=random.sample(range(50),8)
r.sort()
print(r)

print(list(range(0,len(r))))