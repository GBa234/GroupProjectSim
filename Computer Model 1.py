import numpy as np
from matplotlib import pyplot as plt, animation
import time
import ffmpeg

xmin=0.05   #boundaries
xmax=0.15

c = 0.3     #wave speed in m/s
Nx = 1000   #number of intervals along line
Nt = 6000   #number of time intervals
T = 2   #time frame of calculation
L = 0.24     #length of line
g = 9.81 #gravity term
nu = 40000 #damping term



dx = L/Nx
dt = T/Nt
C=c*(dt/dx)
print(C)
z = [[0 for x in range(Nx)] for t in range(Nt)]  #z[t][x]

def drive(t):
    freq = 30
    ampli = 0.01
    omega = 2*np.pi*freq
    #if ((t/Nt)<1/(2*freq)):
        #f=(0.005*np.cos(omega*t*dt)-0.005)
    #else:
        #f=0
    f=(0.005*np.cos(omega*t*dt)-0.005)

    #f=0.01*(np.round(int(np.cos(0.05*t)+0.5)))
    return f

#for t=1;
def undampedfunc(z):
    for x in range (1,Nx-1):
        z[1][x]= z[0][x]-0.5*(C**2)*(z[0][x+1]-2*z[0][x]+z[0][x-1])
        z[1][int(Nx/2)]=drive(1)

    for t in range (2,Nt-1):
        for x in range (1,Nx-1):
            z[t][int(Nx/2)]=drive(t)  #a term that oscillates the half way point
            z[t+1][x]=-z[t-1][x]+2*z[t][x]+(C**2)*(z[t][x+1]-2*z[t][x]+z[t][x-1])
            #z[t][int(xmin/(L/Nx))]=0  #enforcing boundary conditions
            #z[t][int(xmax/(L/Nx))]=0


def dampedfunc(z):
    for x in range (1,Nx-1):
        z[1][x]= z[0][x]-0.5*(C**2)*(z[0][x+1]-2*z[0][x]+z[0][x-1])
        z[1][int(Nx/2)]=drive(1)

    for t in range (2,Nt-1):
        for x in range (1,Nx-1):
            z[t+1][x]=(1/(1+(nu*(dt**2))/2))*(((dt**2)*(c**2)/(dx**2))*(z[t][x+1]-2*z[t][x]+z[t][x-1])+((nu*(dt**2))/2)*z[t-1][x]+2*z[t][x]-z[t-1][x])
            z[t][int(Nx/2)]=drive(t)  #a term that oscillates the half way point
            #z[t][int(xmin/(L/Nx))]=0  #enforcing boundary conditions
            #z[t][int(xmax/(L/Nx))]=0











undampedfunc(z)
#print (z)

#for t in range (0,Nt):
    #plt.plot(x,z[t][:])
    #plt.xlim([0.09, 0.11])
    #plt.ylim([-1, 1])
    #plt.show()

sampledz=[[0 for x in range(Nx)] for t in range(1000)]

for t in range (0,1000):
    for x in range (0,Nx):
        sampledz[t][x]=z[t*(int(Nt/1000))][x]
print (sampledz)
x = []
for i in range (0,Nx):
    x.append(0+i*dx)



plt.rcParams["figure.figsize"] = [14.00, 3.50] #this section animates the plot
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()
ax.set(ylim=(-0.02, 0.02))
ax.set(xlim=(0, 0.12))
line, = ax.plot(x, sampledz[0][:], color='k', lw=2)
def animate(i):
   line.set_ydata(sampledz[i][:])
anim = animation.FuncAnimation(fig, animate, interval=0.13, frames=1000)
anim.save('503.gif')
plt.show()
