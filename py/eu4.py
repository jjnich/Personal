#first method
from time import time
max1 = 0
p = 999
m1, m2 = 0, 0
t = time()
while p > 100:
  n = 999
  if n < m1 and p < m2: break
  while n > 100:
    if n < m1 and p < m2: break
    a = n * p
    b = int(str(a)[::-1])
    if a==b and a > max1:
      max1 = a
      if m1 < n and m2 < p:
        m1 = n
        m2 = p
      break
    else:
      n-=1
  if a==b and a > max1:
    break
  p-=1
print "biggest pal: ", max1, "time taken: ", time()-t

#second method
def pally( x ):
  if str(x) == str(x)[::-1]:
    return True
  return False
l = time()
w =  max(filter((lambda x: str(x)==str(x)[::-1]), [(a*b) for a in range(100, 1000) for b in range(100, 1000)]))
print "biggest pal2: ", w, "time taken: ", time()-l

