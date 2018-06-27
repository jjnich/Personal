#!/usr/bin/python

def collatz(num):
    while num != 1:
        if num % 2 == 0:
            num = num//2
            print(num)
            collatz(num)
        else:
            num = 3 * num + 1
            collatz(num)
    return num
collatz(input('Pick a number to Collatz: "))
