#!/usr/bin/python

#Test Vars
a=2
b=5
c=9
d=10
e=20

#Floor Division Operator
#f=b//a
#print f

#Data type conversion (Casting)
#int(x)
#str(x)

#Dictionary (kind of a hash table)
#dict = {}
#dict['one'] = "This is one"
#dict[2]     = "This is two"
#
#tinydict = {'name': 'john', 'code':6734, 'dept':'sales'}
#print dict['one']
#print dict[2]
#print tinydict
#print tinydict.keys()
#print tinydict.values()

#Multiple vars, different values
#a, b, c = 1, 2, 'Jim'

#String type casting
#print str(a) + str(b) +"\n"
#print c

#String concatenation
#print a, b, c

#Multiple vars, same value
#a=b=c=1

#Multiple statements on one line
#import sys; x = 'foo'; sys.stdout.write(x + '\n')

#Waits for enter keypress to end program.
#raw_input("\n\nPress the enter key to exit.")

#Defining a function
#def printinfo( name, age = 35 ):
#  "This prints a passed info into this function"
#  print "Name: ", name
#  print "Age ", age
#  return; #Statement not necessary if returning nothing and at the end of the function

#Calling the function
#printinfo( age=50, name="miki" )
#printinfo( name='miki' )

#Variable args
#def printinfo( arg1, *vartuple ):
#def printinfo( *vartuple ):
#  "This prints a variable passed arguments"
#  print "Output is: "
#  print arg1
#  for var in vartuple:
#    print var
#  return;

#Calling function again
#printinfo( 10 )
#printinfo( 70, 60, 50 )

#Accepting raw_input treats input as string
#str = raw_input("Enter your input: ")
#print "Recieved input is: ", str

#Input accepts valid Py expression and evaluates them. Treats input as expression
#str2 = input("Enter your input: ")
#print "Recieved input is: ", str2

#File I/O opening a file and checking info of file
#fo = open("data.txt", "w+")
#fo = open("data.txt", "r+")
#print "Name of the file: ", fo.name
#print "Closed or not: ", fo.closed
#print "Opening mode: ", fo.mode
#print "Softspace flag: ", fo.softspace

#File I/O writing to a file
#fo.write("Python is a great language.\nYeah it's great!!\n")

#File I/O reading from a file
#str3 = fo.read(10)
#print "Read string is: ", str3

#File I/O navigating in a file
#position = fo.tell()
#print "Current file position: ", position
#Repositioning pointer to beginning of file
#position = fo.seek(0, 0)
#str3 = fo.read(6)
#print "New read string is: ", str3

#File I/O closing a file
#fo.close()
#print "Now closed?: ", fo.closed

#Meta File I/O renaming a file
#import os
#os.rename("data.txt", "pyda.txt")

