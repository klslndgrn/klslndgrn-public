# Assignment 1 - EH2745

## Author

Klas Lindgren

## Subject

The first assignment involves reading and parsing a CIM data file
representing a small power system. You are then tasked with storing the data
and analyzing it to generate a model of the grid using the Pandapower toolbox.

## PLEASE NOTE THAT

This file requires iGraph (pip install igraph).

## File Descriptions

### main.py and mainGUI.py

"main.py" contains the main structure of the program. Which includes a function
that retreivs equipment data from an EQ XML-file, create_data_lists(), and
another function that updates these equipments based on a SSH XML-file,
update_data_lists(). This file also contains a function, grid_initializer(),
that creates buses and nodes from conducting equipment "BusBars" and remaining
nodes from connectivity nodes.

"mainGUI.py" is the file that runs "main.py" but with a user GUI. "mainGUI.py"
needs to be runned for the GUI to appear.

Descriptions of the other files can be found below.

### psclasses.py

This file ....

### ceclasses.py

This file ....

### eqread.py

This file contains the program which loads and extracts information from the XML-files.

### grid.py

This file .... PandaPower functions.
