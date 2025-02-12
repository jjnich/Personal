num = int(input("Enter a number: "))
for i in range(0, num+1):
    for b in range(num-i):
        print(" ",end="")
    for j in range(i):
        print("* ",end="")
    print()
