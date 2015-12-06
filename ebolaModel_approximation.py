import random
import numpy as np
import pylab as pl 

"""
 'r' = red
 'g' = green
 'b' = blue
 'c' = cyan
 'm' = magenta
 'y' = yellow
 'k' = black
 'w' = white
"""
#####################################################################################################
############################################### SIR MODEL ###########################################
#####################################################################################################

## Initial conditions
S = 1000	# Number of susceptibles
I = 1		# Seed the outbreak with one infectious individual
R = 0 		# No one has yet recovered

N = float(S+I+R)

## Simulation clock 
t = 0

## Transmission parameters

# Normal infectivity (alpha)
a = np.random.uniform(0.00, 1.00, [1,100])		# Array of 100 random floats from [0.00, 1.00]
a = np.linspace(0.00, 1.0, num=100) 			# Array of 100 floats sorted in ascending order 

# Probably of recovering at each time step (lambda), 1/l = average duration of illness
l = np.random.uniform(0.00, 1.00, [1,100])		
l = np.linspace(0.00, 1.0, num=100) 			

a = .09
l = .05

susceptibles = []	# Stores number of susceptible individuals at each step 
infected = []		# Stores number of infected individuals 
recovered = []		# Stores number of recovered individuals
newlyInfected = []	# Records the number of newly infected people at each step 

# Each list element represents the S, I, and R values for a single time step
susceptibles.append(S)
infected.append(I)
recovered.append(R)
newlyInfected.append(0)

# For as long as there are still infectious individuals, this loop will continue running
while I > 0:

	# No one has yet been infected
	newI = 0

	for i in range(S):

		# If we use a frequency dependent transmission process: random val is in range [0, 1)
		# if random.random() < a*(I/N):
		# 	newI += 1

		# If we use a density dependent transmission process: 
		if random.random() < a*I:
			newI += 1

	# Number of individuals that recover at each time step
	recoverI = 0
	for i in range(I):
		if random.random() < l:
			recoverI += 1

	""" 
	All plausible events are assumed to occur in a step simultaneously. 
	Susceptible individuals are infected as infected individuals recover. 
	"""
	S -= newI 							
	I += (newI - recoverI)
	R += recoverI 

	# Each list element represents the S, I, and R values for a single time step
	susceptibles.append(S)
	infected.append(I)
	recovered.append(R)
	newlyInfected.append(newI)

	print('t', t)
	t += 1

print('SUSCEPTIBLES', susceptibles)
print('INFECTED', infected)
print('RECOVERED', recovered)
print('NEWLY INFECTED', newlyInfected)

pl.figure()
pl.plot(susceptibles, '-g')
pl.plot(infected, '-r')
pl.plot(recovered, '-b')
pl.show()

#####################################################################################################
############################################## SILR MODEL ###########################################
#####################################################################################################

## New cases
"""
s (sigma) for sexual transmission rate
p (rho) for rate of recovery from the latent period (1/p = average duration of latency)

(*) m (mu) for mortality rate has yet been implemented

"""

## Initial conditions
S = 1000	# Number of susceptibles
I = 1		# Seed the outbreak with one infectious individual
L = 0		# No one has yet entered latent phase
R = 0 		# No one has yet died or been cured

N = float(S+I+L+R)

## Simulation clock 
t = 0

## Transmission parameters

# Normal infectivity (alpha)
a = np.random.uniform(0.00, 1.00, [1,100])		# Array of 100 random floats from [0.00, 1.00]
a = np.linspace(0.00, 1.0, num=100) 			# Array of 100 floats sorted in ascending order 

# Sexual infectivity (sigma)
s = np.random.uniform(0.00, 1.00, [1,100])		
s = np.linspace(0.00, 1.0, num=100) 			

# Probably of recovering from illness at each time step (lambda), 1/l = average duration of illness
l = np.random.uniform(0.00, 1.00, [1,100])		
l = np.linspace(0.00, 1.0, num=100) 			

# Probably of recovering from the latent phase at each time step (rho), 1/p = average duration of latency
p = np.random.uniform(0.00, 1.00, [1,100])		
p = np.linspace(0.00, 1.0, num=100) 			

# alpha, sigma, lambda, rho, and mu as constant parameters instead of arrays of values 
a = .09
s = .001
l = .033	# 
p = .0037 	# If t is in days => 9 months = 270 days => 1/270 = .0037
m = .6  	# Really high... 

## Storage lists for tracking # of people at each stage for a time step

# The sum of any column through each list should equal N
S_stage = []		# Stores number of susceptible individuals at each step 
I_stage = []		# Stores number of infected individuals 
L_stage = [] 		# Stores number of latent individuals 
R_stage = []		# Stores number of recovered individuals
newlyInfected = []	# Records the number of newly infected people at each step 

# Each list element represents the S, I, and R values for a single time step
S_stage.append(S)
I_stage.append(I)
L_stage.append(L)
R_stage.append(R)
newlyInfected.append(0)

# For as long as there are still infectious individuals, this loop will continue running
while I > 0:

	# No one has yet been infected
	newI = 0

	for individual in range(S):

		# If we use a frequency dependent transmission process: random val is in range [0, 1)
		# if random.random() < a*(I/N):
		# 	newI += 1

		# If we use a density dependent transmission process:
		if random.random() < (a*I + s*L):	
			newI += 1

	# Number of individuals that recover from the illness at each time step --> lambda*I
	recoverI = 0
	for individual in range(I):
		if random.random() < l:		
			recoverI += 1

	# Number of individuals die from the illness at each time step --> mu*I
	dieI = 0
	for individual in range(I):  
		if random.random() < m:		
			dieI += 1

	# Number of individuals that recover from latency at each time step --> rho*I
	recoverL = 0
	for individual in range(L):
		if random.random() < p:		
			recoverL += 1

	""" 
	All plausible events are assumed to occur in a step simultaneously. 
	Susceptible individuals are infected as infected individuals recover. 
	"""
	S -= newI 							
	I += (newI - recoverI - dieI)
	L += (recoverI - recoverL)
	R += (recoverL + dieI)

	# Each list element represents the S, I, and R values for a single time step
	S_stage.append(S)
	I_stage.append(I)
	L_stage.append(L)
	R_stage.append(R)
	newlyInfected.append(0)

	print('t', t)
	t += 1

print('SUSCEPTIBLES', S_stage)
print('INFECTED', I_stage)
print('LATENT', L_stage)
print('REMOVED', R_stage)
print('NEWLY INFECTED', newlyInfected)

print('%s' % (S_stage[1]+I_stage[1]+L_stage[1]+R_stage[1]))
pl.figure()
pl.plot(S_stage, '-g')
pl.plot(I_stage, '-r')
pl.plot(L_stage, '-b')
pl.plot(R_stage, '-k')
pl.show()

#####################################################################################################
############################################## SILR MODEL ###########################################
#####################################################################################################

# a = np.linspace(0.00, 0.1, num=10) 			# Array of 100 floats sorted in ascending order 
# s = np.linspace(0.00, 0.1, num=10) 			

# Ro = np.linspace(1.5, 2.5, num=10)
# pl.figure()
# pl.plot(a, Ro)
# pl.show()
