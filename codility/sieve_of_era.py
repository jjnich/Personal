import time
import math

def sieve(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    i = 2
    while (i * i <= n): # goes up to sqrt(n) so it's fast
        if sieve[i]:
            k = i * i
            while k <= n:
                sieve[k] = False
                k += i
        i += 1
    return sieve

def sieve2(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, n + 1): # goes up to n+1 so it's not fast
        if sieve[i]:
            k = i * i
            while k <= n:
                sieve[k] = False
                k += i
    return sieve

def sieve3(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(n)) + 1): # up to sqrt(n) so faster, but requires math.sqrt so it's not as fast.
        if sieve[i]:
            k = i * i
            while k <= n:
                sieve[k] = False
                k += i
    return sieve

if __name__ == "__main__":
    starttime = time.time()
    primes = sieve3(1000000)
    prime_list = [i for i in range(len(primes)) if primes[i]]
    endtime = time.time()
    print("Execution time: ", endtime - starttime)
    print(len(prime_list))
    # print(prime_list)
    # for i in range(len(primes)):
    #     if primes[i]:
    #         print("prime: ",i)
