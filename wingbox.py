import numpy as np
import scipy as sp
from scipy import integrate

y = np.linspace(0.0, 10.1, 400)
t = float(input("thickness is "))
n = int(input("number of stringers on up beam "))
A_stringer = float(input("area of the stringer is "))

c_r = 3.44
b = 20.2
c = c_r - 0.6*y*2/b*c_r

h_front = 0.1122 * c
h_rear = 0.058 * c
up_beam = 0.550506 * c
low_beam = 0.550149 * c

ds = h_front + h_rear + up_beam + low_beam
enc_area = (h_front + h_rear)/2 * 0.55 * c

J = 4 * (enc_area)**2 * (t / ds)

print(J)

left_ax = t * h_front * 0.25 * c
left_a = t * h_front
left_ay = t * h_front**2 /2

right_ax = t * h_rear * 0.7 * c
right_a = t * h_rear
right_ay = t * ( 0.0152*c + h_rear/2 ) * h_rear


top_ax = (0.45*c/2 + 0.25*c) * t * up_beam
top_a = t * up_beam
top_ay = t * ( h_front-(0.0804-0.0568)*c/2)*up_beam

bot_ax = (0.45*c/2 + 0.25*c) * t * low_beam
bot_a = t * low_beam
bot_ay = t * 0.0152*c/2*low_beam




sum_ax = left_ax + right_ax + top_ax + bot_ax
sum_a = left_a + right_a + top_a + bot_a
sum_ay = left_ay + right_ay + top_ay + bot_ay

x_axis = sum_ax / sum_a
y_axis = sum_ay / sum_a


I_y_bot = 0
I_y_top = 0

top_y0 = h_front - y_axis
top_slope = (-0.0236*c) / (0.55*c)
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
bot_slope = (0.0152*c) / (0.45*c)
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

I_wingbox_l = t * h_front**3 /12 + t*h_front * (h_front/2 - y_axis)**2

I_wingbox_r = t * h_rear**3 /12 + t*h_rear * (h_rear/2 - y_axis)**2

I_wingbox_u = up_beam * t**3 /12 + up_beam * t * ( h_front-(0.0804-0.0568)*c/2-y_axis)**2

I_wingbox_d = low_beam * t**3 /12 + low_beam * t * ( 0.0152*c/2 - y_axis)**2

I_wingbox = I_wingbox_l + I_wingbox_r + I_wingbox_u + I_wingbox_d

I = I_wingbox + I_stringers
print(I)


E = 68.9 * 10**9
G = 26 * 10**9

def f(x):
    return T/(G*J)
    estimatef,errorf = sp.integrate.quad(f,0,y)

def f(x):
    return T/(G*J)
    estimatef,errorf = sp.integrate.quad(f,0,y)