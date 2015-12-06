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
    
    # The right-hand sides
    dS = -1 * S * (alpha * I + sigma * L) / N
    dI = S * (alpha * I + sigma * L) / N - (mu + lambd) * I
    dL = lambd * I - rho * L 

    # Convert meaningful component vectors into a single vector
    dY = [ dS, dI, dL ]
    return dY

# Parameters
a = 5               # alpha
l = 1.0 / 5.61      # lambda
s = 0.0             # sigma
p = 1.0 / 180.0     # rho
m = 1.0 / 60.0      # mu

# Initial condition
N = 1000.0
S0 = N - 1
I0 = 1
L0 = 0
R0 = 0

Y0 = [ S0, I0, L0 ]

tMax = 100

# Time vector for solution
T = scipy.linspace(0, tMax, 1001)

## Using for loop to output more conditions at once
alphaRates = np.linspace(0.00, 5.0, num=8) 
sigmaRates = np.linspace(0.00, 5.0, num=8) 
illnessDurations = range(5, 20, 2)
traces_a = []
traceConditions_a = []   ## To plot for different lambda and alpha conditions
traces_s = []
traceConditions_s = []   ## To plot for different lambda and alpha conditions

for k in range(len(illnessDurations)):
  a = alphaRates[k]
  # s = sigmaRates[k]
  for x in range(len(illnessDurations)):
    l = 1 / float(illnessDurations[x])
    solution = scipy.integrate.odeint(rhs,
                                      Y0,
                                      T,
                                      args = (a, s, l, p, m))

    S = solution[:, 0]
    I = solution[:, 1]
    L = solution[:, 2]

    Ro_alpha = (s * L / I * l) + (m / l) + 1
    Ro_sigma = (L * s * p * a / L * s * p * l)

    trace_a=Scatter( 
      x=T, 
      y=Ro_alpha,
      mode='lines',
      name='%s' % illnessDurations[x],
      marker=Marker(
        symbol='x',
        size=9
        ),
      line=Line(color=colors[x], width=1.0)
    )

    trace_s=Scatter( 
      x=T, 
      y=Ro_sigma,
      mode='lines',
      name='%s day duration' % illnessDurations[x],
      marker=Marker(
        symbol='x',
        size=9
        ),
      line=Line(color=colors[x], width=1.0)
    )

    traces_a.append(trace_a)
    traces_s.append(trace_s)

  traceConditions_a.append(traces_a)
  traceConditions_s.append(traces_s)
  traces_a = []
  traces_s = []


for i in range(1,2):
  figure = Figure(
    data=Data(traceConditions_a[i]), 
    layout=Layout(
      title='EVD Ro (alpha=%s, sigma=%s)' % (alphaRates[i], sigmaRates[i]),
      xaxis=XAxis(
        title='Time',
        showgrid=True,
        zeroline=True,
        gridwidth=0.5
        ),
      yaxis=YAxis(
        title='Reproduction Number',
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
  py.plot(figure, filename='EVD-SILR Graph %s' % i)

  ## Plot everything
  figure = Figure(
    data=Data(traceConditions_s[i]), 
    layout=Layout(
      title='EVD Ro specific to Sexual Transmission (alpha=%s, sigma=%s)' % (alphaRates[i], sigmaRates[i]),
      xaxis=XAxis(
        title='Time',
        showgrid=True,
        zeroline=True,
        gridwidth=0.5
        ),
      yaxis=YAxis(
        title='Reproduction Number',
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
  py.plot(figure, filename='EVD-SILR Sexual Graph %s' % i)