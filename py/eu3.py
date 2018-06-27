#3333333333333333333333333333333333333333333333333
import math
#simplified
def isPrime( n ):
  if n % 2 == 0 and n > 2: return False
  return all(n%i for i in range(3, int(math.sqrt(n))+1, 2))
prime = 600851475143
for x in range(int(math.sqrt(prime)//1), 0, -1):
  if prime % x == 0 and isPrime(x): print x; break
#original method
#list = [x for x in range(int(math.sqrt(prime)//1), 0, -1) if prime % x == 0 and isPrime(x)]
#print list
#better method, no list, less memory

#original method
#def isPrime(a)
#  if n % 2 == 0 and n > 2:
#    return False
#  for i in range(3, int(math.sqrt(a) + 1, 2):
#    if a % i == 0:
#      return False
#  return True

