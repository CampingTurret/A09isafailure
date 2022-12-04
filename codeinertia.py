import numpy as np
import scipy as sp
import math as m
from scipy import integrate

from main import sum_moment1,torque_dist1,sum_moment2,torque_dist2

sum_moment1=sum_moment1[0:400]
torque_dist1=torque_dist1[0:400]
sum_moment2=sum_moment2[0:400]
torque_dist2=torque_dist2[0:400]

X1 = 0.2      # float(input("X-coordinate of Leading Spar X1: "))
X2 = 0.75      # float(input("X-coordinate of Trailing Spar X2: "))

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

    return h1, h2, w1, w2, A

h1, h2, w1, w2, A = airfoilparameters(X1,X2)

y = np.linspace(0.0, 10.1, 400)
t = float(input("Wingbox Thickness t [m]: "))
t_spar = float(input("Spar Thickness t_spar [m]: "))
n = int(input("Number of Stringers: "))
A_stringer = float(input("Stringer Area [m^2]: "))

cr = 3.44
b = 20.2
E = 68.9 * 10**9
G = 26 * 10**9
c = cr - 0.6*y*2/b*cr

h_front = h1 * c
h_rear = h2 * c
up_beam = w1 * c
low_beam = w2 * c

area = (h_front+h_rear)*t_spar+(up_beam+low_beam)*t+A_stringer*n
volume = 2*(np.trapz(area,y)) # Full span volume
print("\nStructure Volume:",str(volume),"[m^3]")
print("Structure Weight:",str(volume*2800),"[kg]\n")

# print(h_front)
# print(h_rear)

ds = h_front + h_rear + up_beam + low_beam
enc_area = (h_front + h_rear)/2 * (X2-X1) * c
J = 4 * (enc_area)**2 * (t / ds)

left_ax = t_spar * h_front * X1 * c # Centroid stuff
left_a = t_spar * h_front # Area
left_ay = t_spar * h_front**2 /2

right_ax = t_spar * h_rear * X2 * c
right_a = t_spar * h_rear
right_ay = t_spar * ( ((low_beam**2-((X2-X1)*c)**2)**0.5) + h_rear/2 ) * h_rear

top_ax = ((X2-X1)*c/2 + X1*c) * t * up_beam
top_a = t * up_beam
top_ay = t * ( h_front-((up_beam**2-((X2-X1)*c)**2)**0.5)/2)*up_beam

bot_ax = ((X2-X1)*c/2 + X1*c) * t * low_beam
bot_a = t * low_beam
bot_ay = t * ((low_beam**2-((X2-X1)*c)**2)**0.5)/2*low_beam

sum_ax = left_ax + right_ax + top_ax + bot_ax
sum_a = left_a + right_a + top_a + bot_a
sum_ay = left_ay + right_ay + top_ay + bot_ay

x_axis = sum_ax / sum_a
y_axis = sum_ay / sum_a

I_y_bot = 0
I_y_top = 0

top_y0 = h_front - y_axis
top_slope = -((up_beam**2-((X2-X1)*c)**2)**0.5) / ((X2-X1)*c)
top_end = top_y0 + top_slope *c
top_stringer_distance = (top_y0 - top_end) /(n-1)

top_dist = top_y0

m = n
while m > 0.1 :
    I_stringer_top = A_stringer * top_dist**2
    I_y_top += I_stringer_top

    top_dist -= top_stringer_distance
    m = m-1

bot_y0 = -y_axis
bot_slope = ((low_beam**2-((X2-X1)*c)**2)**0.5) / ((X2-X1)*c)
bot_end = bot_y0 + bot_slope *c
bot_stringer_distance = (bot_y0 - bot_end) /(n-1)

bot_dist = bot_y0

l = n
while l > 0.1 :
    I_stringer_bot = A_stringer * bot_dist**2
    I_y_bot += I_stringer_bot

    bot_dist -= bot_stringer_distance
    l = l-1

I_stringers = I_y_top + I_y_bot

I_wingbox_l = t_spar * h_front**3 /12 + t_spar*h_front * (h_front/2 - y_axis)**2

I_wingbox_r = t_spar * h_rear**3 /12 + t_spar*h_rear * (h_rear/2 - y_axis)**2

I_wingbox_u = up_beam * t * ( h_front-((up_beam**2-((X2-X1)*c)**2)**0.5)/2-y_axis)**2

I_wingbox_d = low_beam * t * ( ((low_beam**2-((X2-X1)*c)**2)**0.5)/2 - y_axis)**2

I_wingbox = I_wingbox_l + I_wingbox_r + I_wingbox_u + I_wingbox_d

I = I_wingbox + I_stringers

T1 = torque_dist1
T2 = torque_dist2
M1 = sum_moment1
M2 = sum_moment2

def mov(T,M):

    dtheta = T / (G*J)
    theta = 10.1/400 * dtheta

    ddv = - M / (E*I)
    dvs = 10.1/400 * ddv
    dv = np.linspace(0.0, 0.0, 400)

    for n in range(399):
        if n == 0:
            dv[n] = dvs[n]
            n = n + 1
        else:
            dv[n] = dv[n-1] + dvs[n]
            n= n + 1

    v = 10.1/400 * dv
    
    return theta,v

theta1,v1=mov(T1,M1)

theta2,v2=mov(T2,M2)

##### Internal Stresses

# Bending Mx

sigma_y1 = (M1 * h1/2)/I
sigma_max1 = round(max(sigma_y1)/10**6, 2)

sigma_y2 = (M2 * h1/2)/I
sigma_max2 = round(max(sigma_y2)/10**6, 2)

# Torsion T

tau1 = T1 / (2*enc_area*t)
tau_max1 = round(min(tau1)/10**6, 2)

tau2 = T2 / (2*enc_area*t)
tau_max2 = round(min(tau2)/10**6, 2)

# print(sigma_y)
# print(I)

print("### Bending Limiting ###\n")

print('Angle of twist is', np.sum(theta1), '[rad]')
print('Deflection is', np.sum(v1), '[m]')
print('Maximum normal stress due to bending is',sigma_max1,'[MPa]')
print('Maximum shear stress due to torsion is',tau_max1,'[MPa]\n')

print("### Torsion Limiting ###\n")

print('Angle of twist is', np.sum(theta2), '[rad]')
print('Deflection is', np.sum(v2), '[m]')
print('Maximum normal stress due to bending is',sigma_max2,'[MPa]')
print('Maximum shear stress due to torsion is',tau_max2,'[MPa]')