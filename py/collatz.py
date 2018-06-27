#!/usr/bin/python3

def collatz(num):
    while num != 1:
      print(num)
      if num % 2 == 0:
        num = num//2
        if num == 1:
          break
      else:
        num = 3 * num + 1
        if num == 1:
          break
    return num
print(collatz(int(input('Pick a number to collatz:'))))
