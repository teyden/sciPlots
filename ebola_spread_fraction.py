from matplotlib import pyplot as plt 
from scipy.integrate import ode
import numpy as np 


## Parameters
alpha = 0
lambda_ = float(1)/float(5.61)
mu = 0.77
sigma_pass = 0
rho_pass = 0

# def dSdt_fraction(t, S):
# 	"""
# 	S is an np.array, t is a constant? 
# 	"""
# 	a = (-1*(alpha*S[1] + sigma_pass*S[2])) * S[0]
# 	b = (alpha*S[1] + sigma_pass*S[2]) * S[0]-lambda_*S[1]
# 	c = (1-mu) * lambda_*S[1] - rho_pass*S[2]

# 	print a
# 	print b
# 	print c

	# return np.array([a, b, c])

def ebolaSpreadFraction(sigma, rho, t, S):
	"""
	"""
	S0 = range(0, 100000, 1)
	S0.reverse()
	S0 = np.array(S0)
	alpha = float(0.27)/float(S0[0])
	sigma_pass = float(sigma)/float(S0[0])
	rho_pass = rho

	a = (-1*(alpha*S[1] + sigma_pass*S[2])) * S[0]
	b = (alpha*S[1] + sigma_pass*S[2]) * S[0]-lambda_*S[1]
	c = (1-mu) * lambda_*S[1] - rho_pass*S[2]
	dSdt_fraction = np.array([a, b, c])

	r = ode(dSdt_fraction).set_integrator('dopri5')
	r.set_initial_value()

	return solution



# Number of cases vs. contact/time 



## Different values of R0