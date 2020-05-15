import sqlite3

conn = sqlite3.connect("test.db")
print("opened")
conn.execute("""CREATE TABLE IF NOT EXISTS QandA
(
QUESTION TEXT NOT NULL,
ANSWER TEXT NOT NULL
);
""")
print("created")


# step1
def restorebackup():
    resetQandA()
    f1 = open("data.txt", "r")
    mylist = list(eval(f1.read()))
    for q in range(0, len(mylist)):
        for w in range(0, len(mylist[q][0])):
            for e in range(0, len(mylist[q][1])):
                conn.execute("""INSERT INTO QandA (QUESTION,ANSWER) VALUES (?,?);""",
                             [str(mylist[q][0][w]), str(mylist[q][1][e])])


import random
import sys
import os


def resetQandA():
    conn.execute("DELETE FROM QandA")





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
    conn.execute("INSERT INTO QandA (QUESTION,ANSWER) VALUES(?,?)", (question, answer))


def save():
    c2 = conn.execute("SELECT * FROM QandA")
    c2 = list(c2)
    f2 = open("data.txt", "w")
    f2.write(str(c2))
    f2.close()


def quitself():
    print("bye")
    save()
    conn.commit()
    print("sucessful")
    conn.close()
    sys.exit(0)


def menu():
    os.system("cls")  #
    print("hint: app = app number")  #
    print("add any two numbers= 1")  #
    print("customize= 2")  #
    n = int(input("enter app number: "))
    os.system("cls")  #
    if n == 1:
        addnum()
    elif n == 2:
        import options
        options.run()


restorebackup()
# usnu=input("usernumber: ")
# password(usnu)
while True:
    usi = input("?:").strip()
    cursor = conn.execute(f"""SELECT ANSWER FROM QandA WHERE QUESTION LIKE "(?)" """, (usi))
    # print(list(cursor))
    ans = list(cursor)
    ansindex = random.randint(0, len(ans) - 1)
    ans = str(ans[ansindex][0])
    print(ans)
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

# step2
# import texttable
#
# t = texttable.Texttable()
# w = [["question", "answer"]] + list(cursor)
# t.add_rows(w)
# print(t.draw())
