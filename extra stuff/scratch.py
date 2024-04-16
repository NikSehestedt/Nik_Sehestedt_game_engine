#this file was created by Nikolaus Sehestedt
class Number:
    on = True
        
    def multiply(a, b):
        return a*b

    def stringify(a):
        return str(a) + " is a number"
   
    d = 10
    a = (multiply(2,3))
    b = (stringify(multiply(2,3)))
    while on:
        print (a)
        print (b)
        d-=1
        if d == 0:
            on = False
    for i in range(10):
        print(multiply(2,3))
        print (stringify(multiply(2,3)))