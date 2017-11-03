import numpy as np

a = b = np.arange(9).reshape(3, 3)
c = np.zeros(3)

for x in range(3):
    c[x] = np.average(b[np.where(a < x + 3)])

print(c)

a = b = np.arange(9).reshape(3, 3)
c = np.zeros(3)
i = np.arange(3)

d = b[np.where(a < (i + 3))]
print(d)
c[i] = np.average(b[np.where(a < (i + 3))])
print(c)