from src.autospice.parameters import parameters
from src.autospice.gauss_var import gauss_dist
import numpy as np

class netlist_design(parameters):

	def __init__(self):
		parameters.__init__(self)
		if self.memristor_model == "JART_VCM_1b_det":  
			self.static_parameters = " T0=T0 eps=esp epsphib=epsphib phiBn0=phiBn0 phin=phin un=un Nplug=Nplug \ \n a=a ny0=ny0 dWa=dWa Rth0=Rth0 Ninit=Ndiscmin rdet=rdet lcell=lcell \ \n ldet=ldet Rtheff_scaling=Rtheff_scaling RseriesTiOx=RseriesTiOx R0=R0 \ \n"
			self.variablity = "Ndiscmax={} Ndiscmin={} rdet={} ldet={}" 
		else:    
			self.static_parameters = " eps=eps epsphib=epsphib phibn0=phibn0 phin=phin \ \n un=un Ninit=Ndiscmin Nplug=Nplug a=a \ \n nyo=nyo dWa=dWa Rth0=Rth0 rdet=rdet  \ \n lcell=lcell ldet=ldet Rtheff_scaling=Rtheff_scaling RTiOx=RTiOx R0=R0 \ \n Rthline=90471.5 alphaline=0.00392 eps_eff=(eps)*(8.85419e-12) \ \n epsphib_eff=(epsphib)*(8.85419e-12)"
			self.variablity = " Ndiscmax={} Ndiscmin={} lnew = {} rnew= {} " 

	def design_voltage_sources(self):

		num_volt_source = 0
		voltages_name = ""
		vpulse = "V{} ({} {}) vsource type={} val0={} val1={} period={} width={} rise={} fall={} \n" 
		voltage_source = ""
		for i in range(self.rows):
			voltages_name += "r{} ".format(i)
			voltage_source += vpulse.format(str(num_volt_source),"r{} ".format(i),0, self.input_type_r[i], self.volt_0_r[i],self.volt_1_r[i], self.time_period_r[i], self.pulse_width_r[i], self.rise_time_r[i],self.fall_time_r[i])
			num_volt_source += 1
		for j in range(self.columns):
			voltages_name += f"c{j} "
			voltage_source += vpulse.format(str(num_volt_source),"c{} ".format(j),0, self.input_type_c[j], self.volt_0_c[j],self.volt_1_c[j], self.time_period_c[j], self.pulse_width_c[j], self.rise_time_c[j],self.fall_time_c[j])
			num_volt_source += 1
		return voltages_name,voltage_source


	def update_param(self, static_param = "", mean_sigma_param = {}, bools_var = {}):

		var_param = "parameters "
		d_to_d_vardict = {}
		gauss = gauss_dist((self.rows,self.columns))

		for variation in bools_var:
			if bools_var[variation]:
				d_to_d_vardict[variation] = gauss_dist(mean_sigma_param[variation]).create_distribution((self.rows,self.columns))

		
		if(len(d_to_d_vardict) == 0):
			print("No random variations.\n")
		else:
			var_param += gauss.make_paramset(d_to_d_vardict) 
			print(f"{len(d_to_d_vardict)} parameters are updated due to variation.\n")
	
		var_param += static_param 
		return var_param


	def create_pulse(self, step_time, pulse_vol, time_unit, pulses, idx):
    
		insert_p = False
		concatenated = False
	
		if not pulses[idx]:	
			start_time = 0
			stop_time = 3000
			concatenated = False

		else:
			start_time = int(pulses[idx][-2][:-1])+1 
			stop_time = start_time + 2000
			concatenated = True
		
		for i in range(start_time, stop_time, step_time):

			if insert_p == False and concatenated == False:
				pulses[idx].append(str(i)+time_unit)
				pulses[idx].append('0')
				pulses[idx].append(str(i+(step_time-1))+time_unit)
				pulses[idx].append('0')
				insert_p = True
				
			else:
				pulses[idx].append(str(i)+time_unit)
				pulses[idx].append(pulse_vol)
				pulses[idx].append(str(i+(step_time-1))+time_unit)
				pulses[idx].append(pulse_vol)
				insert_p = False
				concatenated = False


	def pulses_to_string(self, in_pulses_list):

		pulses = [[] for _ in range(self.rows*self.columns)]

		for s in in_pulses_list:
			pulse_str = s[0:s.find('(')]
			pulse_idx = s[s.find('(')+1:s.find(')')]
			pulse_idx = pulse_idx.split(",")
			row,column = int(pulse_idx[0]), int(pulse_idx[1])
			idx = self.columns*row + column

			if pulse_str.lower() == "read":
				self.create_pulse(1000, "Read_V", self.time_units, pulses, idx)
				
			elif pulse_str.lower() == "set":
				self.create_pulse(1000, "Set_V", self.time_units, pulses, idx)

			elif pulse_str.lower() == "reset":
				self.create_pulse(1000, "Reset_V", self.time_units, pulses, idx)
			
		if not pulses:
			print("Empty list!")
			return
		
		pulses_str = ""
		c = 0
		for i in range(0, self.rows):
			for j in range(0, self.columns):
				pulses_str += f"V{c} (r{i} c{j}) vsource type=pwl wave=[\\\n"
				for k in range(0, len(pulses[self.columns*i + j])-1, 2):
					pulses_str += pulses[self.columns*i + j][k] + '\t' + pulses[self.columns*i + j][k+1] + '\t\\\n'
				pulses_str += ']\n\n'
				c += 1

		return pulses_str


	def gen_netlist(self,static_param= {}, pulses = [], file_name = "", memristor_model_path = "", transistor_model_path = ""):

		print("Generating netlist...\n")

		str_param = ""
		str_ckt = ""
		str_instances = ""
		str_pulses = ""

		str_param += "global 0\n"
		str_param += "ahdl_include " + "\"" + memristor_model_path + "\"" + "\n"
		str_param += "ahdl_include " + "\"" + transistor_model_path + "\"" + "\n" 
		str_param += "simulatorOptions options vabstol=1e-6 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12\n"
		str_param += f"trans {self.simulation_type} stop={self.simulation_stop_time} errpreset=conservative maxstep ={self.simulation_maxstep}\n"
		str_param += f"saveOptions options save=all currents=all saveahdlvars=all\n"
		#str_param += f"save {ckt_name}.I0:OE {ckt_name}.I0:AE\n"
		str_param += f"parameters Read_V = {self.read_v} Set_V = {self.set_v} Reset_V = {self.reset_v}\n"
		str_param += "parameters " + self.parameters_list(param=static_param) + "\n\n\n"

		str_ckt += "subckt 1T1M_ckt MemInput Output TransGate inh_bulk_n\n"
		str_ckt += f"\tM0 (net03 MemInput) {self.memristor_model}"
		str_ckt += "\t" + self.parameters_list(param=static_param, numerical_mode = False) + "\n"
		str_ckt += f"\tT0 (net03 TransGate Output inh_bulk_n) {self.transistor_model}\n"
		str_ckt += "ends 1T1M_ckt\n\n\n"

		k = 0
		for i in range(0, self.rows):
			for j in range(0, self.columns):
				str_instances += f"I{k} (c{j} 0 r{i} 0) 1T1M_ckt\n"
				k += 1

		str_pulses += "\n\n" + self.pulses_to_string(pulses)
		#str_pulses += "\nV1 (c0  0) vsource dc=0\n\n\n"

		to_be_written = str_param + str_ckt + str_instances + str_pulses
		file_ = open(file_name,"w")
		file_.write(to_be_written)
		print(f"Netlist, model path and simulation parameters written to \"{file_name}\"\n")
		