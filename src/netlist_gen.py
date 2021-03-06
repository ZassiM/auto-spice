from tracemalloc import stop
from src.netlist_params import parameters
from src.gauss_var import gauss_dist
import numpy as np

class netlist_design(parameters):

	def __init__(self):
		parameters.__init__(self)
		if self.memristor_model == "JART_VCM_1b_det":  
			self.memristor_paramseters = " T0=T0 eps=esp epsphib=epsphib phiBn0=phiBn0 phin=phin un=un Nplug=Nplug \ \n a=a ny0=ny0 dWa=dWa Rth0=Rth0 Ninit=Ndiscmin rdet=rdet lcell=lcell \ \n ldet=ldet Rtheff_scaling=Rtheff_scaling RseriesTiOx=RseriesTiOx R0=R0 \ \n"
			self.variablity = "Ndiscmax={} Ndiscmin={} rdet={} ldet={}" 
		else:    
			self.memristor_paramseters = " eps=eps epsphib=epsphib phibn0=phibn0 phin=phin \ \n un=un Ninit=Ndiscmin Nplug=Nplug a=a \ \n nyo=nyo dWa=dWa Rth0=Rth0 rdet=rdet  \ \n lcell=lcell ldet=ldet Rtheff_scaling=Rtheff_scaling RTiOx=RTiOx R0=R0 \ \n Rthline=90471.5 alphaline=0.00392 eps_eff=(eps)*(8.85419e-12) \ \n epsphib_eff=(epsphib)*(8.85419e-12)"
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

	def update_param(self, mean_sigma_param = {}, bools_var = {}):

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
	
		
		return var_param

	def pulses_to_file(self, row_list, filename):

		if not row_list:
			print("Empty list")
			return
		
		with open(filename,'w') as fl:
			for s in row_list:
				cmd = s[0]
				row = s[1]

				if cmd.lower() == "w":
					for i in range(2, len(s)):
						if s[i] == '0':
							fl.write(f"Reset,{row},{i-2}\n")
						else:
							fl.write(f"Set,{row},{i-2},{s[i]}\n")

				elif cmd.lower() == "r":
					for i in range(2, len(s)):
						if s[i] == '1':
							fl.write(f"Read,{row},{i-2}\n")

				fl.write('\n')
				
		with open(filename) as fl:
			data = fl.read().rstrip('\n')
		with open(filename, "w") as fl:
			fl.write(data)

	def append_pulse(self, pulse_list, idx, value, time, step):
		pulse_list[idx].append(str(time) + self.time_unit)
		pulse_list[idx].append(value)
		pulse_list[idx].append(str(time+(step-1))+ self.time_unit)
		pulse_list[idx].append(value)
		
	def update_pulses(self, pulse_vol, WL_pulses, SEL_voltage, BL_voltage, cells, row, gate_level):

		insert_zeros = False
		concatenated = False

		if len(WL_pulses[row]) == 4:	
			start_time = self.period
			if self.period > self.step_time: stop_time = 2*self.period - self.step_time
			else:  stop_time = 2*self.step_time
			insert_zeros = True

		else:
			start_time = int(WL_pulses[row][-2][:-1])+1 
			stop_time = start_time + self.step_time * 2
			concatenated = True	
			

		for t in range(start_time, stop_time, self.step_time):



			if insert_zeros == False and concatenated == False:

				for k in range(0,self.rows):
					if k != row:
						self.append_pulse(WL_pulses, k, '0', t, self.period)

				self.append_pulse(WL_pulses, row, '0', t, self.period)

				for k in range(0, self.columns):
					self.append_pulse(BL_voltage, k, '0', t, self.period)

				for k in range(0, self.rows):
					self.append_pulse(SEL_voltage, k, '0', t, self.period)

				insert_zeros = True
				concatenated = True		
				

			else:

				for k in range(0,self.rows):
					if k != row:
						self.append_pulse(WL_pulses, k, '0', t, self.step_time)

				self.append_pulse(WL_pulses, row, pulse_vol, t, self.step_time)

				for k in cells:
					self.append_pulse(BL_voltage, k, '0', t, self.step_time)

				if gate_level == None:
					self.append_pulse(SEL_voltage, row, 'Gate_V', t, self.step_time)

				else:
					self.append_pulse(SEL_voltage, row, gate_level, t, self.step_time)
		
				for k in range(0, self.columns):
					if k not in cells:
						self.append_pulse(BL_voltage, k, pulse_vol, t, self.step_time)
						
				insert_zeros = False
				concatenated = False
		
	def pulses_to_string(self,cell_pulses_list):

		WL_pulses = [[] for _ in range(self.rows)]
		SEL_voltage = [[] for _ in range(self.rows)]
		BL_voltage = [[] for _ in range(self.columns)]

		for k in range (0, self.columns):
			self.append_pulse(BL_voltage, k, '0', 0, self.period)

		for k in range (0,self.rows):
			self.append_pulse(SEL_voltage, k, '0', 0, self.period)
			self.append_pulse(WL_pulses, k, '0', 0, self.period)


		if self.input_type == 1:	#cell by cell with multiple state
			
			for s in cell_pulses_list:
				if s:
					row,column = int(s[1]), int(s[2])
					column = [column]
					gate_level = None
					if len(s) > 3:
						gate_level = s[3]

					if s[0].lower() == "read":
						self.update_pulses("Read_V", WL_pulses, SEL_voltage, BL_voltage, column, row, gate_level)

					elif s[0].lower() == "set":
						self.update_pulses("Set_V", WL_pulses, SEL_voltage, BL_voltage, column, row, gate_level)

					elif s[0].lower() == "reset":
						self.update_pulses("Reset_V", WL_pulses, SEL_voltage, BL_voltage, column, row, gate_level)
		
		elif self.input_type == 2: #row by row with multiple state
			READ_CELLS = []

			for s in cell_pulses_list:
				if not s:
					if READ_CELLS:
						self.update_pulses("Read_V", WL_pulses, SEL_voltage, BL_voltage, READ_CELLS, row, None)
						READ_CELLS = []
					
					continue

				row,column = int(s[1]), int(s[2])
				
				gate_level = None
				if len(s) > 3:
					gate_level = s[3]
				if s[0].lower() == "set":
					column = [column]
					self.update_pulses("Set_V", WL_pulses, SEL_voltage, BL_voltage, column, row, gate_level)		
				elif s[0].lower() == "reset":
					column = [column]
					self.update_pulses("Reset_V", WL_pulses, SEL_voltage, BL_voltage, column, row, gate_level)
				elif s[0].lower() == "read":
					READ_CELLS.append(column)

			if READ_CELLS:
				self.update_pulses("Read_V", WL_pulses, SEL_voltage, BL_voltage, READ_CELLS, row, None)
				READ_CELLS = []


		elif self.input_type == 3:  #binary operation in parallel

			SET_CELLS = []
			RESET_CELLS = []
			READ_CELLS = []


			for s in cell_pulses_list:
				if not s:
					if SET_CELLS:
						self.update_pulses("Set_V", WL_pulses, SEL_voltage, BL_voltage, SET_CELLS, row, None)
						SET_CELLS = []
					if RESET_CELLS:
						self.update_pulses("Reset_V", WL_pulses, SEL_voltage, BL_voltage, RESET_CELLS, row, None)
						RESET_CELLS = []
					if READ_CELLS:
						self.update_pulses("Read_V", WL_pulses, SEL_voltage, BL_voltage, READ_CELLS, row, None)
						READ_CELLS = []
					
					continue

				row,column = int(s[1]), int(s[2])

				if s[0].lower() == "set":
					SET_CELLS.append(column)
		
				elif s[0].lower() == "reset":
					RESET_CELLS.append(column)

				elif s[0].lower() == "read":
					READ_CELLS.append(column)

			if SET_CELLS:
				self.update_pulses("Set_V", WL_pulses, SEL_voltage, BL_voltage, SET_CELLS, row, None)
				SET_CELLS = []
			if RESET_CELLS:
				self.update_pulses("Reset_V", WL_pulses, SEL_voltage, BL_voltage, RESET_CELLS, row, None)
				RESET_CELLS = []
			if READ_CELLS:
				self.update_pulses("Read_V", WL_pulses, SEL_voltage, BL_voltage, READ_CELLS, row, None)
				READ_CELLS = []


		pulses_str = ""
		c = 0
		for i in range(0, self.rows):
			pulses_str += f"V_WL{i}(r{i} 0) vsource type=pwl wave=[\\\n"
			for k in range(0, len(WL_pulses[i])-1, 2):
				pulses_str += WL_pulses[i][k] + '\t' + WL_pulses[i][k+1] + '\t\\\n'
			pulses_str += ']\n'

			pulses_str += f"V_SEL{i}(g{i} 0) vsource type=pwl wave=[\\\n"
			for k in range(0, len(SEL_voltage[i])-1, 2):
				pulses_str += SEL_voltage[i][k] + '\t' + SEL_voltage[i][k+1] + '\t\\\n'
			pulses_str += ']\n\n'


		pulses_str += "\n\n"

		for j in range(0, self.columns):
			pulses_str += f"V_BL{j}(c{j} 0) vsource type=pwl wave=[\\\n"
			for k in range(0, len(BL_voltage[j])-1, 2):
				pulses_str += BL_voltage[j][k] + '\t' + BL_voltage[j][k+1] + '\t\\\n'
			pulses_str += ']\n\n'
			
		
		return pulses_str

	def sweep_to_string(self, sweep_params):

		sweep_str = ""
		min_g, max_g, step_g = sweep_params[0], sweep_params[1], sweep_params[2]

		if max_g < min_g : step_g = -step_g
		
		sweep_str += "swp sweep param = Gate_V values=["
		for i in np.arange(min_g, max_g + step_g, step_g):
			sweep_str += str(np.round(i,2)) + " "

		sweep_str = sweep_str[0:-1] + f"]{{\n\ttran tran stop = {self.simulation_stop_time} errpreset=conservative maxstep={self.simulation_maxstep}\n}}"

		return sweep_str

	def gen_netlist(self,memristor_params= {}, pulses = [], sweep_params = [], file_name = "", memristor_model_path = "", transistor_model_path = ""):

		str_param = ""
		str_ckt = ""
		str_instances = ""
		str_pulses = ""

		str_param += "global 0\n"
		str_param += "ahdl_include " + "\"" + memristor_model_path + "\"" + "\n"
		str_param += "include " + "\"" + transistor_model_path + "\"" + "\n" 
		str_param += f"simulatorOptions options vabstol = {self.vabstol} iabstol = {self.iabstol} temp = {self.temp} tnom = {self.tnom} gmin = {self.gmin}\n"
		str_param += f"trans {self.simulation_type} stop = {self.simulation_stop_time}  maxstep = {self.simulation_maxstep} errpreset=conservative\n"
		str_param += f"saveOptions options save=all currents=all saveahdlvars=all\n"
		str_param += f"parameters Read_V = {self.read_v} Set_V = {self.set_v} Reset_V = {self.reset_v} Gate_V = {self.gate_v} Transistor_Width = {self.trans_width}n Transistor_Length = {self.trans_length}n\n"
		if memristor_params: str_param += "parameters " + self.parameters_list(param=memristor_params) + "\n"
		str_param += "\n"

		str_ckt += "subckt XBAR_CELL WordLine BitLine SelectLine\n"
		str_ckt += f"\tM0 (net WordLine) {self.memristor_model}"
		str_ckt += "\t" + self.parameters_list(param=memristor_params, numerical_mode = False) + "\n"
		str_ckt += f"\tT0 (net SelectLine BitLine BitLine) {self.transistor_model}  w = Transistor_Width	 l = Transistor_Length\n"
		str_ckt += "ends XBAR_CELL\n\n"

		k = 0
		for i in range(0, self.rows):
			for j in range(0, self.columns):
				str_instances += f"I{k} (r{i} c{j} g{i}) XBAR_CELL\n"
				k += 1

		str_pulses += "\n\n" + self.pulses_to_string(pulses)
		


		if sweep_params:
			str_pulses += self.sweep_to_string(sweep_params)


		to_be_written = str_param + str_ckt + str_instances + str_pulses
		file_ = open(file_name,"w")
		file_.write(to_be_written)
		print(f"Netlist, model path and simulation parameters written to \"{file_name}\"\n")
		