import copy
from tracemalloc import stop

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

    def parameters_list(self, param, model_name="det", numerical_mode = True):

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

    def set_simulation_params(self, type_ = "tran", step_time = 100, period = 100, max_step = 1, time_unit = "u", vabstol = "1e-6", iabstol = "1e-12", temp = "27", tnom = "27", gmin = "1e-12", cell_pulses_list = [], row_pulses_list = [], input_type = 0):

        self.simulation_type = type_
        self.time_unit = time_unit
        self.simulation_maxstep = str(max_step) + self.time_unit
        self.step_time = step_time
        if period < 2 : period = 2
        self.period = period
        self.input_type = input_type
        self.simulation_stop_time = str(self.calculate_stop_time(cell_pulses_list, row_pulses_list)) + self.time_unit
        self.vabstol, self.iabstol, self.temp, self.tnom, self.gmin = vabstol, iabstol, temp, tnom, gmin
        
        
        print(f"Stop time: {self.simulation_stop_time}s, Step time: {self.step_time}{self.time_unit}s, Max step: {self.simulation_maxstep}s.\n")

    def calculate_crossbar_size(self, cell_pulses_list = []):

        rows = 0
        columns = 0

        for s in cell_pulses_list:
            if s:
                row,column = int(s[1]), int(s[2])
                
                if(row > rows): rows = row
                if(column > columns): columns = column

        self.rows = rows + 1
        self.columns = columns + 1
        
        print(f"Crossbar size: {self.rows} rows, {self.columns} columns.\n")

    def calculate_stop_time(self, cell_pulses_list, row_pulses_list):
        cnt = [0]*self.rows
        pulse_time = self.period + self.step_time
        stop_time = self.period

        if self.input_type == 1:
            for s in cell_pulses_list:
                if s:
                    cnt[int(s[1])] += 1
            for c in cnt:
                stop_time += pulse_time * c

        elif self.input_type == 2:
            print(row_pulses_list)
            for s in row_pulses_list:
                if s[0].lower() == 'r':
                    stop_time += pulse_time
                elif s[0].lower() == 'w':
                    stop_time += pulse_time * (len(s)-2)
        
        elif self.input_type == 3:
            print(row_pulses_list)
            for s in row_pulses_list:
                if s[0].lower() == 'r':
                    stop_time += pulse_time
                elif s[0].lower() == 'w':
                    stop_time += pulse_time
                    for i in range(2, len(s)-1):
                        if s[i] != s[i+1]:
                            stop_time += pulse_time
                            break

        return stop_time
            
    def set_crossbar_params(self, read_v = 0.2, set_v = -1.05, reset_v = 0.75, gate_v = 1, trans_length = 32, trans_width = 32):

        self.read_v = read_v
        self.set_v = set_v
        self.reset_v = reset_v
        self.gate_v = gate_v
        self.trans_length = trans_length
        self.trans_width = trans_width
        
    def set_variablity(self, Nmin=False, Nmax=False, rdet=False, ldet=False):

        self.vary_nmin = Nmin
        self.vary_nmax = Nmax
        self.vary_rdet = rdet
        self.vary_ldet = ldet

        return {"Ndiscmin": Nmin, "Ndiscmax": Nmax, "rnew": rdet,"lnew": ldet}



