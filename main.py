'''
    Main python file
'''
import json
import csv
import os
#import time
import sys
from src.netlist_gen import netlist_design

CONFIG_FILEPATH = "config.json"
PULSES_INPUT_FILEPATH = "cell_input.csv"
ROW_INPUT_FILEPATH = "row_input.csv"
OUT_FILE_NAME = "netlist.scs"
memristor_model_path = os.getcwd() + '/deps/memristor-models/'
transistor_model_path = os.getcwd() + '/deps/transistor-models/'
circuit = netlist_design()

mean_sigma = {"Ndiscmin": (8e-03, 2e-3), "Ndiscmax": (20, 1), "lnew": (0.4, 0.04), "rnew": (45e-09, 5e-09)}	

memristor_params = {}

print("\n***********************************************")

if len(sys.argv) > 1 and str(sys.argv[1]) == 'sample':
    CONFIG_FILEPATH = "sample/" + CONFIG_FILEPATH
    PULSES_INPUT_FILEPATH = "sample/" + PULSES_INPUT_FILEPATH
    ROW_INPUT_FILEPATH = "sample/" + ROW_INPUT_FILEPATH
    print("Sample used.\n")



with open(CONFIG_FILEPATH, 'r', encoding="utf-8") as file:
    config = json.load(file)

    input_type = config['input_type']['row_by_row']

    sim_params = config["sim_params"]
    sim_type, step_time, period, max_step, time_units = sim_params['type'], sim_params['step_time'], sim_params['period'], sim_params['max_step'],sim_params['time_units']

    vabstol, iabstol, temp, tnom, gmin = sim_params['vabstol'], sim_params['iabstol'], sim_params['temp'], sim_params['tnom'], sim_params['gmin']

    crossbar_params = config["crossbar_params"]

    memristor_model_path += crossbar_params['memristor_model_file']
    transistor_model_path += crossbar_params['transistor_model_file']
    read_v, set_v, reset_v, gate_v = crossbar_params['read_v'], crossbar_params['set_v'], crossbar_params['reset_v'], crossbar_params['gate_v']
    nmin_b, nmax_b, ldet_b, rdet_b = crossbar_params['ndiscmin'], crossbar_params['ndiscmax'], crossbar_params['ldet'], crossbar_params['rdet']	
    transistor_lenght, transistor_width = crossbar_params["transistor_length"], crossbar_params["transistor_width"]

    crossbar_params = list(crossbar_params.items())

    if len(crossbar_params) > 12:
        for i in range(12, len(crossbar_params)):
            memristor_params[crossbar_params[i][0]] = crossbar_params[i][1]
            #Rth0 = 1.572e7


    gate_sweep = config['gate_sweep']
    if gate_sweep['min_v'] == 0 and gate_sweep['max_v'] == 0:
        sweep_params = []
    else:
        min_gate = gate_sweep['min_v']
        max_gate = gate_sweep['max_v']
        step_gate = gate_sweep['step_v']
        sweep_params = [min_gate, max_gate, step_gate]		


if input_type == 1 or input_type == 2:
    with open(ROW_INPUT_FILEPATH, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        row_pulses_list = list(filter(None,reader))
        circuit.pulses_to_file(row_pulses_list, PULSES_INPUT_FILEPATH)

with open(PULSES_INPUT_FILEPATH, 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    in_pulses_list = list(filter(None,reader))
if not in_pulses_list:
    print("No pulses input! Terminating program...")
    sys.exit()


circuit.calculate_xbar_size(in_pulses_list)
circuit.set_crossbar_params(read_v, set_v, reset_v, gate_v, transistor_lenght, transistor_width, input_type)
circuit.set_simulation_params(sim_type, step_time, period, max_step, time_units, vabstol, iabstol, temp, tnom, gmin, in_pulses_list)

var_bools = circuit.set_variablity(Nmin = nmin_b, Nmax = nmax_b, ldet = ldet_b, rdet = rdet_b)	
var_param = circuit.update_param(mean_sigma, var_bools)	

circuit.gen_netlist(memristor_params, in_pulses_list, sweep_params, OUT_FILE_NAME, memristor_model_path, transistor_model_path)	

'''
input("Press Enter to run the simulation.\n")
print("Running simulation...")
print("***********************************************\n")
time.sleep(1.5)
os.system(f"spectre {OUT_FILE_NAME}")
'''

