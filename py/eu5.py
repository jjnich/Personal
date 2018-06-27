from time import time

def gcd(a,b):
  if a>b:
    if b==0:
      return a
    return gcd(b,a%b)
  if b>a:
    if a==0:
      return b
    return gcd(a,b%a)

def lcm(a,b):
  return (a*b)/gcd(a,b)

maxrange = input("Max?")
t=time()
print "answer:",reduce(lcm,range(2,maxrange)),"\ntime:",time()-t
