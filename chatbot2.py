import random
import sys
import os


def addnum():
    n1 = int(input("n1: "))
    n2 = int(input("n2: "))
    print(n1 + n2)


def adduser(list, usernumber):
    username = input("username=")
    password = input("password=")
    list.append((usernumber, (username, password)))
    f2 = open("user", "w")
    f2.write(str(list))
    f2.close()


def password(usernumber):
    matched = False
    f3 = open("user", "r")
    users = list(eval(f3.read()))
    for pair in range(0, len(users)):
        if usernumber == users[pair][0]:
            usn = input("username: ")
            if usn == users[pair][1][0]:
                usp = input("password: ")
                if usp == users[pair][1][1]:
                    print("WELCOME!")
                    input("press enter to continue...")
                    matched = True
    if not matched:
        print("user doesnt exist.")
        p = input("do you want to create a new one?(y/n)").lower()
        if p == "y":
            adduser(users, usernumber)
        else:
            sys.exit(0)

def addans(question):
    answer = input("ans=")
    data.append(((question,), (answer,)))
    f2 = open("data.txt", "w")
    f2.write(str(data))
    f2.close()


def quitself():
    print("bye")
    sys.exit(0)


def menu():
    os.system("cls")                                                            #
    print("hint: app = app number")                                             #
    print("add any two numbers= 1")                                             #
    print("customize= 2")                                                       #
    n = int(input("enter app number: "))
    os.system("cls")                                                            #
    if n == 1:
        addnum()
    elif n == 2:
        import options
        options.run()


usnu=input("usernumber: ")
password(usnu)
while True:
    os.system("cls")
    match = False
    userinput = input("type something: ")                                         #
    f1 = open("data.txt", "r")
    data = list(eval(f1.read()))
    for pair in range(0, len(data)):
        for questions in range(0, len(data[pair][0])):
            if userinput == data[pair][0][questions]:
                ansindex = random.randint(0, len(data[pair][1]) - 1)
                ans = data[pair][1][ansindex]
                if ans == "add":
                    addnum()
                elif ans == "quit":
                    quitself()
                elif ans == "activatemenu":
                    menu()
                elif ans == "originalchatbot":
                    import chatbot

                    chatbot.run()
                else:
                    print(ans)
                match = True
                break
        if match:
            break
    if not match:
        addans(userinput)
    input("press enter to continue... ")
