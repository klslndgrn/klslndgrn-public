import numpy as np
from plot_functions import plot_one_graph
from plot_functions import plot_subplot

# ---- EXAMPLE DATA FOR THE PLOT ---- #
num_points = 1000
x = np.linspace(-4*np.pi, 4*np.pi, num=num_points)
f1 = np.exp(x/10)*np.sin(x)*np.cos(x)
f2 = np.exp(2*x/10)*np.sin(2*x)*np.cos(2*x)

x_ax_lim = [-10, 10]  # X-limits
y_ax_lim = [-5, 5]  # Y-limits

lbls = ['$f_1$', '$f_2$']

plot_one_graph([x, x], [f1, f2],
               LineLabels=lbls,
               LineColors=['r', 'b'],
               LineStyles=['-', '--'],
               XLimits=x_ax_lim,
               YLimits=y_ax_lim)

plot_subplot([x, x], [f1, f2])

# , SaveAs='test.png'
