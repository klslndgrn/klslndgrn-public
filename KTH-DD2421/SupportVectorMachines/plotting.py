def plot_data(A, B, XYG=None,
              Fignum='', Title=r'$\mathrm{Support \; Vector \; Machine}$',
              XLabel=r'$\mathrm{Datapoint}$ $x_i$',
              YLabel=r'$\mathrm{Datapoint}$ $x_j$',
              XLimits=[-4, 4], YLimits=[-4, 4],
              XLines=[], YLines=[],
              LineLabels=None, LineColors=None, LineStyles=None,
              SaveAs=None):
    '''This function uses Matplotlib to plot.
    Atleast one X-vector and Y-vector is needed.'''

    # ==== Libraries ==========================================================
    import matplotlib.pyplot as plt
    from matplotlib import rc
    import seaborn as sns

    # ==== Settings ===========================================================
    rc('text', usetex=True)
    rc('font', size=10)
    rc('legend', fontsize=12)
    # set seaborn style
    sns.set_style("white")

    # ==== Figure =============================================================
    f, ax = plt.subplots(figsize=(10, 7))
    # ==== PLOTS ==============================================================
    for p in A:
        plt.plot(p[0], p[1], color='b', marker='.')
    for p in B:
        plt.plot(p[0], p[1], color='r', marker='.')
    # ==== CONTOUR ============================================================
    if XYG is not None:
        plt.contour(XYG[0], XYG[1], XYG[2],
                    (-1.0, 0.0, 1.0),
                    colors=('red', 'black', 'blue'),
                    linewidths=(1, 3, 1))
    # ==== SEABORN ============================================================
    sns.kdeplot(x=A[:, 0], y=A[:, 1],
                cmap="Blues", fill=True, alpha=0.5)
    sns.kdeplot(x=B[:, 0], y=B[:, 1],
                cmap="Reds", fill=True, alpha=0.5)
    # ==== X AND Y AXIS =======================================================
    plt.axhline(y=0, color='k', linewidth=0.9, alpha=0.3)  # X-AXIS
    plt.axvline(x=0, color='k', linewidth=0.9, alpha=0.3)  # Y-AXIS
    # plt.axis('equal')
    # ==== AXIS ===============================================================
    if len(XLimits) == 2:
        plt.xlim(XLimits)  # XLIM
    if len(YLimits) == 2:
        plt.ylim(YLimits)  # YLIM
    # ==== FORMATTING =========================================================
    plt.grid(visible=True, which='major', color='k', linestyle='-', alpha=0.2)
    plt.grid(visible=True, which='minor', color='k', linestyle='--', alpha=0.1)
    plt.minorticks_on()
    # ==== LABELS =============================================================
    # textstr = '\n'.join((r'$\mathrm{Kernel:\;Linear}$',
    #                      r'$\mathrm{C:\;None}$'))
    # textstr = '\n'.join((r'$\mathrm{Kernel:\;Polynomial}$',
    #                      r'$\mathrm{C:\;5}$',
    #                      r'$\mathrm{p:\;2}$'))
    textstr = '\n'.join((r'$\mathrm{Kernel:\;Radial Basis}$',
                         r'$\mathrm{C:\;1}$',
                         r'$\sigma\mathrm{:\;0.5}$'))
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', color='black',
            bbox=dict(facecolor='gray', alpha=0.3,
                      edgecolor='black', boxstyle='round,pad=1'))
    # ==== LABELS =============================================================
    plt.title(Title, fontsize=14)
    plt.xlabel(XLabel, fontsize=12)
    plt.ylabel(YLabel, fontsize=12)
    # ==== SAVE PLOT ==========================================================
    if SaveAs is not None:
        if 'png' in SaveAs:
            plt.savefig(SaveAs, dpi=600)
        else:
            plt.savefig(SaveAs)
    # ==== SHOW PLOT ==========================================================
    plt.show()
    # =========================================================================
