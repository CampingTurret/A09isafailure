import numpy as np
import math as m

#X1 = float(input("Input first x-coordinate,(X1): "))
#X2 = float(input("Input second x-coordinate,(X2): "))
X1 = 0.2
X2 = 0.75

def airfoilparameters(X1, X2):
    data = []
    with open("NACA.txt") as data_points:
        for line in data_points.readlines():
            data.append(np.fromstring(line,sep=' '))
    data_array = np.array(data)

    Xu = np.flip(data_array[0:51,0]) 
    Xl = data_array[51:102,0]
    Yu = np.flip(data_array[0:51,1])
    Yl = data_array[51:102,1]

    y1u = np.interp(X1, Xu, Yu)
    y1l = np.interp(X1, Xl, Yl)
    y2u = np.interp(X2, Xu, Yu)
    y2l = np.interp(X2, Xl, Yl)

    h1 = abs(y1u - y1l)
    h2 = abs(y2u - y2l)
    w1 = m.sqrt((y1u-y2u)**2+(X1-X2)**2)
    w2 = m.sqrt((y1l-y2l)**2+(X1-X2)**2)
    A = ((h1+h2)/2)*abs(X2-X1)

    return y1u, y1l, y2u, y2l, h1, h2, w1, w2, A

y1u, y1l, y2u, y2l, h1, h2, w1, w2, A = airfoilparameters(X1,X2)
#print("\n")
#print("--------------- Results ---------------")
#print("Height at X1 is", h1)
#print("Height at X2 is", h2)
#print("Upper diagonal length is", w1)
#print("Lower diagonal length is", w2)
#print("Wing box area is", A)
#print(y1u, y1l, y2u, y2l)




    
        
