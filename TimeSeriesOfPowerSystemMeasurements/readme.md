# Assignment 2 - EH2745

## Author

Klas Lindgren

## Subject

The second assignment involves ... a small power system using the Pandapower toolbox.
You are then tasked with ... and analyzing it to generate a ....

## PLEASE NOTE THAT

This project is either started in "main.py" without GUI, or "mainGUI.py" to
start with GUI.

This file requires iGraph (pip install igraph) to show the grid with a
visual presentation.

## File Descriptions

### main.py and mainGUI.py (with GUI_prerequisites.py)

"main.py" contains the main structure of the program. Which includes a function
that retreivs equipment data from an EQ XML-file, create_data_lists(), and
another function that updates these equipments based on a SSH XML-file,
update_data_lists(). This file also contains a function, grid_initializer(),
that creates buses and nodes from conducting equipment "BusBars" and remaining
nodes from connectivity nodes. Furthermore the grid_creator() function creates
the rest of the grid.

"mainGUI.py" is the file that runs "main.py" but with a user GUI. "mainGUI.py"
needs to be runned for the GUI to appear. A few prerequisites for the GUI is
defined in "GUI_prerequisites.py"

Descriptions of the other files can be found below.

### psclasses.py

This file contains the first and second layer of PowerSystemEquipment classes.
This file initializes the main class "PSEquipment" and it's three sub-classes
or children. These are the Terminal class, the ConnectivityNode class and the
ConductingEquipment class.

### ceclasses.py

This file contains the third layer of PowerSystemEquipment classes. Only the
ConductingEquipment (CE) class has children. Here is a class defined for each
CE.

### eqread.py

This file contains the program which loads and extracts information from the
Equipment (EQ) XML-files. This file contains the functions that deal with the
information regarding all equipment of the grid.

### sshread.py

This file contains the program which loads and extracts information from the
SteadyStateHypotesis (SSH) XML-files. This file contains functions that deal
with the information and statuses of some of the equipment in the grid.

### grid.py

This file utilizes PandaPower to define functions that are able to create
equipment in an PandaPower transmission grid. This file also contains functions
that create the initial empty grid, finds PandaPower grid indices for each
equipment based on the Terminal ID's of all equipment. Finally, this file also
contains the function that plots the grid using SimplePlot and iGraph.

### gridcreator.py

Finally, this file contains functions that utilizes the functions in "grid.py",
and creats the grid. There is an initial function that creates busbars and
nodes from "CE - BusBars" and CN's, respectively. When all busbars and nodes
are created, the CE can be connected to these busbars and nodes and the final
grid is created. As every PowerSystemEquipment class variable is processed the
status for each individual object is set to True using a flag function. There
is also a function that verifies that all inserted equipment has been processed
and used to create the grid. This is used as an output for both "main.py" and
"mainGUI.py". Finally, there is a function that converts terminal output to
strings to be printed in the GUI. This contains information for the entire grid
in detail.
