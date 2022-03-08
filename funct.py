

with open("pulses.txt") as file_in:
    lines = []
    lines = list(line for line in (l.strip() for l in file_in) if line)

rows = 0
columns = 0

for s in lines:
    a = s[s.find('(')+1:s.find(')')]
    values = a.split(",")
    row,column = int(values[0]), int(values[1])

    if(row > rows): rows = row
    if(column > columns): columns = column

def create_pulse(self, step_time, pulse_vol, time_unit, pulses = []):
    
    insert_p = False
    concatenated = False

    if not pulses:	# empty list
        start_time = 0
        stop_time = 3000
        concatenated = False

    else:
        start_time = (int(pulses[-2][:-1])+1) # get last time
        stop_time = start_time + 2000
        concatenated = True

    for i in range(start_time, stop_time, step_time):

        if insert_p == False and concatenated == False:
            pulses.append(str(i)+time_unit)
            pulses.append('0')
            pulses.append(str(i+(step_time-1))+time_unit)
            pulses.append('0')
            insert_p = True
            
        else:
            pulses.append(str(i)+time_unit)
            pulses.append(pulse_vol)
            pulses.append(str(i+(step_time-1))+time_unit)
            pulses.append(pulse_vol)
            insert_p = False
            concatenated = False


def convert_to_pulses(self, in_pulses_list = []):

    pulses_list = []
    for pulse in in_pulses_list:
        if pulse.lower() == "read":
            self.create_pulse(1000, "Read_V", self.time_units, pulses_list)

        elif pulse.lower() == "set":
            self.create_pulse(1000, "Set_V", self.time_units, pulses_list)
            
        elif pulse.lower() == "reset":
            self.create_pulse(1000, "Reset_V", self.time_units, pulses_list)

    if not pulses_list:
        print("Empty list!")
        return
    
    pulses_str = ""
    pulses_str += "V0 (r0 0) vsource type=pwl wave=[\\\n"
    for i in range(0, len(pulses_list)-1, 2):
        pulses_str += pulses_list[i] + '\t' + pulses_list[i+1] + '\t\\\n'

    pulses_str += ']'
    return pulses_str

   