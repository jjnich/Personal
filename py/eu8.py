fo = open("8eudata.txt")
big = fo.read()
fo.close()

blen = len(big)
x = 0
num = 13
#num = input("what legth of string?")
mmax = 0
while x<(blen-num):
  test = 1
  for y in range(0,num):
    test=test*int(big[x+y])
  if test>mmax:
    mmax=test
  x+=1
print mmax
