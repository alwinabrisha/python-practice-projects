a = input("enter the password:")

up = 0
lo = 0
dg = 0
sp = 0

if (len(a)>7):
    for i in a:
        if(a.isupper()):
            up=up+1
        elif(a.islower()):
            lo=lo+1
        elif(a.isdigit()):
            dg=dg+1
        else:
            sp=sp+1
    if(up>0 and lo>0 and dg>0 and sp>0):
        print("your passwords is strong")
    else:
        print("your passwords is strong")
else:
    print("your password does not contain enough number of values...")
