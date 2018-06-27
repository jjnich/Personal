import math

#pythagorean triplet = a^2+b^2=c^2
#one exists where a+b+c=1000
#find product abc

it=0

x = 0
y = 0
flag = 0
mmax = 1000
#mmax = 12
for b in range(1,mmax):
  for a in range(1,b):
    #it=it+1
    c = mmax-a-b
    if a**2 + b**2 == c**2:
      print "a=",a,"b=",b,"c=",c
      print "a * b * c = ",a*b*c
    #  print "iteration",it
      flag = 1
      break
  if flag == 1: break
