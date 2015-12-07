#!/usr/bin/env python
#
# The above allows this script to be run directly from the shell
#

# This loads some pacakges that have arrays etc and the ODE integrators
import scipy, scipy.integrate


# Parameters
# beta = 0.27
# gamma = 0.74
# mu = 1.0 / 5.61  # Warning!  int / int = int, e.g. 1 / 50 = 0.

beta = 5
gamma = 1
mu = 1.0 / 50  # Warning!  int / int = int, e.g. 1 / 50 = 0.

# Initial condition
S0 = 0.99
I0 = 0.00001
R0 = 0.00

Y0 = [ S0, I0, R0 ]

tMax = 730

# Time vector for solution
T = scipy.linspace(0, tMax, 1001)


# This defines a function that is the right-hand side of the ODEs
# Warning!  Whitespace at the begining of a line is significant!
def rhs(Y, t, beta, gamma, mu):
    '''
    SIR model.
    
    This function gives the right-hand sides of the ODEs.
    '''
    
    # Convert vector to meaningful component vectors
    # Note: Indices start with index 0, not 1!
    S = Y[0]
    I = Y[1]
    R = Y[2]
    
    N = S + I + R
    
    # The right-hand sides
    dS = mu * N - beta * I * S - mu * S
    dI = beta * I * S - (gamma + mu) * I
    dR = gamma * I - mu * R
    
    # Convert meaningful component vectors into a single vector
    dY = [ dS, dI, dR ]

    return dY

# Integrate the ODE
# Warning!  The ODE solver over-writes the initial value.
# This can be a pain in the ass if you run the ODE multiple times.
# Also, 'args' passes parameters to right-hand-side function.
solution = scipy.integrate.odeint(rhs,
                                  Y0,
                                  T,
                                  args = (beta, gamma, mu))
        
S = solution[:, 0]
I = solution[:, 1]
R = solution[:, 2]

N = S + I + R

# # Make plots

# Load a plotting package
# PyLab is motivated by Matlab...
import pylab

# I usually use PyLab for quick plots
# and the Python GnuPlot package for publication
pylab.figure()

pylab.plot(T, S / N,
           T, I / N,
           T, R / N)

pylab.xlabel('Time')
pylab.ylabel('Proportion')

pylab.legend([ 'Susceptible', 'Infective', 'Recovered' ])

# Actually display the plot
pylab.show()


# ############ Using Plot.ly ############
# from plotter import scatter_builder_plotly, plot_with_plotly
# import plotly.plotly as py 
# from plotly.graph_objs import *
# teal = 'rgb(89,142,146)'
# red = 'rgb(197,22,22)'
# blue = 'rgb(13,86,172)'
# orange = 'rgb(218,135,60)'
# purple = 'rgb(159,98,225)'
# pink = 'rgb(223,98,225)'
# plum = 'rgb(22,9,22)'
# green = 'rgb(34,149,34)'
# colors = [teal, red, blue, orange, purple, pink, plum, green]

# ## Define traces for each curve 
# traceS=Scatter( 
#   x=T, 
#   y=S/N,
#   mode='lines',
#   name='Susceptible',
#   marker=Marker(
#     symbol='x',
#     size=9
#     ),
#   line=Line(color=blue, width=1.0)
# )

# traceI=Scatter( 
#   x=T, 
#   y=I/N,
#   mode='lines',
#   name='Infective',
#   marker=Marker(
#     symbol='x',
#     size=9
#     ),
#   line=Line(color=red, width=1.0)
# )

# traceR=Scatter( 
#   x=T, 
#   y=R/N,
#   mode='lines',
#   name='Removed',
#   marker=Marker(
#     symbol='x',
#     size=9
#     ),
#   line=Line(color=teal, width=1.0)
# )

# fig = Figure(
#   data=Data([traceS, traceI, traceR]), 
#   layout=Layout(
#     title='Ebola Virus Disease SIR Model',
#     xaxis=XAxis(
#       title='Time (days)',
#       showgrid=True,
#       zeroline=True,
#       gridwidth=0.5
#       ),
#     yaxis=YAxis(
#       title='Population',
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

# fig['layout'].update(height=1000, width=1000, title='Ebola Virus Disease SIR Model (alpha = 0.27)')
# py.image.save_as(fig, 'EVD-SIR.png')
