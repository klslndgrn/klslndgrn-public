import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

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

# ---- EXAMPLE DATA FOR THE PLOT ---- #
num_points = 1000
x = np.linspace(-4*np.pi, 4*np.pi, num=num_points)
f1 = np.exp(x/10)*np.sin(x)*np.cos(x)
f2 = np.exp(2*x/10)*np.sin(2*x)*np.cos(2*x)

# ----------------------------------------------------
# ---- PLOT 1 ----------------------------------------
# ----------------------------------------------------
rc('text', usetex=True)
rc('font', size=10)
rc('legend', fontsize=12)

mttl = 'PLOT 1'
ttl = r'$\mathrm{TITLE}$: $f_1(x) = e^{x/10}sin(x)cos(x)$'
xlbl = r'$\mathrm{X-label}$'
ylbl = r'$\mathrm{Y-label}$'

x_ax_lim = [-10, 10] # X-limits
y_ax_lim = [-5, 5] # Y-limits

fig = plt.figure(mttl, figsize=(10, 7))
# ------------------ #
# ---- PLOTS ---- #
plt.plot(x, f1, label='$f_1(x)$', linewidth=1)
plt.plot(x, f2, label='$f_2(x)$', linewidth=1)
# ---- AXIS ---- #
plt.xlim(x_ax_lim)  # XLIM
plt.ylim(y_ax_lim)  # YLIM
plt.axhline(y=0, color='k', linewidth=0.9, alpha=0.3)  # X-AXIS
plt.axvline(x=0, color='k', linewidth=0.9, alpha=0.3)  # Y-AXIS
# ---- FORMATTING ---- #
plt.grid(visible=True, which='major', color='k', linestyle='-', alpha=0.2)
plt.grid(visible=True, which='minor', color='k', linestyle='--', alpha=0.1)
plt.minorticks_on()
# plt.tick_params(direction='inout')
# plt.tick_params(labelcolor='k', labelsize='large', width=1) # TICK FORMAT
# ---- LEGEND ---- #
plt.legend()
# ---- LABELS ---- #
plt.title(ttl, fontsize = 14)
plt.xlabel(xlbl, fontsize = 12)
plt.ylabel(ylbl, fontsize = 12)
# ---- SHOW PLOT ---- #
plt.show()
# ---- SAVE PLOT ---- #
# plt.savefig("XXXX.png")
# plt.savefig("XXXX.pdf")
