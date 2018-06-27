#11111111111111111111111111111111111111111111111111
#list = [x for x in range(0, 1000, 3)]
#for y in range(0, 1000, 5):
  #if y not in list:
    #list.append(y)
#print sum(list)

#alternate 1
#print sum([x for x in range(0, 1000) if x % 3 == 0 or x % 5 == 0])

#2222222222222222222222222222222222222222222222222
#def Fibonacci( n ):
#  "Finds Fib number that does not exceed n"
#  if n <= 0: return 0
#  if n > 0 and n < 3: return 1
#
#  sum = 0
#  result = 0
#  preOld = 1
#  Old = 1
#  #for x in range(1,n): #to find fib at index n
#  while result < n: #to find fib less than n
#    result = preOld + Old
#    preOld = Old
#    Old = result
#    if result % 2 == 0:
#      sum += result
#
#  #return result
#  return sum
#
#int = input("What index: ")
#print Fibonacci(int)

import math
print int(math.sqrt(2)//1)
