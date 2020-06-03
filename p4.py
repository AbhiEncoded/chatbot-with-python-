import random
import sys
import mysql.connector
from datetime import datetime
import os
import pprint

#i added .strip() to the end of every input statement

def restorebackup():
    cursor.execute("""create table if not exists qanda (
    question text not null,
    answer text not null
    )""")
    f1 = open("Documents\\data.txt", "r")   #always give full path for any external files
    mylist = list(eval(f1.read()))
    for q in range(0, len(mylist)):
        cursor.execute("""INSERT INTO qanda (question,answer) VALUES (%s,%s);""",
                       [str(mylist[q][0]), str(mylist[q][1])])
        print(str(mylist[q][0]), str(mylist[q][1]))
    f1.close()
    conn.commit()


def login():
    cursor.execute("""create table if not exists users (
	usernumber int not null,
	name char(200) not null,
	password char(200) not null,
	color text,
	admin text,
	primary key (usernumber,name,password) 
	)""")
    usernumber = input("usernumber: ").strip()
    username = input("username: ").strip()
    password = input("password: ").strip()
    try:
        cursor.execute("select autoclear,color,admin from users where usernumber like %s and name like %s and password like %s",
                       (usernumber, username, password))
        results = cursor.fetchall()  #
        autoclear,color, admin = results[0]  #
        if autoclear== None:
            autoclear=False
        return usernumber, username, password, color, admin,autoclear
    except Exception as e:
        print(e)
        print("user not found")
        newuser = input("do you want to create a new user?(y/n)").strip()
        if newuser == "y":
            adduser(usernumber, username, password)
        if newuser == "n":
            print("bye")
            sys.exit(0)


def adduser(usernumber, username, password):
    print("adding user")
    admin = "no"
    color = " "
    autoclear=0
    try:
        cursor.execute("INSERT INTO users (usernumber,name,password,color,admin,autoclear) values (%s,%s,%s,%s,%s,%s)",
                       (usernumber, username, password, color, admin,autoclear))
        print("user added")
    except :
        print("duplicate user")
        login()

def addadmin():                                          #to add other admins
    usernumber=input("usernumber: ").strip()
    username=input("username: ").strip()
    password=input("password: ").strip()
    print("adding user")
    admin = "yes"
    color = " "
    try:
        cursor.execute("INSERT INTO users (usernumber,name,password,color,admin) values (%s,%s,%s,%s,%s)",
                       (usernumber, username, password, color, admin))
        print("user added")
    except :
        print("duplicate user")
        login()


def addtohistory(usernumber, question):
    cursor.execute("""create table if not exists history(
    time text not null,
	question text not null,
	usernumber text not null)""")
    time = datetime.now()
    cursor.execute("INSERT INTO history (time,question,usernumber) values (%s,%s,%s)", (time, question, usernumber))


def menu():
    os.system("cls")  
    print("hint: app = app number")  
    print("add any two numbers= 1")  
    print("change color theme = 2")  #changed options
    print("autoclear toggle = 3")
    n = int(input("enter app number: "))  #dont add .strip here as it will give error
    os.system("cls")  
    if n == 1:
        addnum()
    elif n == 2:
        import options
        color = options.run()
        cursor.execute("update users set color=%s where usernumber like %s and name like %s and password like %s",
                       (color,usernumber, username, password))
        os.system("color" + " " + str(color))
        print("color changed")
        conn.commit()
    elif n==3:
        global autoclear
        autoclear = not autoclear   # toggle autoclear
        cursor.execute("update users set autoclear=%s where usernumber like %s and name like %s and password like %s",
                       (autoclear,usernumber, username, password))
        print("updated")

def quitself():
    print("bye")
    conn.commit()
    print("sucessful")
    conn.close()
    os.system("color")
    sys.exit(0)


def addans(question):
    answer = input("ans=").strip()
    cursor.execute("INSERT INTO qanda (question,answer) VALUES(%s,%s)", (question, answer))
    conn.commit()


def resettable():
    print("resetting..")
    cursor.execute("drop table qanda")   #only for qanda
    restorebackup()


def savetobackup():
    print("saving...")
    cursor.execute("select * from qanda")
    f1 = open("Documents\\data.txt", "w") #always give full path for external files
    f1.write(str(cursor.fetchall()))
    f1.close()
    print("saved")


def addnum():
    n1 = input().strip()
    n2 = input().strip()
    print(n1 + n2)


def viewhistory():
    cursor.execute("select * from history where usernumber like %s order by time desc")
    pprint.pprint(cursor.fetchall())


conn = mysql.connector.connect(host="localhost", user="root", password="root", db="chatbot")  #
print("connected")
cursor = conn.cursor()


username, usernumber, password, color, admin,autoclear = login()
print(username, usernumber, password, color, admin,autoclear)
os.system("color" + " " + str(color))
while True:
    if autoclear==1:
        os.system("cls")  # to clearscreen everytime
    usi = input(": ").strip(""" \n\r\t!@#$%^&*():'";<?>,./~` """)  #to clear all special characters
    addtohistory(usernumber, usi)  # add all new searches to history
    try:
        cursor.execute("""select answer from qanda where question like %s """, (usi,))
        ans = cursor.fetchall()
        ansindex = random.randint(0, len(ans) - 1)
        ans = ans[ansindex][0]
        if ans == "add":
            addnum()
        if ans=="cls":
            os.system("cls")
        elif ans == "quit":
            quitself()
        elif ans == "activatemenu":
            menu()
        elif ans == "customize":
            import options

            color = options.run()
            cursor.execute("update users set color=%s where usernumber like %s and name like %s and password like %s",
                           (color,usernumber, username, password))
            os.system("color" + " " + str(color))
            print("color changed")
            conn.commit()

        elif ans == "originalchatbot":
            import chatbot

            chatbot.run()
        else:
            if admin == "yes":
                if ans == "sql":
                    while True:
                        try:
                            sql = input("sql> ").strip()
                            if sql == "\\q":  # press \q to exit sql mode
                                break
                            else:
                                cursor.execute(sql)
                                print(cursor.fetchall())
                        except Exception as e:
                            print(e)
                elif ans == "resettable":  # these are the extra commands
                    resettable()
                elif ans == "restorebackup":
                    restorebackup()
                elif ans=="addadmin":
                    addadmin()
                elif ans == "dosave":
                    savetobackup()
                else:
                    print(ans)                  #if not admin and ans not match
            else:
                print(ans)
    except Exception as e:
        print(e)
        if admin == "yes":
            d = input("do you want to add a answer?(y/n)").strip()
            if d == "y":
                addans(usi)
                conn.commit()
    if autoclear==1:
        input("press enter to continue").strip()
print("closed")

conn.close()
