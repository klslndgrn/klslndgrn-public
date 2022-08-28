# Assignment 2 - EH2745

## Author

Klas Lindgren

## Subject

The second assignment involves creating a k-Means Clustering and a k-Nearest
Neighbor algorithm to analyze a small power system using the Pandapower toolbox.

## PLEASE NOTE THAT

This project is either started in "main.py" without GUI, or "mainGUI.py" to
start with GUI.

This file requires iGraph (pip install igraph) to show the grid with a
visual presentation.

## File Descriptions

### main.py and mainGUI.py (with GUI_prerequisites.py)

"main.py" contains the main structure of the program.

"mainGUI.py" is the file that runs "main.py" but with a user GUI. "mainGUI.py"
needs to be runned for the GUI to appear. A few prerequisites for the GUI is
defined in "GUI_prerequisites.py"

Descriptions of the other files can be found below.

### grid.py

In this file the grid is created using the PandaPower toolbox.

### data.py

In this file all data for the power system is created. Including the time-
series calculations.

### output.py

In this file all functions that include creating outputs are created.

### kmc.py

This file is the main file for the k-Means Clustering (kMC) algorithm.

### kmc_data.py

This file contains all sub-functions for the kMC algorithm.

### test_data.py

This file contains the functions that initializes the test-functions.

### knn.py

This file is the main file for the k-Nearest Neighbor (kNN) algorithm.

### kclasses.py

This file contains all the classes used. This includes the clusters and the
datapoints.
