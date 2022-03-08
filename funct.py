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

rows += 1
columns += 1


def create_pulse(step_time, pulse_vol, time_unit, pulses, idx):
    
    insert_p = False
    concatenated = False
  
    
    if not pulses[idx]:	# empty list
        start_time = 0
        stop_time = 3000
        concatenated = False

    else:
        start_time = int(pulses[idx][-2][:-1])+1 # get last time
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


def pulses_to_string(in_pulses_list):
    pulses = [[] for _ in range(rows*columns)]

    cnt = 0
    for s in in_pulses_list:
        pulse_str = s[0:s.find('(')]
        pulse_idx = s[s.find('(')+1:s.find(')')]
        pulse_idx = pulse_idx.split(",")
        row,column = int(pulse_idx[0]), int(pulse_idx[1])
        idx = columns*row + column

        
        if pulse_str.lower() == "read":
            create_pulse(1000, "Read_V", "n",  pulses, idx)

        elif pulse_str.lower() == "set":
            create_pulse(1000, "Set_V", "n", pulses, idx)

        elif pulse_str.lower() == "reset":
            create_pulse(1000, "Reset_V", "n", pulses, idx)
        

    if not pulses:
        print("Empty list!")
        return
    
    pulses_str = ""
    c = 0
    for i in range(0, rows):
        for j in range(0, columns):
            pulses_str += f"V{c} (r{i} c{j}) vsource type=pwl wave=[\\\n"
            for k in range(0, len(pulses[columns*i + j])-1, 2):
                pulses_str += pulses[columns*i + j][k] + '\t' + pulses[columns*i + j][k+1] + '\t\\\n'
            pulses_str += ']'
            c += 1

    return pulses_str

p = pulses_to_string(lines)


# read(0,0)
# set(0,0)
# reset(0,1)
# read(0,1)
# read(1,0)
# reset(1,0)
# set(1,1)
# read(1,1)






   