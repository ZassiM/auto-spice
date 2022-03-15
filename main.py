from src.ckt_gen import netlist_design
import json
import csv
import os
import time

out_file_name = "netlist.scs" 
memristor_model_path = os.getcwd() + '/deps/JART-memristor-models/' 
transistor_model_path = os.getcwd() + '/deps/transistor-models/'
ckt = netlist_design()  

mean_sigma = { "Ndiscmin": (8e-03, 2e-3), "Ndiscmax": (20, 1), "lnew": (0.4, 0.04), "rnew": (45e-09, 5e-09)}	

static_param_sim = " eps = 17 epsphib = 5.5 Ndiscmin=0.008"	

 
static_param = {"T0":0.293,"eps": 17,"epsphib":5.5,"phiBn0":0.18, "phin":0.1,"un":4e-06,
		 "Ndiscmax":20,"Ndiscmin": 0.008,"Ninit": 0.008, "Nplug": 20,
		 "a": 2.5e-10,"ny0": 2e+13, "dWa": 1.35, "Rth0": 1.5e7,
		 "rdet": 45e-09, 'lcell': 3, 'ldet': 0.4,
		 "Rtheff_scaling": 0.27, "RseriesTiOx": 650, "R0": 719.244,
	     'Rthline': 90471.5, 'alphaline': 0.00392}

with open('config.json', 'r') as file:
	config = json.load(file)

	nmin_b, nmax_b, ldet_b, rdet_b = config['var_bools']['ndiscmin'], config['var_bools']['ndiscmax'], config['var_bools']['ldet'], config['var_bools']['rdet']	

	sim_type, step_time, max_step, time_units = config['sim_params']['type'], config['sim_params']['step_time'], config['sim_params']['max_step'], config['sim_params']['time_units']

	memristor_model_path += config['sim_params']['memristor_model_file']

	transistor_model_path += config['sim_params']['transistor_model_file']

	read_v, set_v, reset_v, gate_v = config['sim_params']['read_v'], config['sim_params']['set_v'], config['sim_params']['reset_v'], config['sim_params']['gate_v']

	Rth0 = config['sim_params']['Rth0']

	if config['gate_sweep']['min_v'] == 0 and config['gate_sweep']['max_v'] == 0:
		print("No sweeping of the gate voltage.\n")
		sweep_params = []

	else:
		min_gate = config['gate_sweep']['min_v']
		max_gate = config['gate_sweep']['max_v']
		step_gate = config['gate_sweep']['step_v']

		sweep_params = [min_gate, max_gate, step_gate]		



with open('pulses.csv', 'r') as file:
    reader = csv.reader(file)
    in_pulses_list = list(filter(None,reader))
    

ckt.calculate_xbar_size(in_pulses_list)
ckt.set_xbar_params(read_v, set_v, reset_v, gate_v)
ckt.set_simulation_params(sim_type, step_time, max_step, time_units, in_pulses_list)

var_bools = ckt.set_variablity(Nmin = nmin_b, Nmax = nmax_b, ldet = ldet_b, rdet = rdet_b)	
var_param = ckt.update_param(static_param_sim, mean_sigma, var_bools)	

static_param["Rth0"] = Rth0
ckt.gen_netlist(static_param, in_pulses_list, sweep_params, out_file_name, memristor_model_path, transistor_model_path)	

# print("Running simulation...")
# time.sleep(1.5)
# os.system('module load cadence-flow/mixed-signal/2020-21')
# os.system(f'spectre {out_file_name}')
