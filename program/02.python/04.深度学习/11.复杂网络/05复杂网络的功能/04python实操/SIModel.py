#%%
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics.SIModel as si

# Network topology
g = nx.erdos_renyi_graph(1000, 0.1)

# Model selection
model = si.SIModel(g)

# Model Configuration
cfg = mc.Configuration()
cfg.add_model_parameter('beta', 0.01)
cfg.add_model_parameter("percentage_infected", 0.05)
model.set_initial_status(cfg)

# Simulation execution
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
viz1 = DiffusionTrend(model, trends)
p = viz1.plot(width=400, height=400)
# show(p)
print(viz1)
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
viz2 = DiffusionPrevalence(model, trends)
p2 = viz2.plot(width=400, height=400)
from ndlib.viz.bokeh.MultiPlot import MultiPlot
vm1 = MultiPlot()
vm1.add_plot(p)
vm1.add_plot(p2)
m = None
m = vm1.plot()
show(m)

#%%
