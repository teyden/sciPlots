import plotly.plotly as py
from plotly.graph_objs import *
import csv


def scatter_builder_plotly(X=[], Y=[], name='', mode='', shape='', color=''):
	if shape == "":
		shape = 'spline'
	if color == "":
		color = 'rgb(233,62,62)'
	if mode == "":
		mode = "lines"
	trace = Scatter( 
			x=X, 
			y=Y,
			mode=mode,
			name=name, 
			line=Line(shape=shape, color=color, width=0.2)
		)
	return trace

def plot_with_plotly(X=[], Y=[], title={}, trace=[]):
	"""
	Plotter for the plotly module. Loads the web interface 
	for plotly upon successful call to the function, prints
	out success statement, and returns True. 

	X and Y must be non-empty lists of equal lengths. 
	title is an empty string by default. 
	If trace is not specified, then the default trace will be
	used.  
	"""
	if X == [] and Y == []:
		print "Input non-empty lists for x."
	
	# If trace == [], then there is a maximum of one Y axis list.
	if trace == []:  
		# Builds the default trace using the X and Y axis lists
		trace = scatter_builder_plotly(X=X[1:], Y=Y[1:])
	data = Data(trace)
	layout = Layout(
		title=title,
		xaxis=XAxis(
			title=title['x'],
			showgrid=True,
			zeroline=True,
			gridwidth=0.8
			),
		yaxis=YAxis(
			title=title['y'],
			showgrid=True,
			zeroline=True,
			gridwidth=0.8
			),
		font = dict(
			size=16
			),
		titlefont = dict(
			size=24
			)
	)
	figure = Figure(data=data, layout=layout)
	plot = py.plot(figure, filename=title['title'], validate=False)
	print "Plot '%s' has been plotted with plotly." % title


def save_toCSV(storage, path):
		''' 
		Inserts every element in storage to a CSV file given by
		the path string.

		storage is a dictionary with two elements with keys as axis titles
		and values as a list of values with the first element as the title
		for the axis 
			storage['x'] = ['title for x axis', x values...]
			storage['y'] = ['title for y axis', y values...]

		'''
		with open(path, 'w') as csvfile:
			fieldnames = [storage['x'][0], storage['y'][0]]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			# Sets CSV headers with fieldnames
			writer.writeheader()
			# Sets CSV headers with fieldnames
			for key in storage:

				for i in range(1,len(storage[key])):
					writer.writerow({
						storage[key][0]: storage[key][i]
						})
				print "save_toCSV() Status ||| %s added to CSV." % key