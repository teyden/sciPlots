import random
import numpy as np
import pylab as pl 
import scipy, scipy.integrate

#####################################################################################################
############################################## SILR MODEL ###########################################
#####################################################################################################
# how much of an effect would limiting sexual contact of ebola survivors would have? (# of 

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

"""
alpha = infection rate 
sigma = sexual infection rate 
lambda = rate of recovery / rate of going from I -> L
rho = rate of recovery / rate of going from L -> R
mu = rate of death 
1 - mu = rate of not dying 
"""

# Parameters
a = 0.27                # alpha
l = 1.0 / 5.61          # lambda, from Parameters table (find on slack)
s = .01                 # sigma = [0, alpha], plot over vector series of sigma values. 
p = 1.0 / 169.0         # rho
m = 0.74                # mu

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


# Using for loop to output more sigma conditions 
sigmaRates = np.linspace(0.01, a/2.0, num=4)
sigmaRates = np.linspace(0.01, a/2.0, num=4)
sigmaRates = [0.0, a/100, a/10, a/4, a/3, a/2]

traceConditions = []   ## To plot for different lambda and alpha conditions
for i, sigma in enumerate(sigmaRates):
  s = sigma 
  solution = scipy.integrate.odeint(rhs,
                                    Y0,
                                    T,
                                    args=(a, s, l, p, m))

  S = solution[:, 0]
  I = solution[:, 1]
  L = solution[:, 2]
  R = solution[:, 3]
  print "*************"
  print('LATENT', L)
  print('REMOVED', R)

  if i == 0:
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


  else:
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
      showlegend=False,
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


  traceConditions.append([ traceS, traceI, traceL, traceR ])


for item in traceConditions:
  print '**************************'
  # print item[0]
  # print item[1]

## Plot everything

tokens = ['pq37pxx4y3', '8272w1lh4o', 's5ekv993e6', 'rz46mfkiki', '87gmh2eos1']
figures = []
titles = []
letters = ['A', 'B', 'C', 'D', 'E', 'F']
for i, traces in enumerate(traceConditions):
  title = '%s. sigma = %s' % (letters[i], format(sigmaRates[i], '.3f'))
  figure = Figure(
    data=Data(traces), 
    layout=Layout(
      title=title,
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
  titles.append(title)
  figures.append(figure)
  # py.plot(figure, filename='EVD-SILR', stream=Stream(token=tokens[i], maxpoints=1000))


fig = tools.make_subplots(rows=3, cols=2, subplot_titles=(titles[0], titles[1], titles[2], titles[3], titles[4], titles[5]))
# print "********* traceConditions"
# print traceConditions[0][1]


fig.append_trace(traceConditions[0][0], 1, 1)
fig.append_trace(traceConditions[1][0], 1, 2)
fig.append_trace(traceConditions[2][0], 2, 1)
fig.append_trace(traceConditions[3][0], 2, 2)
fig.append_trace(traceConditions[4][0], 3, 1)
fig.append_trace(traceConditions[5][0], 3, 2)

fig.append_trace(traceConditions[0][1], 1, 1)
fig.append_trace(traceConditions[1][1], 1, 2)
fig.append_trace(traceConditions[2][1], 2, 1)
fig.append_trace(traceConditions[3][1], 2, 2)
fig.append_trace(traceConditions[4][1], 3, 1)
fig.append_trace(traceConditions[5][1], 3, 2)

fig.append_trace(traceConditions[0][2], 1, 1)
fig.append_trace(traceConditions[1][2], 1, 2)
fig.append_trace(traceConditions[2][2], 2, 1)
fig.append_trace(traceConditions[3][2], 2, 2)
fig.append_trace(traceConditions[4][2], 3, 1)
fig.append_trace(traceConditions[5][2], 3, 2)

fig.append_trace(traceConditions[0][3], 1, 1)
fig.append_trace(traceConditions[1][3], 1, 2)
fig.append_trace(traceConditions[2][3], 2, 1)
fig.append_trace(traceConditions[3][3], 2, 2)
fig.append_trace(traceConditions[4][3], 3, 1)
fig.append_trace(traceConditions[5][3], 3, 2)

fig['layout'].update(height=1000, width=1000)

for i, item in enumerate(traceConditions):
  xaxis = 'xaxis%s' % str(i+1)
  yaxis = 'yaxis%s' % str(i+1)
  fig['layout'][xaxis].update(title='t (days)', showline=True, mirror=True)
  fig['layout'][yaxis].update(title='Population', showline=True, mirror=True)
  fig['layout'][yaxis].update(ticktext=['0', '10k', '20k', '30k', '40k', '50k', '60k', '70k', '80k', '90k', '100k'],
  tickvals=[0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000])


fig['layout'].update(font=dict(size=10))
py.image.save_as(fig, 'EVD-SILR_sigma_multi.png')
