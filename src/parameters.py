import copy

class parameters(object):  

	def __init__(self, device="det", simulation = "spectre"): 
		
		if simulation !="spectre":
			print("simulation needs to be set = spectre")
			exit()
		if device =="var":
			self.memristor_model= "JART_VCM_1b_VAR"
		else:
			self.memristor_model= "JART_VCM_1b_det"
		
		self.transistor_model = "nmos"


	def parameters_list(self, param= {}, model_name="det", numerical_mode = True):

		self.device_parameters = ""
		k = 0
		if model_name=="var" or model_name == "det":
			for i in param:
				k += 1
				if numerical_mode:
					self.device_parameters += i + " = " + str(param[i]) + " "   
				else:
					self.device_parameters += i + " = " + i + " " 
				if k == 5:
					self.device_parameters += "\\\n\t\t"
					k=0
		
		return self.device_parameters


	def variablity_param(self, iteration):

		variablity_dict = {}
		variablity_dict["Ninit"] = "Ndiscmin"

		if self.vary_nmin:
			ndisc_min_var = f"Ndiscmin{iteration} "
			variablity_dict["Ndiscmin"] = variablity_dict["Ninit"] = ndisc_min_var
		if self.vary_nmax:
			ndisc_max_var = f"Ndiscmax{iteration} "
			variablity_dict["Ndiscmax"] = ndisc_max_var
		if self.vary_ldet:
			lnew_var = f"lnew{iteration} "
			variablity_dict["lnew"] = lnew_var
		if self.vary_rdet:
			rnew_var = f"rnew{iteration}"
			variablity_dict["rnew"] = rnew_var

		return variablity_dict

	def set_input_voltages(self, volt_r = [], volt_c = []):

		self.input_type_r, self.input_type_c = [], []
		self.volt_0_r, self.volt_0_c = [], []
		self.volt_1_r, self.volt_1_c = [], []
		self.time_period_r, self.time_period_c = [], []
		self.pulse_width_r, self.pulse_width_c = [], []
		self.rise_time_r, self.rise_time_c = [], []
		self.fall_time_r, self.fall_time_c = [], []

		def_vol = ["pulse", 0, 0, "0", "0", "0", "0"]

		if self.rows < len(volt_r):
			print(f"There are {len(volt_r)} voltage pulses but only {self.rows} rows -> {len(volt_r)-self.rows} voltage pulses are ignored.\n")
			while self.rows != len(volt_r):
				volt_r.pop()
		
		if self.columns < len(volt_c):
			print(f"There are {len(volt_c)} voltage pulses but only {self.columns} columns -> {len(volt_c)-self.columns} voltage pulses are ignored.\n")
			while self.columns != len(volt_c):
				volt_c.pop()
		
		if self.rows > len(volt_r):
			print(f"There are {self.rows} rows, but only {len(volt_r)} voltage pulses are defined -> {self.rows - len(volt_r)} null voltages are added.\n")
			while self.rows != len(volt_r):
				volt_r.append(def_vol)
		
		if self.columns > len(volt_c):
			print(f"There are {self.columns} columns, but only {len(volt_c)} voltage pulses are defined -> {self.columns - len(volt_c)} null voltages are added.\n")
			while self.columns != len(volt_c):
				volt_c.append(def_vol)

		for v in volt_r:
			self.input_type_r.append(v[0])
			self.volt_0_r.append(v[1])
			self.volt_1_r.append(v[2])
			self.time_period_r.append(v[3])
			self.pulse_width_r.append(v[4])
			self.rise_time_r.append(v[5])
			self.fall_time_r.append(v[6])

		for v in volt_c:
			self.input_type_c.append(v[0])
			self.volt_0_c.append(v[1])
			self.volt_1_c.append(v[2])
			self.time_period_c.append(v[3])
			self.pulse_width_c.append(v[4])
			self.rise_time_c.append(v[5])
			self.fall_time_c.append(v[6])
		
		print("Voltage pulses correctly added.\n")

	def set_simulation_params(self, type_ = "tran", stop_time = "5u", maxstep = "1u"):

		self.simulation_stop_time = stop_time
		self.simulation_type = type_
		self.simulation_maxstep = maxstep
		self.time_units = stop_time[-1] 

		print(f"Stop time: {self.simulation_stop_time}s, Max step: {self.simulation_maxstep}s.\n")

	def calculate_xbar_size(self, in_pulses_list = []):

		rows = 0
		columns = 0

		for s in in_pulses_list:
			row,column = int(s[1]), int(s[2])
			
			if(row > rows): rows = row
			if(column > columns): columns = column

		self.rows = rows + 1
		self.columns = columns + 1
		
		print(f"Crossbar size: {self.rows} rows, {self.columns} columns.\n")


	def set_xbar_params(self, read_v = 0.2, set_v = -1.05, reset_v = 0.75):

		self.read_v = read_v
		self.set_v = set_v
		self.reset_v = reset_v
		

	def set_variablity(self, Nmin=False, Nmax=False, rdet=False, ldet=False):

		self.vary_nmin = Nmin
		self.vary_nmax = Nmax
		self.vary_rdet = rdet
		self.vary_ldet = ldet

		return {"Ndiscmin": Nmin, "Ndiscmax": Nmax, "rnew": rdet,"lnew": ldet}



