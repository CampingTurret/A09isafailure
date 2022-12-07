import numpy as np
import scipy as sp
import math as m
import os
from matplotlib import pyplot as plt
from scipy import integrate

from main import sum_shear1,sum_moment1,torque_dist1,sum_shear2,sum_moment2,torque_dist2,sum_shear3,sum_moment3,torque_dist3

sum_shear1=sum_shear1[0:400]
sum_shear2=sum_shear2[0:400]
sum_shear3=sum_shear3[0:400]

sum_moment1=sum_moment1[0:400]
sum_moment2=sum_moment2[0:400]
sum_moment3=sum_moment3[0:400]

torque_dist1=torque_dist1[0:400]
torque_dist2=torque_dist2[0:400]
torque_dist3=torque_dist3[0:400]

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

l_top=w1*c
l_bot=w2*c

area_skin = (h_front+h_rear)*t_spar+(up_beam+low_beam)*t
area = (h_front+h_rear)*t_spar+(up_beam+low_beam)*t+A_stringer*n
volume = 2*(np.trapz(area,y)) # Full span volume
print("\nStructure Volume:",str(volume),"[m^3]")
print("Structure Weight:",str(volume*2700),"[kg]\n")

# print(h_front)
# print(h_rear)

ds = h_front + h_rear + up_beam + low_beam
enc_area = (h_front + h_rear)/2 * (X2-X1) * c
J = 4 * (enc_area)**2 / (h_front/t_spar + h_rear/t_spar + up_beam/t + low_beam/t)

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

x_ctr = (x_axis/c)[0]
y_ctr = (y_axis/c)[0]

# print(x_ctr)
# print(y_ctr)

# print(x_axis)

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

# print(bot_y0)
# print("\n")

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

V1 = sum_shear1
V2 = sum_shear2
V3 = sum_shear3
T1 = torque_dist1
T2 = torque_dist2
T3 = torque_dist3
M1 = sum_moment1
M2 = sum_moment2
M3 = sum_moment3

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

# def vstress(V): # DEPRECATED
    
    up_y0= h_front-y_axis
    low_y0= -y_axis
    
    Bc=area_skin/4
    Bs=A_stringer
    
    a_dist = np.zeros((400,n+2))
    
    a_dist[:,0]=Bc
    a_dist[:,n+1]=Bc
    
    for i in range(n):
        a_dist[:,i+1]=Bs
        
    # print(a_dist)
    
    up_end = up_y0+(X2-X1)*c*top_slope
    bot_end = low_y0+(X2-X1)*c*bot_slope
    
    y_loc_top = np.linspace(up_y0,up_end,n+2)
    y_loc_top = y_loc_top.transpose()
    y_loc_bot = np.linspace(low_y0,bot_end,n+2)
    y_loc_bot = y_loc_bot.transpose()
    
    top_sum=np.sum((y_loc_top*a_dist),axis=1)
    bot_sum=np.sum((y_loc_bot*a_dist),axis=1)
    
    funcsum = top_sum+bot_sum
    k=-(V/I)
    
    qb = k*funcsum
    
    print(qb)
    
    return

# def qshear(V):
    
    # Geometric Calculations
    up_y0 = h_front - y_axis
    low_y0 = -y_axis
    
    upsl = np.tan(top_slope)
    dnsl = np.tan(bot_slope)
    
    n_up_y0 = up_y0+(x_axis-X1*c)*upsl
    n_low_y0 = low_y0+(x_axis-X1*c)*bot_slope
    
    up_end = up_y0+(X2-X1)*c*top_slope
    bot_end = low_y0+(X2-X1)*c*bot_slope
    
    # Calculating qb
    
    int1 = (X1*c-x_axis)*(low_y0-up_y0)*t_spar
    int2 = 0.5*bot_slope*((x_axis-X1*c)**2+(X2*c-x_axis)**2)*t
    int3 = (X2*c-x_axis)*(up_y0-low_y0)*t_spar
    int4 = 0.5*top_slope*((X2*c-x_axis)**2+(x_axis-X1*c)**2)*t
    
    sum_int=int1+int2+int3+int4
    k=-(V/I)
    qb=k*sum_int
    
    # Calculating qs - cut at top left corner
    
    r2 = h_front
    r3 = (X2-X1)*c
    
    q2=k*int2
    q3=k*int3
    
    qs = (r2*q2+r3*q3)/(-2*enc_area)
    
    # print(qs)
    
    q=qb+qs 
    # print(q)
    
    return q

def fq1(s,k):
    f=k*t_spar*((s)**2)/2
    return f

def fq2(s,k):
    f=k*t*(h_front/2*s-(s**2)/2*(h_front/2-h_rear/2)/w1)
    return f

def fq3(s,k,q2):
    f=k*t_spar*(h_rear/2*s-(s**2)/2)+q2
    return f

def qshear(V):
    
    k=-(V/I)
    
    q01=fq1(h_front/2,k)
    q12=fq2(w1,k)
    q23=fq3(0,k,q12)
    
    # print(q12)
    
    int1=np.zeros(400)
    int2=np.zeros(400)
    int3=np.zeros(400)
    
    for i in range(400): # Calculate qs0
        int1[i]=sp.integrate.quad(lambda s: k[i]*t_spar*(s**2)/2*(x_axis[i]-X1*c[i]),0,h_front[i]/2)[0]
        
        h1=h_front[i]/2-(h_front[i]/2-h_rear[i]/2)/((X2-X1)*c[i])*(x_axis[i]-X1*c[i])
        int2[i]=sp.integrate.quad(lambda s: k[i]*t*((h_front[i]/2)*s-(s**2)/2*((h_front[i]/2-h_rear[i]/2)/l_top[i]))*h1*(X2-X1)*c[i]/l_top[i],0,l_top[i])[0]
        
        int3[i]=sp.integrate.quad(lambda s: k[i]*t_spar*(h_rear[i]/2*s-(s**2)/2)+q12[i],0,h_rear[i]/2)[0]
    
    qs0=-2*(int1+int2+int3)/enc_area
    
    qa = q01+qs0
    qb = q12+qs0
    qc = q23+qs0
    
    # print(qa)
    # print(qb)
    # print("\n")
    
    qa_max=max(abs(qa))
    qb_max=max(abs(qb))
    
    q=(max(qa_max,qb_max))
    
    return q

q1=qshear(V1)
q2=qshear(V2)
q3=qshear(V3)

theta1,v1=mov(T1,M1)
theta2,v2=mov(T2,M2)
theta3,v3=mov(T3,M3)

##### Internal Stresses

# Shear V

vtau1 = q1/(min(t,t_spar))/10**6
vtau2 = q2/(min(t,t_spar))/10**6
vtau3 = q3/(min(t,t_spar))/10**6

# Bending Mx

sigma_y1 = (M1 * h1/2)/I
sigma_max1 = round(max(sigma_y1)/10**6, 2)

sigma_y2 = (M2 * h1/2)/I
sigma_max2 = round(max(sigma_y2)/10**6, 2)

sigma_y3 = (M3 * h1/2)/I
sigma_max3 = round(max(sigma_y3)/10**6, 2)

# Torsion T

tau1 = T1 / (2*enc_area*t)
tau_max1 = round(min(tau1)/10**6, 2)-vtau1

tau2 = T2 / (2*enc_area*t)
tau_max2 = round(min(tau2)/10**6, 2)-vtau2

tau3 = T3 / (2*enc_area*t)
tau_max3 = round(min(tau3)/10**6, 2)-vtau3

print("### Positive - Bending Limiting ###\n")

print('Angle of twist is', np.sum(theta1), '[rad]')
print('Deflection is', np.sum(v1), '[m]')
print('Maximum normal stress due to bending is',sigma_max1,'[MPa]')
print('Maximum shear stress due to torsion is',tau_max1,'[MPa]\n')
print('Tau contribution due to shear: ',-1*vtau1,'[MPa]\n')

print("### Zero - Torsion Limiting ###\n")

print('Angle of twist is', np.sum(theta2), '[rad]')
print('Deflection is', np.sum(v2), '[m]')
print('Maximum normal stress due to bending is',sigma_max2,'[MPa]')
print('Maximum shear stress due to torsion is',tau_max2,'[MPa]\n')
print('Tau contribution due to shear: ',-1*vtau2,'[MPa]\n')

print("### Negative ###\n")

print('Angle of twist is', np.sum(theta3), '[rad]')
print('Deflection is', np.sum(v3), '[m]')
print('Maximum normal stress due to bending is',sigma_max3,'[MPa]')
print('Maximum shear stress due to torsion is',tau_max3,'[MPa]\n')
print('Tau contribution due to shear: ',-1*vtau3,'[MPa]\n')

def movPlot(v,theta,lc,design):

    deflection = np.linspace(0.0, 10.1, 400)
    for i in range(y.size):

        deflection[i] = np.sum(v[0:i])

    # deflection=deflection*-1

    twist = np.linspace(0.0, 10.1, 400)
    for i in range(y.size):

        twist[i] = np.sum(theta[0:i])

    twist=twist*180/np.pi

    fig, ax1 = plt.subplots(figsize=(10,5))
    ax2 = ax1.twinx()

    plt.xlim([0,11])
    plt.xticks(np.arange(0, 12, 1.0))
    plt.grid(True, color='0.9')
    
    ax1.axhline(y=0, color='black', linewidth=0.5, linestyle=(0,(5,5)), xmax=10.1/11)
    
    lns1 = ax1.plot(y,deflection,color='black',label='Deflection [m]')
    lns2 = ax2.plot(y,twist,color='orange',label='Twist [deg]')
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="upper right")

    ax1.set_ylim([0.5,-4])
    ax2.set_ylim([-10,0.5])
    ax1.set_xlabel('y [m]')
    ax1.set_ylabel('deflection [m]')
    ax2.set_ylabel('twist [deg]')
    
    # ax1.legend(('Deflection [m]'), loc="lower left")
    # ax2.legend(('Twist [deg]'), loc="lower right")

    plt.title('Deflection and Twist of Design '+str(design)+' Under LC'+str(lc), fontweight='bold', y=1.05)

    path=os.path.join('figures/deflections/design'+str(design)+'/')
    if os.path.exists(path) == False:
        os.mkdir(path)
    plt.savefig(path+'/design'+str(design)+'lc'+str(lc)+'.jpg')

    # twi = plt.figure(figsize=(10,5))
    
movPlot(v1,theta1,26,3)
movPlot(v2,theta2,18,3)
movPlot(v3,theta3,15,3)

'''
Second value in each function is the loading case, third value in each is the design number.
Don't touch the loading case numbers, they are in a different order from the document (18 and 15 switched in the code).
Order running from main: 26-18-15
Change the design number depending on what geometric values you are inputting.
'''




    
    


