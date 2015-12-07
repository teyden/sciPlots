import random
import numpy as np
import pylab as pl 
import scipy, scipy.integrate

#####################################################################################################
############################################## SILR MODEL ###########################################
#####################################################################################################

## Plot using Plot.ly (much nicer) - outputs to web  
from plotter import scatter_builder_plotly, plot_with_plotly
from plotly import tools
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
black = 'rgb(0,0,0)'
colors = [teal, red, blue, orange, purple, pink, plum, green]


# Parameters
a = 0.27			          # alpha
l = 1.0 / 5.61          # lambda, from Parameters table (find on slack)
s = .01	      		      # sigma = [0, alpha], plot over vector series of sigma values. 
p = 1.0 / 169.0		  # rho
m = 0.74	    # mu

# Adjust to graph for SIR model. No latent class to be represented
s = 0.0
p = 0.0

# Initial condition
S0 = 100000.0
I0 = 1.0
L0 = 0
R0 = 0
N0 = S0 + I0

Y0 = [ S0, I0, R0 ]

tMax = 1000

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
    R = Y[2]

    alpha = alpha / N0
    sigma = sigma / N0
    
    # The right-hand sides

    dS = -1 * alpha * I * S
    dI = alpha * I * S - lambd * I
    dR = lambd * I

    # dS = -1 * S * (alpha * I + sigma * L)
    # dI = S * (alpha * I + sigma * L) - lambd * I
    # dL = (1 - mu) * lambd * I - rho * L
    # dR = mu * lambd * I 
    # Initial condition, assuming that L is 0
    # Ro = alpha / lambda
    # dI = I * lambd * ((alpha / lambd) * S - mu / lambd - 1)
    
    # Convert meaningful component vectors into a single vector
    dY = [ dS, dI, dR ]

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
R = solution[:, 2]

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

# traceL=Scatter( 
#   x=T, 
#   y=L,
#   mode='lines',
#   name='Latent',
#   marker=Marker(
#     symbol='x',
#     size=9
#     ),
#   line=Line(color=green, width=1.0)
# )

traceR=Scatter( 
  x=T, 
  y=R,
  mode='lines',
  name='Removed',
  marker=Marker(
    symbol='x',
    size=9
    ),
  line=Line(color=black, width=1.0)
)

## Plot everything
fig = Figure(
  data=Data([traceS, traceI, traceR]), 
  layout=Layout(
    title='Ebola Virus Disease SIR Model',
    xaxis=XAxis(
      title='time (days)',
      showgrid=True,
      zeroline=True,
      gridwidth=0.5
      ),
    yaxis=YAxis(
      title='population',
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

SIR_trace = [traceS, traceI, traceR]
###############################################################################
# # py.plot(figure, filename='EVD-SIR_zeroLatent')
# fig['layout'].update(height=1000, width=1000, title='Ebola Virus Disease SIR Model (alpha = 0.27)')

# py.image.save_as(fig, 'EVD-EVD-SIR_zeroLatent.png')



# Parameters
a = 0.27                # alpha
l = 1.0 / 5.61          # lambda, from Parameters table (find on slack)
s = .01                 # sigma = [0, alpha], plot over vector series of sigma values. 
p = 1.0 / 169.0         # rho
m = 0.74                # mu

s = 0.0

# Initial condition
S0 = 100000.0
I0 = 1.0
L0 = 0
R0 = 0
N0 = S0 + I0 + R0

Y0 = [ S0, I0, L0, R0 ]

tMax = 1000

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
    R = Y[3]

    alpha = alpha / N0
    sigma = sigma / N0
    
    # The right-hand sides
    dS = -1 * S * (alpha * I + sigma * L)
    dI = S * (alpha * I + sigma * L) - lambd * I
    dL = (1 - mu) * lambd * I - rho * L
    dR = mu * lambd * I + rho * L

    # Initial condition, assuming that L is 0
    # Ro = alpha / lambda
    # dI = I * lambd * ((alpha / lambd) * S - mu / lambd - 1)
    
    # Convert meaningful component vectors into a single vector
    dY = [ dS, dI, dL, dR ]

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
R = solution[:, 3]

traceS=Scatter( 
  x=T, 
  y=S,
  mode='lines',
  showlegend=False,
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
  showlegend=False,
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

traceR=Scatter( 
  x=T, 
  y=R,
  mode='lines',
  showlegend=False,
  marker=Marker(
    symbol='x',
    size=9
    ),
  line=Line(color=black, width=1.0)
)

SILR_trace = [traceS, traceI, traceL, traceR]


fig = tools.make_subplots(rows=1, cols=2, subplot_titles=('SIR', 'SILR'))

fig.append_trace(SIR_trace[0], 1, 1)
fig.append_trace(SILR_trace[0], 1, 2)

fig.append_trace(SIR_trace[1], 1, 1)
fig.append_trace(SILR_trace[1], 1, 2)

fig.append_trace(SIR_trace[2], 1, 1)
fig.append_trace(SILR_trace[2], 1, 2)

fig.append_trace(SILR_trace[3], 1, 2)

fig['layout'].update(height=700, width=900)
fig['layout']['xaxis1'].update(title='t (days)', showline=True, mirror=True)
fig['layout']['yaxis1'].update(title='Population', showline=True, mirror=True)
fig['layout']['xaxis2'].update(title='t (days)', showline=True, mirror=True)
fig['layout']['yaxis2'].update(title='Population', showline=True, mirror=True)
py.image.save_as(fig, 'EVD-SIR-SILR_comparison.png')