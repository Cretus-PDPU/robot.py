from matplotlib import pyplot as plt
import numpy as np
import math
from scipy import interpolate
from scipy.integrate import odeint

class parameters:
    def __init__(self):
        self.m1 = 1
        self.m2 = 1
        self.I1 = 0.1
        self.I2 = 0.1
        self.c1 = 0.5
        self.c2 = 0.5
        self.l = 1
        self.g = 9.81
        self.pause = 0.05
        self.fps =20
        self.trail_length = 50  # Number of points to store in the trail
        self.trail_data = np.zeros((self.trail_length, 2))

def cos(angle):
    return np.cos(angle)

def sin(angle):
    return np.sin(angle);

def animate(t,z,parms):
    #interpolation
    #print(type(z))
    t_interp = np.arange(t[0],t[len(t)-1],1/parms.fps)
    [m,n] = np.shape(z)
    shape = (len(t_interp),n)
    z_interp = np.zeros(shape)

    for i in range(0,n-1):
        f = interpolate.interp1d(t, z[:,i])
        z_interp[:,i] = f(t_interp)

    l = parms.l
    c1 = parms.c1
    c2 = parms.c2

    # Create a continuous line for the trail
    trail, = plt.plot(parms.trail_data[:, 0], parms.trail_data[:, 1], color='cyan', linewidth=1.5)


    #plot
    for i in range(0,len(t_interp)):
        theta1 = z_interp[i,0];
        theta2 = z_interp[i,2];
        O = np.array([0, 0])
        P = np.array([l*sin(theta1), -l*cos(theta1)])
        Q = P + np.array([l*sin(theta1+theta2),-l*cos(theta1+theta2)])
        G1 = np.array([c1*sin(theta1), -c1*cos(theta1)])
        G2 = P + np.array([c2*sin(theta1+theta2),-c2*cos(theta1+theta2)])
        parms.trail_data = np.roll(parms.trail_data, shift=1, axis=0)
        parms.trail_data[0, :] = Q

        # Update the trail line data
        trail.set_xdata(parms.trail_data[:, 0])
        trail.set_ydata(parms.trail_data[:, 1])

        pend1, = plt.plot([O[0], P[0]],[O[1], P[1]],linewidth=5, color='red')
        pend2, = plt.plot([P[0], Q[0]],[P[1], Q[1]],linewidth=5, color='blue')
        com1, = plt.plot(G1[0],G1[1],color='black',marker='o',markersize=10)
        com2, = plt.plot(G2[0],G2[1],color='black',marker='o',markersize=10)
        trail, = plt.plot(parms.trail_data[:, 0], parms.trail_data[:, 1], color='cyan', linestyle='-', linewidth=1.5)

        plt.xlim(-2,2)
        plt.ylim(-2,2)
        plt.gca().set_aspect('equal')


        plt.pause(parms.pause)
        if (i < len(t_interp)-1):
            pend1.remove()
            pend2.remove()
            com1.remove()
            com2.remove()
            trail.remove()

    #plt.show()
    plt.show(block=False)
    plt.pause(5)
    plt.close()


def double_pendulum(z,t,m1,m2,I1,I2,c1,c2,l,g):

    theta1 = z[0];
    omega1 = z[1];
    theta2 = z[2];
    omega2 = z[3];

    

    A = np.array([[M11, M12], [M21,M22]]);
    b = -np.array([C1+G1,C2+G2])
    invA = np.linalg.inv(A)
    thetaddot = invA.dot(b)
    alpha1 = thetaddot[0]
    alpha2 = thetaddot[1]

    dzdt = np.array([omega1, alpha1, omega2, alpha2]);
    return dzdt

params = parameters()

t = np.linspace(0, 10, 101)
z0 = np.array([np.pi+0.001, 0.1, 0, 0])
all_params = (params.m1,params.m2,params.I1,params.I2,params.c1,params.c2, params.l,params.g)
z = odeint(double_pendulum, z0, t, args=all_params)

animate(t,z,params)
