# Crossbar netlist generator for SPICE simulator

This python script generates a netlist on a SCS file which can be used by the Cadence Virtuoso Spectre to simulate it behavior. The netlist describes a memristor crossbar whose parameteres are user-defined through a separated config file (CSV format). The memristor model used by the simulator is written with Verilog-A (JART VCM V1b var, see description here http://www.emrl.de/JART.html#Artikel_4). It considers device-to-device and cycle-to-cycle variability.
At the moment, you can define the xbar size (rows, columns), the variability parameters, the simulation parameters and the input pulses for each row and column.

## Set-up

### Virtual environment

To create/activate your venv run.

``` bash
make
source source_me.sh
```

## Usage

How to generate netlist:
1. Open the config.json file.
1. Input the preferred parameters values (xbar size, variability parameters, etc), save the file.
1. Open the pulses.csv file.
1. Enter the voltage pulses characteristics, the row and columns pulses are separated by an empty row. Save the file.
1. Run the main.py script
The netlist is written to the file "netlist.scs".

How to run the spectre simulator via terminal:
1. Open a terminal on a ICE machine.
1. Load the Cadence module: 
``` bash 
module load cadence-flow/mixed-signal/2020-21'. 
```
1. Enter to the directory which contains the SCS file.
1. Run the simulator:
``` bash 
'spectre netlist.scs'.
```

You'll get the simulation results via textual information, and a .raw file is generated which can be used to visualize the waveforms.

To visualize the output waveforms, run:
``` bash
viva -datadir netlist.raw
```
