import sys
import os


def add():
    n1 = int(input("first number: "))
    n2 = int(input("second number: "))
    print(n1 + n2)


def run():
    while True:
        userinput = input("input: ")
        os.system("cls")
        if userinput == "hi" or userinput == "hello":
            print("hello")
        elif userinput == "add":
            add()
        elif userinput == "how are you doing":
            print("i am fine")