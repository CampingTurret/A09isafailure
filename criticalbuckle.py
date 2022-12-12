import math as m
import numpy as np
import Airfoil as A

def WebBuckle(k_s, E, nu, t, b):
    tau_cr = ((m.pi**2*k_s*E)/(12*(1-nu**2)))*(t/b)**2
    return tau_cr

def SkinBuckle(k_c, E, nu, t, b):
    sigma_cr = ((m.pi**2*k_c*E)/(12*(1-nu**2)))*(t/b)**2
    return sigma_cr

def ColumnBuckle(K, E, I, L, A):
    sigma_cr = (K*m.pi**2*E*I)/(L**2*A)
    return sigma_cr

def K_S(a,b):
    K_S = (4.982/((a/b)**2.311))+9.378
    return K_S

def K_C(a,b):
    K_c = (3.178/((a/b)**2.082))+7.173
    return K_c

def Chord(y, C_r, T, S):
    C = C_r - ((2*C_r*(1-T))/(S))*y
    return C
    

# ----- Constants ----- #
K = 4
X1 = 0.2
X2 = 0.75
C_r = 3.44
nu = 0.33
E = 68.9*10**9
Taper = 0.4
Span = 20.2

# ----- Input ----- #
Num_S = float(input("Input Number of Stringers: "))/2
Area_S = float(input("Input Stringer Area (m^2): "))
t_S = float(input("Input Stringer Thickness (mm): "))/1000
t_web = float(input("Input Thickness of Spar (mm): "))/1000
t_skin = float(input("Input Thickness of Skin (mm): "))/1000

# ----- Wing Dimensions ----- #
y1u, y1l, y2u, y2l, h1, h2, w1, w2, A = A.airfoilparameters(X1,X2)

#Uncomment next two lines, if you want to change bay size
#Y1 = float(input("Input Position of First Rib (Y1): "))    
#Y2 = float(input("Input Position of Second Rib (Y2): "))

#Comment next two lines, if you want to change bay size
Y1 = 0
Y2 = 10.1

C_1 = Chord(Y1, C_r, Taper, Span)
C_2 = Chord(Y2, C_r, Taper, Span)
a = abs(Y1-Y2)

# ----- Spar/Web ----- #
b_web1_aft = h2*C_1
b_web2_aft = h2*C_2
b_web_ave_aft = (b_web1_aft+b_web2_aft)/2
b_web1_for = h1*C_1
b_web2_for = h1*C_2
b_web_ave_for = (b_web1_for+b_web2_for)/2

b_web = max(b_web1_aft,b_web2_aft,b_web_ave_aft,b_web1_for,b_web2_for,b_web_ave_for)
k_s = K_S(a,b_web)

Tau_web = WebBuckle(k_s, E, nu, t_web, b_web)

# ----- Skin ----- #
b_skin1 = (w1*C_1)/(Num_S+1)
b_skin2 = (w1*C_2)/(Num_S+1)
b_skin_ave = (b_skin1+b_skin2)/2

b_skin = max(b_skin1, b_skin2, b_skin_ave)
k_c = K_C(a,b_skin)

Sigma_skin = SkinBuckle(k_c, E, nu, t_skin, b_skin)

# ----- Column ----- #
w_S = (Area_S)/(2*t_S)
I = (t_S*w_S**3)/12+(w_S**3*t_S)/4

Sigma_column = ColumnBuckle(K, E, I, a, Area_S)

# ----- Output ----- #
print(Tau_web, Sigma_skin, Sigma_column)


















    

