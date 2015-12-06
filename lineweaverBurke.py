from plotter import scatter_builder_plotly, plot_with_plotly
import plotly.plotly as py 
from plotly.graph_objs import *
import numpy as np
teal = 'rgb(89,142,146)'
red = 'rgb(197,22,22)'
blue = 'rgb(13,86,172)'

"""
scatter_builder_plotly(X=[], Y=[], name='', mode='', shape='', color='')
plot_with_plotly(X=[], Y=[], title={}, trace=[])
save_toCSV(storage, path)
"""

stream_ids = ["amo3i4wkhl", "1ef07kyg6t", "tlzo4famlm", "jib5xblf4u"]

#########################################################################################################
#########################################################################################################
####################  (2b) 1/vi vs. 1/[S] - Table 2 (Lineweaver-Burke Plot)  ############################
#########################################################################################################
#########################################################################################################
"""
- Scatter plot, don't connect dots
- Two lines, 1) Alkaline phosphatase control, 2) Alkaline phosphatase + inhibitor

Y = 1/vi
X = 1/[S] 
"""

Control_enzymeRate = np.array([0.0218, 0.0447, 0.0815, 0.0975, 0.1035])
Control_enzymeConcentration = np.array([3.636, 9.091, 45.45, 90.91, 181.82])

Inhibitor_enzymeRate = np.array([0.0056, 0.0216, 0.0370, 0.0545, 0.0746])
Inhibitor_enzymeConcentration = np.array([9.091, 45.45, 90.91, 181.82, 363.64])

Control_Y = 1/Control_enzymeRate
Control_X = 1/Control_enzymeConcentration

Inhibitor_Y = 1/Inhibitor_enzymeRate
Inhibitor_X = 1/Inhibitor_enzymeConcentration

title2 = 'Lineweaver-Burk Plot for Alkaline Phosphatase in the presence and absence of an Inhibitor'

traceControl=Scatter( 
	x=Control_X, 
	y=Control_Y,
	mode='markers',
	name='Alk.Phos. control',
	marker=Marker(
		symbol='x',
		size=9
		),
	line=Line(color=blue, width=0.5)
)

traceInhibitor=Scatter( 
	x=Inhibitor_X, 
	y=Inhibitor_Y,
	mode='markers',
	name='Alk.Phos. + inhibitor',
	marker=Marker(
		symbol='x',
		size=9
		),
	line=Line(color=red, width=0.5)
)

figure = Figure(
	data=Data([traceControl, traceInhibitor]), 
	layout=Layout(
		title=title2,
		xaxis=XAxis(
			title='1/[S]',
			showgrid=True,
			zeroline=True,
			gridwidth=0.8
			),
		yaxis=YAxis(
			title='1/vi',
			showgrid=True,
			zeroline=True,
			gridwidth=0.8
			),
		font=dict(
			size=12
			),
		titlefont=dict(
			size=20
			)
		)
	)
py.plot(figure, filename='Enzyme Kinetics Plot 2b', stream=Stream(token=stream_ids[2], maxpoints=1000))