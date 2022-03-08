from src.autospice.ckt_gen import netlist_design
import json
import pandas as pd
import os

"""
This is the main function which defined the flow of code by calling different classes in it.
"""
print()

out_file_name = "netlist.scs" # file name of netlist
memristor_model_path = os.getcwd() + '/deps/JART-memristor-models/' # change this path according to local path
transistor_model_path = os.getcwd() + '/deps/transistor-models/'
ckt = netlist_design()  # object of the netlist class

mean_sigma = { "Ndiscmin": (8e-03, 2e-3), "Ndiscmax": (20, 1), "lnew": (0.4, 0.04), "rnew": (45e-09, 5e-09)}	# mean and sigma of each variablity parameter

static_param_sim = " eps = 17 epsphib = 5.5 Ndiscmin=0.008"	# static parameters which are required for internal calculation

# static parameters value. 
static_param = {"T0":0.293,"eps": 17,"epsphib":5.5,"phiBn0":0.18, "phin":0.1,"un":4e-06,
		 "Ndiscmax":20,"Ndiscmin": 0.008,"Ninit": 0.008, "Nplug": 20,
		 "a": 2.5e-10,"ny0": 2e+13, "dWa": 1.35, "Rth0": 10e+06,
		 "rdet": 45e-09, 'lcell': 3, 'ldet': 0.4,
		 "Rtheff_scaling": 0.27, "RseriesTiOx": 650, "R0": 719.244,
	     'Rthline': 90471.5, 'alphaline': 0.00392}


single_mode, xbar_mode = False, False
params_read = 0 # number of parameters read on the csv format file
volt_r, volt_c = [], [] # manual pulses

read_v, set_v, reset_v = 0,0,0

with open('config.json', 'r') as f:
	config = json.load(f)

	rows, columns = config['xbar_size']['rows'], config['xbar_size']['columns']	# read rows and columns

	nmin_b, nmax_b, ldet_b, rdet_b = config['var_bools']['ndiscmin'], config['var_bools']['ndiscmax'], config['var_bools']['ldet'], config['var_bools']['rdet']	# create dict with variability params bools

	sim_type, stop_time, max_step = config['sim_params']['type'], config['sim_params']['stop_time'], config['sim_params']['max_step']	# tune the simulation parameters  - duration of simulation and step you want to take

	memristor_model_path += config['sim_params']['memristor_model_file']

	transistor_model_path += config['sim_params']['transistor_model_file']

	read_v, set_v, reset_v = config['sim_params']['read_v'], config['sim_params']['set_v'], config['sim_params']['reset_v']



ckt.set_xbar_params(rows, columns, read_v, set_v, reset_v)
ckt.set_simulation_params(sim_type, stop_time, max_step)
var_bools = ckt.set_variablity(Nmin = nmin_b, Nmax = nmax_b, ldet = ldet_b, rdet = rdet_b)	# creates a dict for checking if the variabilities for each parameters are set
var_param = ckt.update_param(static_param_sim, mean_sigma, var_bools)	# update the parameters of the memristors in case the var_bools are set

#check if single memristor or xbar to read appropriate csv file
if rows>1 or columns>1: xbar_mode = True #crossbar
else: single_mode = True #single memristor (rows=columns=1)


if single_mode:
	csv_pulses = pd.read_csv('pulses_single.csv',header=None)
	in_pulses_list = csv_pulses.values.tolist()[0]
	ckt.gen_netlist_single(static_param, in_pulses_list, out_file_name, memristor_model_path, transistor_model_path)	# create spectre netlist using the parameters set before and the static and variab parameters


else:
	print("TO DO")
	#to do, xbar...

	# cross_bar = ckt.set_cross_bar_params(rows, columns)	# set xbar size

	# ckt.set_input_voltages(volt_r, volt_c)	# set input voltages using the list read by the file

	# #ckt.create_set_reset_pulses(-0.75, 1.5, 0.2)	# parameters: set, reset, read voltages



# netlist = ckt.design_ckt(var_param, static_param)	# create spectre netlist using the parameters set before and the static and variab parameters

# ckt.set_simulation_params(sim_type, stop_time, max_step) # tune the simulator

# ckt.write_into_file(out_file_name, memristor_memristor_model_path, netlist)	# write the netlist and the sim configutation into the scs file 
