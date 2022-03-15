# Crossbar netlist generator for SPICE simulator

This python script generates a netlist on a SCS file which is used by the Cadence Virtuoso Spectre to simulate it behavior. The netlist describes a memristor crossbar whose parameteres are user-defined through a separated configuration file (JSON format), while the input pulses are read from another user-defined file (CSV format). The memristor model used by the simulation is the 1T1R model. It considers device-to-device and cycle-to-cycle variability of the memristor. 
The input pulses could be given as row-by-row format, or directly by specifying each cell pulse. The rows of the crossbar (Wordline) are connected to the input pulses, the gates of the transistors are connected to a separated Selectline, while the output current is read along the columns of the crossbar (Bitline). When a single 1T1R cell is written, it's gate voltage is set to a high voltage (user-defined), and its column is tied to ground, while all other cells of the same row have the column voltage tied to the set or reset voltage; all other cells of the other rows have the gate voltage set to 0.
## Set-up

### Virtual environment

To create/activate your venv run.

``` bash
make
source source_me.sh
```

## Usage

First of all the configuration file (config.json) should be edited:
1. Simulation parameters: the first parameter (row_by_row) contains a bool which must be activated when the user wants to give row-by-row input to the rw_input.csv file. Otherwise, the user gives the input pulses one by one to each cell to the pulses.csv file.
Then the user could change the type of simulation ("tran" is the default one), the max step, the step time and the time units. The stop time is not specified since the script calculates it dynamically. The memristor and transistor model names are specified, which can be found on the deps folder. The Rth0 parameter (thermal resistance of the Hafnium Oxide) can be changed and should be in the range between 1.5e7 and 2e7 in order to make the memristor function properly (different behaviours can be tested).
2. Pulse voltages: define the Read, Set and Reset voltage levels given to the 1T1R cells. The Gate voltage level is used to select which row (or Word Line) to activate.
3. Gate sweep: those parameters allow the user to sweep the Gate voltage between a minimum and a maximum value, with a defined step. Those parameters will be ignored only when the min and max values are set to 0. In this case, the Gate voltage given previously is used.
4. Var bools: those bools allow to select which parameter/s will be affected by a cycle-to-cycle or device-to-device variability. Those parameters are the Minimum and the maximum oxygen concentration in the disc (Ndiscmin and Ndiscmax), the Radius of the filament (rvar) and Length of the disc (lvar)

If the user decided to give the pulses directly (i.e when row_by_row is set to 0), then the inputs should be written to the pulses.csv file by specifying the operation and the cell index (case-insensitive). For example, if the cell in position 0,0 has to be read, while the cell in position 1,0 has to be set, the appropriate commands are:
1. Read,0,0
1. Set,1,0

If, insted, the row_by_row parameter is set to 1, the script will generate automatically the appropriate list of pulses to pulses.csv after reading the user-given row inputs in rw_input.csv file. The format is as this: the first value is a character which is "w" if we want write, or "r" if we want to read. The second value is the row number. From the third value we specify 0 if the respective cell has to be reset, or 1 if set. For example, if we want to access the row 1 by setting the first and third cell, and resetting the second and fourth cell, the appropriate command to write is:
1. w,1,1,0,1,0
The script will then convert this to a series of pulses.

When the script is run, the appropriate netlist is written to an .scs file (netlist.scs) and it runs automatically the spectre simulator.
To visualize the output waveforms, run:
``` bash
viva -datadir netlist.raw
```
The output current for the 1TR1 cell at position (0,0), for example, is I0:OE. 