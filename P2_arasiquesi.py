# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 15:51:09 2021

@author: USUARIO

PROJECT 2: MONTECARLO SIMULATIONS OF HARD DISKS
"""

import numpy as np
import matplotlib.pyplot as plt

########### General definitions ########### 

N = 100 # Number of particles
phi = 0.05 
delta = 0.001 #0.001; 0.003; 0.01; 0.03; 0.1; 0.3.
sigma = 1


L = np.sqrt((np.pi)*N*(sigma**2)/(4*phi)) # Box size
dt = 1 # Time-step
tf = 1000

################# Functions ################# 

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
                dx=np.abs(x2-x1)
                dy=np.abs(y2-y1)
                if dx>L/2:
                    dx=L-dx
                if dy>L/2:
                    dy=L-dy
                if np.sqrt(dx**2 + dy**2) <= sigma:
                    if [j,i] not in overlap:
                        overlap.append([i,j])
    
    return

def montecarlo(x_trial,y_trial,x_trial_bdy,y_trial_bdy):

    eps1 = np.random.uniform(0,1)
    eps2 = np.random.uniform(0,1)
    
    particle = np.random.randint(N)
    
    x_trial[particle] = x_trial[particle] + delta*(eps1-0.5)
    y_trial[particle] = y_trial[particle] + delta*(eps2-0.5)
    
    x_trial_bdy[particle] = x_trial_bdy[particle] + delta*(eps1-0.5)
    y_trial_bdy[particle] = y_trial_bdy[particle] + delta*(eps2-0.5)
    
    if x_trial_bdy[particle] > L:
        x_trial_bdy[particle]=x_trial_bdy[particle] - L
    if x_trial_bdy[particle] < 0:
        x_trial_bdy[particle]=x_trial_bdy[particle] + L
    if y_trial_bdy[particle] > L:
        y_trial_bdy[particle]=y_trial_bdy[particle] - L
    if y_trial_bdy[particle] < 0:
        y_trial_bdy[particle]=y_trial_bdy[particle] + L
        
#    print(eps1,eps2)
#    print(x[particle] + delta*(eps1-0.5))
    
    return x_trial,y_trial,x_trial_bdy,y_trial_bdy

########### Initial conditions ###########

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

print('Initial conditions: Done!')

#plt.figure(1)
#plt.scatter(x,y)
#plt.xlabel('X')
#plt.ylabel('Y')
#plt.show()

############ Montecarlo steps ############

with open('MSD.txt', 'w') as outputfile1:

    msd = np.zeros(N)
    for t in range(1,tf):
        print('Step: ',t)
        for tri in range(1,N):
            
            #print('Step: ', t, tri)
            
            x_trial = x.copy()
            y_trial = y.copy()
            
            x_trial_bdy = x_bdy.copy()
            y_trial_bdy = y_bdy.copy()
            
            montecarlo(x_trial,y_trial,x_trial_bdy,y_trial_bdy)
            
            overlapping(x,y)
            
            if len(overlap)==0:
                x=x_trial.copy()
                y=y_trial.copy()
                
            
        #for i in range(N):
        #    msd[i] = msd[i] + ((x[i]-x_IC[i])**2 + (y[i]-y_IC[i])**2)
        
        #cumulative = 0
            
        #for i in range(N):
        #    cumulative = cumulative + msd[i]/(t*dt)

        cumulative = 0
        for i in range(N):
            msd[i] = msd[i] + ((x[i]-x_IC[i])**2 + (y[i]-y_IC[i])**2)
            cumulative = cumulative + msd[i] #/(t*dt)
        
        outputfile1.write(str(cumulative/N)+'\t')

plt.figure(1)
plt.scatter(x,y)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()