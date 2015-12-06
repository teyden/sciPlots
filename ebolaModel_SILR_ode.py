import random
import numpy as np
import pylab as pl 
import scipy, scipy.integrate

#####################################################################################################
############################################## SILR MODEL ###########################################
#####################################################################################################

## Plot using Plot.ly (much nicer) - outputs to web  
from plotter import scatter_builder_plotly, plot_with_plotly
import plotly.plotly as py 
from plotly.graph_objs import *
teal = 'rgb(89,142,146)'
red = 'rgb(197,22,22)'
blue = 'rgb(13,86,172)'
orange = 'rgb(218,135,60)'
purple = 'rgb(159,98,225)'
pink = 'rgb(223,98,225)'
plum = 'rgb(22,9,22)'
green = 'rgb(34,149,34)'
colors = [teal, red, blue, orange, purple, pink, plum, green]


# Parameters
a = 0.27			          # alpha
l = 1.0 / 5.61          # lambda, from Parameters table (find on slack)
s = .01	      		      # sigma = [0, alpha], plot over vector series of sigma values. 
p = 1.0 / 169.0		  # rho
m = 0.74	    # mu

# Initial condition
S0 = 100000.0
I0 = 1.0
L0 = 0
R0 = 0
N0 = S0 + I0

Y0 = [ S0, I0, L0 ]

tMax = 730

# Time vector for solution
T = scipy.linspace(0, tMax, 1001)

# This defines a function that is the right-hand side of the ODEs
def rhs(Y, t, alpha, sigma, lambd, rho, mu):
    '''
    SIR model.
    
    This function gives the right-hand sides of the ODEs.
    '''
    
    # Convert vector to meaningful component vectors
    S = Y[0]
    I = Y[1]
    L = Y[2]

    alpha = alpha / N0
    sigma = sigma / N0
    
    # The right-hand sides
    dS = -1 * S * (alpha * I + sigma * L)
    dI = S * (alpha * I + sigma * L) - lambd * I
    dL = (1 - mu) * lambd * I - rho * L

    # Initial condition, assuming that L is 0
    # Ro = alpha / lambda
    # dI = I * lambd * ((alpha / lambd) * S - mu / lambd - 1)
    
    # Convert meaningful component vectors into a single vector
    dY = [ dS, dI, dL ]

    return dY

# Integrate the ODE
# The ODE solver over-writes the initial value.
# Also, 'args' passes parameters to right-hand-side function.
solution = scipy.integrate.odeint(rhs,
                                  Y0,
                                  T,
                                  args = (a, s, l, p, m))

print solution 
        
S = solution[:, 0]
I = solution[:, 1]
L = solution[:, 2]

traceS=Scatter( 
  x=T, 
  y=S,
  mode='lines',
  name='Susceptible',
  marker=Marker(
    symbol='x',
    size=9
    ),
  line=Line(color=blue, width=1.0)
)

traceI=Scatter( 
  x=T, 
  y=I,
  mode='lines',
  name='Infective',
  marker=Marker(
    symbol='x',
    size=9
    ),
  line=Line(color=red, width=1.0)
)

traceL=Scatter( 
  x=T, 
  y=L,
  mode='lines',
  name='Latent',
  marker=Marker(
    symbol='x',
    size=9
    ),
  line=Line(color=green, width=1.0)
)

## Plot everything
figure = Figure(
  data=Data([traceS, traceI, traceL]), 
  layout=Layout(
    title='Ebola Virus Disease SILR Model',
    xaxis=XAxis(
      title='Time (days)',
      showgrid=True,
      zeroline=True,
      gridwidth=0.5
      ),
    yaxis=YAxis(
      title='Population',
      showgrid=True,
      zeroline=True,
      gridwidth=0.5
      ),
    font=dict(
      size=12
      ),
    titlefont=dict(
      size=16
      )
    )
  )

py.plot(figure, filename='EVD-SILR')

