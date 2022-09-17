import numpy as np
import matplotlib.pyplot as plt

"""
Linestyles as:
    linestyle =
        'solid' same as '-'
        'dotted' same as ':'
        'dashed' same as '--'
        'dashdot' same as '-.'
Base-colors as:
    color =
        'b' as blue
        'g' as green
        'r' as red
        'c' as cyan (blue-green)
        'm' as magenta (pink)
        'y' as dark yellow
        'k' as black
        'w' as white
RBG Colors as:
    color =
        'tab:blue'
        'tab:orange'
        'tab:green'
        'tab:red'
        'tab:purple'
        'tab:brown'
        'tab:pink'
        'tab:gray'
        'tab:olive'
        'tab:cyan'
Linewidth as:
    linewidth = > 0 "larger than 0!"
Alpha of line as:
    alpha = 0 <-> 1
"""

# ---- PLOT DATA ---- #
num_points = 1000
x = np.linspace(-4*np.pi, 4*np.pi, num=num_points)
f1 = np.exp(x/10)*np.sin(x)*np.cos(x)
f2 = np.exp(2*x/10)*np.sin(2*x)*np.cos(2*x)

xax = [-10, 10]
yax = [-5, 5]

ttl = 'TITLE'
xlbl = 'X-LABEL'
ylbl = 'Y-LABEL'

# ------------------ #
# ---- PLOTTING ---- #
fig = plt.figure('PLOT X',
                 figsize=(7, 5))
# ------------------ #
# ---- PLOTS ---- #
plt.plot(x, f1, label='f1')
plt.plot(x, f2, label='f2')
# ---- AXIS ---- #
plt.xlim(xax)  # XLIM
plt.ylim(yax)  # YLIM
plt.axhline(y=0, color='k', linestyle='-', alpha=0.5)  # X-AXIS
plt.axvline(x=0, color='k', linestyle='-', alpha=0.5)  # Y-AXIS
# ---- FORMATTING ---- #
plt.grid(visible=True, which='major',
         color='k', linestyle='-', alpha=0.3)  # MAJOR GRID
plt.grid(visible=True, which='minor',
         color='k', linestyle='-', alpha=0.1)  # MINOR GRID
plt.minorticks_on()
# plt.tick_params(labelcolor='k', labelsize='large', width=1) # TICK FORMAT
# ---- LEGEND ---- #
plt.legend()
# ---- LABELS ---- #
plt.title(ttl, usetex=True)
plt.xlabel(xlbl, usetex=True)
plt.ylabel(ylbl, usetex=True)
# ---- SHOW PLOT ---- #
plt.show()
# ---- SAVE PLOT ---- #
# plt.savefig("XXXX.png")
