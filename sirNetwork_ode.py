import random
import numpy as np
import pylab as pl 
import scipy, scipy.integrate

#####################################################################################################
############################################### SIR MODEL ###########################################
#####################################################################################################

# Parameters
a = 5			        # alpha
l = 1.0 / 5.61			# lambda
m = 1.0 / 50	      	# mu

# Initial condition
S0 = 1000
I0 = 1
R0 = 0

Y0 = [ S0, I0, R0 ]

tMax = 100

# Time vector for solution
T = scipy.linspace(0, tMax, 1001)


# This defines a function that is the right-hand side of the ODEs
def rhs(Y, t, alpha, lambd, mu):
    '''
    SIR model.
    
    This function gives the right-hand sides of the ODEs.
    '''
    
    # Convert vector to meaningful component vectors
    S = Y[0]
    I = Y[1]
    R = Y[2]
    
    N = S + I + R
    
    # The right-hand sides
    dS = mu * N - alpha * I * S / N - mu * S
    dI = alpha * I * S / N - (lambd + mu) * I
    dR = lambd * I - mu * R
    
    # Convert meaningful component vectors into a single vector
    dY = [ dS, dI, dR ]

    return dY

# Integrate the ODE
# The ODE solver over-writes the initial value.
# Also, 'args' passes parameters to right-hand-side function.
solution = scipy.integrate.odeint(rhs,
                                  Y0,
                                  T,
                                  args = (a, l, m))

print solution 
        
S = solution[:, 0]
I = solution[:, 1]
R = solution[:, 2]

N = S + I + R

# Make plots
import pylab

pylab.figure()

pylab.plot(T, S / N,
           T, I / N,
           T, R / N)

pylab.xlabel('Time')
pylab.ylabel('Proportion')

pylab.legend([ 'Susceptible', 'Infective', 'Recovered' ])

# Actually display the plot
pylab.show()