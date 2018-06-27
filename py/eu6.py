from time import time

def susq(mmax):
  y=0
  for x in range(1,mmax):
    y+=x**2
  return y

num = input("What max should we use?")
#num=100
num+=1 #using this as a non-inclusive max for ranges

#first method
t1=time()
sumofsquares = susq(num)
squareofsums = sum(range(1,num))**2
answer = squareofsums - sumofsquares
print "answer is",answer,"\ttime is",time()-t1

#second method
t2=time()
answer2=sum([x for x in range(num)])**2 - sum([x**2 for x in range(num)])
print "answer is",answer2,"\ttime is",time()-t2

#second method is better.
