# Memristor Crossbar Netlist Generator for SPICE Simulator

This python script generates a netlist on a SCS file which is used by the Cadence Virtuoso Spectre to simulate it behavior. The netlist describes a memristor crossbar whose parameteres are user-defined through a separated configuration file (JSON format), while the input pulses are read from another user-defined file (CSV format). The memristor model used by the simulation is the 1T1R model. It considers device-to-device and cycle-to-cycle variability of the memristor. 
The input pulses could be given as row-by-row format, or directly by specifying each cell pulse. The rows of the crossbar (Wordline) are connected to the input pulses, the gates of the transistors are connected to a separated Selectline, while the output current is read along the columns of the crossbar (Bitline). When a single 1T1R cell is written, it's gate voltage is set to a voltage (user-defined), and its column is tied to ground, while all other cells of the same row have the column voltage tied to the set or reset voltage; all other cells of the other rows have the gate voltage set to 0. The different gate voltages allow to store different values to the memristor.
There is no need to specify the size of the crossbar, since it is calculated at run-time by looking at the input pulses.


## Virtual environment & run test

A set-up should be run with this following two commands. The first one deletes previously generated temporary files, install the required packages by using the requirements.txt file and creates a Virtual environment. The second command runs the Virtual environment and loads the module necessary for running the simulation. Finally, for testing the functioning of the script we use predefined configuration and input files in the sample folder.

``` bash
make
source script.sh
python main.py sample
```

## Set-up

### Settings file

First of all the configuration file (settings.json inside configs folder) should be edited:
#### Simulation parameters
The first parameter (input type) allows to choose how the user configurates the crossbar. There are 3 options:
1. (1) Cell by cell: the input pulses are given one by one for each cell on the cell_input.csv file; multiple memristor states are allowed by specifying different gate voltages;
2. (2) Row by row: the input pulses are given for each row of the corssbar on the row_input.csv file; multiple memristor states are allowed by specifying different gate voltages;
3. (3) Parallel binary operation: the same as the row access, but the Set and Reset operations are in parallel hence the memristors could only be set to High set or reset to Low set (binary)

Then the user could change the type of simulation ("tran" is the default one), the max step, the step time, the period and the time units. The stop time is not specified since the script calculates it at run-time. The last 4 parameters could not be changed unless necessary.
#### Crossbar parameter
The memristor and transistor model names are specified, which can be found on the deps folder. 
Define the Read, Set and Reset voltage levels given to the 1T1R cells. The Gate voltage level is used to select which row (or Word Line) to activate and for having different memristor states. Ndiscmin, Ndiscmax, ldet, rdet are booleans which allow to select which parameter/s will be affected by a cycle-to-cycle or device-to-device variability. Those parameters are the Minimum and the maximum oxygen concentration in the disc (Ndiscmin and Ndiscmax), the Radius of the filament (rvar) and Length of the disc (lvar). Finally, the user could add more parameters for the memristor. For example, the Rth0 parameter (thermal resistance of the Hafnium Oxide) can be changed and should be in the range between 1.5e7 and 2e7 in order to make the memristor function properly (different behaviours can be tested).
#### Gate sweep
Those parameters allow the user to sweep the Gate voltage between a minimum and a maximum value, with a defined step. Those parameters will be ignored only when the min and max values are set to 0. In this case, the Gate voltage given previously is used.


## Input pulses example

### Cell by cell 
If the cell on position 0,0 (first row first column) has to be read, and the other in position 1,0 has to be set:
1. Read,0,0
1. Set,1,0
Furthemore, if the cell should have a different gate voltage (for example multiple bit encoding), the voltage should be specified as third number. For example, if the cell 0,0 should have a gate voltage of 1.3 V, the command is:
1. Set,0,0,1.3
In the case the gate voltage is not specified, the gate voltage given on the settings.json file will be used.

### Row by row 
The format is as this: the first value is a character which is "w" if we want write, or "r" if we want to read. The second value is the row number. From the third value we specify 0 if the respective cell has to be reset, otherwise it has to be set with the specified gate voltage. For example, if we want to access the row 1 by setting the first cell with a gate voltage of 0.9 V and the third cell with a gate voltage of 1.3 V, and resetting the second and fourth cell, the appropriate command to write is:
1. W,1,0.9,0,1.3,0

### Parallel binary
The format is the same as of the row by row, but the gate voltage remains always the same in order in order to have binary states and to access the cells of the same row in parallel. All the set operation and the reset operation of the same row are done in parallel. For example, if we want to encode the number 10 and the number 7 in binary:
1. W,0,1,0,1,0  
2. W,1,0,1,1,1

## Simulation output
To run the script with the customized setting and input files:
``` bash
python main.py
```
The appropriate netlist is written to an .scs file (netlist.scs) and it runs automatically the spectre simulator.
To visualize the output waveforms, run:
``` bash
viva -datadir netlist.raw
```
The output current for the 1TR1 cell at position (0,0), for example, is I0:OE.
