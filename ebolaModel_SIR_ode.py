import random
import numpy as np
import pylab as pl 
import scipy, scipy.integrate

#####################################################################################################
############################################### SIR MODEL ###########################################
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

# Parameters
a = 0.27			        # alpha
l = 1.0 / 33.0			# lambda
m = 1.0 / 60.0	    # mu

# Initial condition
S0 = 100000
I0 = 1
R0 = 0

Y0 = [ S0, I0, R0 ]

tMax = 730

# Time vector for solution
T = scipy.linspace(0, tMax, 1001)

solution = scipy.integrate.odeint(rhs,
                                  Y0,
                                  T,
                                  args = (a, l, m))


S = solution[:, 0]
I = solution[:, 1]
R = solution[:, 2]

# alphaRates = np.linspace(0.00, 5.0, num=8) 
# illnessDurations = range(5, 20, 2)
# traces = []
# traceConditions = []	 ## To plot for different lambda and alpha conditions

# for k in range(len(illnessDurations)):
# 	a = alphaRates[k]
# 	for x in range(len(illnessDurations)):
# 		l = 1 / float(illnessDurations[x])
# 		m = 1.0 / 60.0

# 		solution = scipy.integrate.odeint(rhs,
# 		                                  Y0,
# 		                                  T,
# 		                                  args = (a, l, m))

# 		S = solution[:, 0]
# 		I = solution[:, 1]
# 		R = solution[:, 2]

# 		trace=Scatter( 
# 		  x=T, 
# 		  y=I,
# 		  mode='lines',
# 		  name='%s day duration' % illnessDurations[x],
# 		  marker=Marker(
# 		    symbol='x',
# 		    size=9
# 		    ),
# 		  line=Line(color=colors[x], width=1.0)
# 		)

# 		traces.append(trace)

# 	traceConditions.append(traces)
# 	traces = []

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

traceR=Scatter( 
  x=T, 
  y=R,
  mode='lines',
  name='Removed',
  marker=Marker(
    symbol='x',
    size=9
    ),
  line=Line(color=teal, width=1.0)
)
figure = Figure(
  data=Data([traceS, traceI, traceR]), 
  layout=Layout(
    title='Ebola Virus Disease SIR Model',
    xaxis=XAxis(
      title='Time',
      showgrid=True,
      zeroline=True,
      gridwidth=0.5
      ),
    yaxis=YAxis(
      title='Proportion',
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

# figure = Figure(
#   data=Data(traceConditions[1]), 
#   layout=Layout(
#     title='Ebola Virus Disease SIR Model (alpha=%s)' % alphaRates[1],
#     xaxis=XAxis(
#       title='Time',
#       showgrid=True,
#       zeroline=True,
#       gridwidth=0.5
#       ),
#     yaxis=YAxis(
#       title='Infection Cases',
#       showgrid=True,
#       zeroline=True,
#       gridwidth=0.5
#       ),
#     font=dict(
#       size=12
#       ),
#     titlefont=dict(
#       size=16
#       )
#     )
#   )
py.plot(figure, filename='EVD-SIR', stream=Stream(token='hzb6rmog52', maxpoints=1000))
