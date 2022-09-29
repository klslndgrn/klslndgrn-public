# Plot functions

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


def plot_one_graph(Variables, Functions,
                   Fignum='', Title='TITLE',
                   XLabel='X-label', YLabel='Y-label',
                   XLimits=[], YLimits=[],
                   XLines=[], YLines=[],
                   LineLabels=None, LineColors=None, LineStyles=None,
                   SaveAs=None):
    '''This function uses Matplotlib to plot.
    Atleast one X-vector and Y-vector is needed.'''

    # ---- Libraries ---- # ---------------------------------------------------
    import matplotlib.pyplot as plt
    from matplotlib import rc

    # ---- Settings ---- # ----------------------------------------------------
    rc('text', usetex=True)
    rc('font', size=10)
    rc('legend', fontsize=12)

    # ---- Figure ---- # ------------------------------------------------------
    plt.figure(f'PLOT {Fignum}', figsize=(10, 7))
    # ---- PLOTS ---- # -------------------------------------------------------
    if LineLabels is not None and LineColors is None:
        for x, y, l in zip(Variables,
                           Functions,
                           LineLabels):
            plt.plot(x, y, label=l, linewidth=1)
    elif LineLabels is not None and LineColors is not None:
        if LineStyles is not None:
            for x, y, l, c, t in zip(Variables,
                                     Functions,
                                     LineLabels,
                                     LineColors,
                                     LineStyles):
                plt.plot(x, y, label=l, color=c, linestyle=t, linewidth=1)
        else:
            for x, y, l, c in zip(Variables,
                                  Functions,
                                  LineLabels,
                                  LineColors):
                plt.plot(x, y, label=l, color=c, linewidth=1)
    else:
        for x, y in zip(Variables, Functions):
            plt.plot(x, y, linewidth=1)
    # ---- X-LINE PLOTS ---- # ------------------------------------------------
    if XLines is not None:
        for x in XLines:
            plt.axvline(x=x, color='k', linestyle='--', linewidth=1)
    # ---- Y-LINE PLOTS ---- # ------------------------------------------------
    if YLines is not None:
        for y in YLines:
            plt.axhline(y=y, color='k', linestyle='--', linewidth=1)
    # ---- X AND Y AXIS ---- # ------------------------------------------------
    plt.axhline(y=0, color='k', linewidth=0.9, alpha=0.3)  # X-AXIS
    plt.axvline(x=0, color='k', linewidth=0.9, alpha=0.3)  # Y-AXIS
    # ---- AXIS ---- # --------------------------------------------------------
    if len(XLimits) == 2:
        plt.xlim(XLimits)  # XLIM
    if len(YLimits) == 2:
        plt.ylim(YLimits)  # YLIM
    # ---- FORMATTING ---- # --------------------------------------------------
    plt.grid(visible=True, which='major', color='k', linestyle='-', alpha=0.2)
    plt.grid(visible=True, which='minor', color='k', linestyle='--', alpha=0.1)
    plt.minorticks_on()
    # ---- LEGEND ---- # ------------------------------------------------------
    if LineLabels is not None:
        plt.legend()
    # ---- LABELS ---- # ------------------------------------------------------
    plt.title(Title, fontsize=14)
    plt.xlabel(XLabel, fontsize=12)
    plt.ylabel(YLabel, fontsize=12)
    # ---- SAVE PLOT ---- # ---------------------------------------------------
    if SaveAs is not None:
        if 'png' in SaveAs:
            plt.savefig(SaveAs, dpi=600)
        else:
            plt.savefig(SaveAs)
    # ---- SHOW PLOT ---- # ---------------------------------------------------
    plt.show()
    # -------------------------------------------------------------------------


def plot_subplot(Variables, Functions,
                 MainTitle='MAIN TITLE', Title='TITLE',
                 XLabel='X-label', YLabel='Y-label',
                 XLimits=[], YLimits=[],
                 XLines=[], YLines=[],
                 LineLabels=None, LineColors=None, LineStyles=None,
                 SaveAs=None):
    '''This function uses Matplotlib to plot.
    Atleast one X-vector and Y-vector is needed.'''

    # ---- Libraries ---- # ---------------------------------------------------
    import matplotlib.pyplot as plt
    from matplotlib import rc

    # ---- Settings ---- # ----------------------------------------------------
    rc('text', usetex=True)
    rc('font', size=10)
    rc('legend', fontsize=12)

    # ---- Figure ---- # ------------------------------------------------------
    fig, ax = plt.subplots(2, 1, figsize=(10, 7))
    # ---- PLOTS ---- # -------------------------------------------------------
    for x, y, i in zip(Variables, Functions, range(len(Variables))):
        # ---- Main-plot ---- #
        ax[i].plot(x, y, linewidth=1)

        # ---- X AND Y AXIS ---- #
        ax[i].axhline(y=0, color='k', linewidth=0.9, alpha=0.3)  # X-AXIS
        ax[i].axvline(x=0, color='k', linewidth=0.9, alpha=0.3)  # Y-AXIS
        # ---- AXIS ---- #
        if len(XLimits) == 2:
            ax[i].xlim(XLimits)  # XLIM
        if len(YLimits) == 2:
            ax[i].ylim(YLimits)  # YLIM
        # ---- FORMATTING ---- #
        ax[i].grid(visible=True, which='major', color='k',
                   linestyle='-', alpha=0.2)
        ax[i].grid(visible=True, which='minor', color='k',
                   linestyle='--', alpha=0.1)
        ax[i].minorticks_on()
        # ---- LEGEND ---- #
        if LineLabels is not None:
            ax[i].legend()
        # ---- LABELS ---- #
        ax[i].set_xlabel(XLabel, fontsize=12)
        ax[i].set_ylabel(YLabel, fontsize=12)
    # ---- LABELS ---- #
    ax[0].set_title(MainTitle, fontsize=14)
    # ---- SAVE PLOT ---- #
    if SaveAs is not None:
        if 'png' in SaveAs:
            plt.savefig(SaveAs, dpi=600)
        else:
            plt.savefig(SaveAs)
    # ---- SHOW PLOT ---- #
    plt.show()
