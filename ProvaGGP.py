# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 15:51:09 2021

@author: USUARIO

PROJECT 2: MONTECARLO SIMULATIONS OF HARD DISKS
"""

import numpy as np
import matplotlib.pyplot as plt

########### General definitions ########### 

N = 500 # Number of particles
phi = 0.05 
delta = 0.001 #0.001; 0.003; 0.01; 0.03; 0.1; 0.3.
sigma = 1


L = np.sqrt((np.pi)*N*(sigma**2)/(4*phi)) # Box size
dt = 1 # Time-step
tf = 500

########### Initial Configuration ########### 


def overlapping(x,y):
    
# This function checks if there is overlapping or not in the system
    
    global overlap
    overlap=[]

    for i in range(N):
        for j in range(N):
            if i!=j:
                x1=x[i]
                x2=x[j]
                y1=y[i]
                y2=y[j]
                dx=x2-x1
                dy=y2-y1
                if abs(dx)>L/2:
                    dx=L-abs(dx)
                else:
                    dx = abs(dx)
                if abs(dy)>L/2:
                    dy=L-abs(dy)
                else:
                    dy=abs(dy)
                if np.sqrt(dx**2 + dy**2) <= sigma:
                    if [j,i] not in overlap:
                        overlap.append([i,j])
    
    return

x = np.random.uniform(0, L, size=(N))
y = np.random.uniform(0, L, size=(N))

overlapping(x,y)

while len(overlap) != 0:
    print('Overlapping: ',len(overlap), overlap)
    for i in overlap: #[:int(len(overlap)/2)]:
        np.random.seed(None)
        x[i[0]]=np.random.randint(L)
        y[i[0]]=np.random.randint(L)
    overlapping(x,y)

x_IC = x.copy()
y_IC = y.copy()

x_bdy = x.copy()
y_bdy = y.copy()

plt.figure(1)
plt.scatter(x,y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Initial Conditions')
plt.show()
print('Initial conditions: Done!')

with open('MSD_0p001.txt', 'w') as outputfile1:
    msd = np.zeros(N)
    for t in range(tf):
        print(t)
        for i in range(N):
            p_id = np.random.randint(N)
            eps1 = np.random.uniform(0,1)
            eps2 = np.random.uniform(0,1)
            
            xtrial = x[p_id]+delta*(eps1-0.5)
            ytrial = y[p_id]+delta*(eps2-0.5)
            xtrial_bdy = x_bdy[p_id]+delta*(eps1-0.5)
            ytrial_bdy = y_bdy[p_id]+delta*(eps2-0.5)
            
            if xtrial_bdy > L:
                xtrial_bdy=xtrial_bdy - L
            if xtrial_bdy < 0:
                xtrial_bdy=xtrial_bdy + L
            if ytrial_bdy > L:
                ytrial_bdy=ytrial_bdy - L
            if ytrial_bdy < 0:
                ytrial_bdy=ytrial_bdy + L
            
            #Comprovem el solapament 
            count = 0
            
            for j in range(N):
                if j!=p_id:
                    dx = x[i]-xtrial_bdy
                    dy = y[i]-ytrial_bdy
                    if abs(dx)>L/2:
                        dx=L-abs(dx)
                    else:
                        dx = abs(dx)
                    if abs(dy)>L/2:
                        dy=L-abs(dy)
                    else:
                        dy=abs(dy)
                    if np.sqrt(dx**2 + dy**2) > sigma:
                        count = count+1
                    else:
                        break
                    if count == N-1:
                        x[p_id]=xtrial
                        y[p_id]=ytrial
                        x_bdy[p_id]=xtrial_bdy
                        y_bdy[p_id]=ytrial_bdy
        
        cumulative = 0
        for i in range(N):
            
            msd[i] = ((x[i]-x_IC[i])**2 + (y[i]-y_IC[i])**2) #+msd[i]
            cumulative = cumulative + msd[i]  #/(t*dt)
            
        outputfile1.write(str(cumulative/N)+'\t')
        
plt.figure(2)
plt.scatter(x,y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Final Conditions')
plt.show()
