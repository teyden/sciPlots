from plotter import scatter_builder_plotly, plot_with_plotly
import plotly.plotly as py 
from plotly.graph_objs import Data
import numpy as np
teal = 'rgb(89,142,146)'
red = 'rgb(197,22,22)'
blue = 'rgb(13,86,172)'

"""
scatter_builder_plotly(X=[], Y=[], name='', mode='', shape='', color='')
plot_with_plotly(X=[], Y=[], title={}, trace=[])
save_toCSV(storage, path)
"""


##### (1) Enzymatic rate (vi) vs. "final" enzyme concentration [alkaline phosphatase] - Table 1
"""
- Scatterplot, don't connect dots
- Linear regression using trendline
Y = vi (au(410nm)/min)
X = [alkaline phosphatase] (ug/mL)
"""
enzymeRate = np.array([0.000, 0.05215, 0.1047, 0.18905])
enzymeConcentration = np.array([0.065, 0.130, 0.260])
trace1 = scatter_builder_plotly(X=enzymeConcentration, Y=enzymeRate, name='Effect of Varying Alkaline Phosphatase concentration', shape='markers', color=)
data = Data([trace1])
py.plot(data=data, validate=False)

##### (2a) Enzymatic rate (vi) vs. substrate concentration [PNPP] - Table 2 (Michaelis-Menten Plot)
"""
- Hyperbolic plot, don't connect dots
- Two curves, 1) Alkaline phosphatase control, 2) Alkaline phosphatase + inhibitor
- Final equation for best fit hyperbolic curve
- Km and Vmax values 

Y = vi (au(410nm)/min)
X = [alkaline phosphatase] (ug/mL)
"""

##### (2b) 1/vi vs. 1/[S] - Table 2 (Lineweaver-Burke Plot)
"""
- Scatter plot, don't connect dots
- Two lines, 1) Alkaline phosphatase control, 2) Alkaline phosphatase + inhibitor

Y = 1/vi
X = 1/[S] 
"""

##### (2c) [S]/vi vs. [S] - Table 2 (Hanes-Woolf Plot)
"""
- Scatter plot, don't connect dots

Y = [S]/vi
X = [S]
"""


# traceS = scatter_builder_plotly(T, S/N, 'S', color=teal)
# traceI = scatter_builder_plotly(T, I/N, 'I', color=red)
# traceR = scatter_builder_plotly(T, R/N, 'R', color=blue)
# # fig = {'data': traceS}
# py.image.save_as({'data': Data([traceS, traceI, traceR])}, 'example_SIR_model.png')