def run():
    import os

    run = True
    while run:
        print("black= 0")
        print("grey= 8")
        print("blue= 1")
        print("light blue= 9")
        print("green= 2")
        print("light green= A")
        print("aqua= 3")
        print("light aqua= B")
        print("red= 4")                                        #
        print("light red= C")
        print("purple= 5")
        print("light purple= D")
        print("yellow= 6")
        print("light yellow= E")
        print("white= 7")
        print("bright white= F")
        bg = input("background color: ")
        fg = input("foreground color: ")
        os.system("color " + bg + fg)
        satisfied = input("is this what you wanted?(y/n)").lower()
        if satisfied == "y":
            run = False
        else:
            os.system("color")