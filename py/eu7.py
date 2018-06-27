import math
from time import time

def isPrime( n ):
  if n % 2 == 0 and n > 2: return False
  return all(n%i for i in range(3, int(math.sqrt(n))+1, 2))

guess=3
primeCount=1
t=time()
while primeCount<10001:
  if isPrime(guess):
    primeCount+=1
    if primeCount==10001:break
  guess+=2
print "time",time()-t,"\nanswer",guess
