import monkdata as m
import dtree
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import drawtree_qt5 as qt5

# ----------------------------------------------------
# ---- Datasets --------------------------------------
# ----------------------------------------------------

# MONK1 and MONK1-TEST
m1 = m.monk1
m1t = m.monk1test

# MONK2 and MONK2-TEST
m2 = m.monk2
m2t = m.monk2test

# MONK3 and MONK3-TEST
m3 = m.monk3
m3t = m.monk3test

# # EXPERIMENT SET
# ed = m.exp_data
# ea = m.exp_attributes

# te = dtree.buildTree(ed, ea)
# tedraw = qt5.drawTree(te)


# ----------------------------------------------------
# ---- ASSIGNMENT 0 ----------------------------------
# ----------------------------------------------------
print('')
print('ASSIGNMENT 0:')
print('Number of samples for TRAINING datasets:')
print(f'Length of MONK1 = {len(m1)}')
print(f'Length of MONK2 = {len(m2)}')
print(f'Length of MONK3 = {len(m3)}')
print('')
print('Number of samples for TEST datasets:')
print(f'Length of MONK1-TEST = {len(m1t)}')
print(f'Length of MONK2-TEST = {len(m2t)}')
print(f'Length of MONK3-TEST = {len(m3t)}')
print('')

# ----------------------------------------------------
# ---- ASSIGNMENT 1 ----------------------------------
# ----------------------------------------------------

# MONK1-3 Entropy
ent1 = dtree.entropy(m1)
ent2 = dtree.entropy(m2)
ent3 = dtree.entropy(m3)

print('')
print('ASSIGNMENT 1:')
print(f'Entropy for MONK1 = {ent1:.4f}')
print(f'Entropy for MONK2 = {ent2:.4f}')
print(f'Entropy for MONK3 = {ent3:.4f}')
print('')

# ----------------------------------------------------
# ---- ASSIGNMENT 3 ----------------------------------
# ----------------------------------------------------

print('')
print('ASSIGNMENT 3')
print('Expected Information Gain:')
print('MONK1')
for a in range(6):
    ag = dtree.averageGain(m1, m.attributes[a])
    print(f'A{a+1} = {ag:.4f}')
print('MONK2')
for a in range(6):
    ag = dtree.averageGain(m2, m.attributes[a])
    print(f'A{a+1} = {ag:.4f}')
print('MONK3')
for a in range(6):
    ag = dtree.averageGain(m3, m.attributes[a])
    print(f'A{a+1} = {ag:.4f}')

# ----------------------------------------------------
# ---- ASSIGNMENT 5 ----------------------------------
# ----------------------------------------------------

m1_1 = dtree.select(m1, m.attributes[1], 1)

tree1 = dtree.buildTree(m1, m.attributes)
tree2 = dtree.buildTree(m2, m.attributes)
tree3 = dtree.buildTree(m3, m.attributes)

e1 = 1 - dtree.check(tree1, m1)
e2 = 1 - dtree.check(tree2, m2)
e3 = 1 - dtree.check(tree3, m3)

e1t = 1 - dtree.check(tree1, m1t)
e2t = 1 - dtree.check(tree2, m2t)
e3t = 1 - dtree.check(tree3, m3t)

# DRAW TREES using PyQt5:
# t1draw = qt5.drawTree(tree1)
# t2draw = qt5.drawTree(tree2)
# t3draw = qt5.drawTree(tree3)

print('')
print('ASSIGNMENT 5')
print('Decision tree errors:')
print(' - E(train)')
print(f'E(train,MONK1) = {e1:.4f}')
print(f'E(train,MONK2) = {e2:.4f}')
print(f'E(train,MONK3) = {e3:.4f}')
print('')
print(' - E(test)')
print(f'E(test,MONK1) = {e1t:.4f}')
print(f'E(test,MONK2) = {e2t:.4f}')
print(f'E(test,MONK3) = {e3t:.4f}')
print('')


# ----------------------------------------------------
# ---- ASSIGNMENT 7 ----------------------------------
# ----------------------------------------------------


def partition(ds, fraction):
    ldata = list(ds)
    rnd.shuffle(ldata)
    breakPoint = int(len(ldata) * fraction)
    return ldata[:breakPoint], ldata[breakPoint:]


def prune(ds, ds_test):
    # fractions = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    fractions = list(np.linspace(0.01, 0.99, 25))

    pruned_trees = []
    pruned_error = []

    for fraction in fractions:
        ds_train, ds_validate = partition(ds, fraction)
        tree = dtree.buildTree(ds_train, m.attributes)
        pruned = dtree.allPruned(tree)

        best_tree = tree
        best_perf = 0

        for t in pruned:
            temp_perf = dtree.check(t, ds_validate)
            if best_perf < temp_perf:
                best_perf = temp_perf
                best_tree = t

        pruned_trees.append(best_tree)
        pruned_error.append(1 - dtree.check(best_tree, ds_test))

    return (pruned_trees, pruned_error)


def pruning_perf():
    m1_prune_error = []
    m2_prune_error = []
    m3_prune_error = []

    m1_pruned = []
    m2_pruned = []
    m3_pruned = []

    for i in range(200):
        # PRUNING FOR TREES AND ERRORS
        m1_prune, m1_p_e = prune(m1, m1t)
        m2_prune, m2_p_e = prune(m2, m2t)
        m3_prune, m3_p_e = prune(m3, m3t)

        # PRUNED TREES
        m1_pruned.append(m1_prune)
        m2_pruned.append(m2_prune)
        m3_pruned.append(m3_prune)

        # ERRORS
        m1_prune_error.append(m1_p_e)
        m2_prune_error.append(m2_p_e)
        m3_prune_error.append(m3_p_e)

    return (m1_prune_error, m2_prune_error, m3_prune_error)


prune_perf = pruning_perf()

m1_pruned = np.transpose(prune_perf[0])
m2_pruned = np.transpose(prune_perf[1])
m3_pruned = np.transpose(prune_perf[2])

mean_m1 = np.around(np.mean(m1_pruned, axis=1), 4)
mean_m2 = np.around(np.mean(m2_pruned, axis=1), 4)
mean_m3 = np.around(np.mean(m3_pruned, axis=1), 4)

std_m1 = np.around(np.std(m1_pruned, axis=1), 4)
std_m2 = np.around(np.std(m2_pruned, axis=1), 4)
std_m3 = np.around(np.std(m3_pruned, axis=1), 4)

print('')
print('ASSIGNMENT 7')
print('Pruning decision trees:')
print(f'Mean MONK1 = {*mean_m1,}')
print(f'Std MONK1 = {*std_m1,}')
print('')
print(f'Mean MONK2 = {*mean_m2,}')
print(f'Std MONK2 = {*std_m2,}')
print('')
print(f'Mean MONK3 = {*mean_m3,}')
print(f'Std MONK3 = {*std_m3,}')
print('')

# ----------------------------------------------------
# ---- PLOT 1 ----------------------------------------
# ----------------------------------------------------
rc('text', usetex=True)
rc('font', size=10)
rc('legend', fontsize=12)

mttl = 'Plot 1'
ttl = 'Mean: Pruning of Decision Trees'
xlbl = 'Fraction'
ylbl = 'Mean error'

# x = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
x = list(np.linspace(0.01, 0.99, 25))
x_ax_lim = [x[0], x[-1]]
f1 = mean_m1
f2 = mean_m2
f3 = mean_m3

fig = plt.figure(mttl, figsize=(10, 7))
# ------------------ #
# ---- PLOTS ---- #
plt.plot(x, f1, label='MONK1', color='tab:blue', linewidth=1)
plt.plot(x, f2, label='MONK2', color='tab:orange', linewidth=1)
plt.plot(x, f3, label='MONK3', color='tab:green')
plt.axhline(y=e1t, color='tab:blue', linestyle='--', linewidth=1)
plt.axhline(y=e2t, color='tab:orange', linestyle='--', linewidth=1)
plt.axhline(y=e3t, color='tab:green', linestyle='--', linewidth=1)
# ---- AXIS ---- #
plt.xlim(x_ax_lim)  # XLIM
# plt.ylim(y_ax_lim)  # YLIM
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
plt.title(ttl, fontsize=14)
plt.xlabel(xlbl, fontsize=12)
plt.ylabel(ylbl, fontsize=12)
# ---- SAVE PLOT ---- #
# plt.savefig('plot1_mean.png', dpi=600)
# plt.savefig('plot1_mean.pdf')
# ---- SHOW PLOT ---- #
plt.show()


# ----------------------------------------------------
# ---- PLOT 2 ----------------------------------------

mttl = 'Plot 2'
ttl = 'Standard deviation: Pruning of Decision Trees'
xlbl = 'Fraction'
ylbl = 'Mean error'

# x = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
x = list(np.linspace(0.01, 0.99, 25))
x_ax_lim = [x[0], x[-1]]
f1 = std_m1
f2 = std_m2
f3 = std_m3

# ------------------ #
# ---- PLOTTING ---- #
fig = plt.figure(mttl, figsize=(10, 7))
# ------------------ #
# ---- PLOTS ---- #
plt.plot(x, f1, label='MONK1', linewidth=1)
plt.plot(x, f2, label='MONK2', linewidth=1)
plt.plot(x, f3, label='MONK3', linewidth=1)
# ---- AXIS ---- #
plt.xlim(x_ax_lim)  # XLIM
# plt.ylim(y_ax_lim)  # YLIM
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
plt.title(ttl, fontsize=14)
plt.xlabel(xlbl, fontsize=12)
plt.ylabel(ylbl, fontsize=12)
# ---- SAVE PLOT ---- #
# plt.savefig('plot2_std.png', dpi=600)
# plt.savefig('plot2_std.pdf')
# ---- SHOW PLOT ---- #
plt.show()
