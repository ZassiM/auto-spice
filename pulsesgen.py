import csv

rows=0
columns=0

def create_pulse(step_time, pulse_vol, time_unit, WL_pulse, SEL_voltage, BL_voltage, row, column):

    insert_p = False
    concatenated = False

    start_time_b = 0
    stop_time_b = 3*step_time

    if not WL_pulse[row]:
        start_time = 0
        stop_time = 3 * step_time
    
    else:
        start_time = int(WL_pulse[row][-2][:-1])+1 
        stop_time = start_time + 2000
        concatenated = True

    if not BL_voltage[column]:
        start_time_b = 0
        stop_time_b = 3 * step_time
    else:
        start_time_b = int(BL_voltage[column][-2][:-1])+1 
        stop_time_b = start_time + 2000
    



    for i in range(start_time_b, stop_time_b, step_time):

        BL_voltage[column].append(str(i)+time_unit)
        BL_voltage[column].append("Ground")
        BL_voltage[column].append(str(i+(step_time-1))+time_unit)
        BL_voltage[column].append("Ground")

        for k in range(0, columns):
            if k != column:
                BL_voltage[k].append(str(i)+time_unit)
                BL_voltage[k].append(pulse_vol)
                BL_voltage[k].append(str(i+(step_time-1))+time_unit)
                BL_voltage[k].append(pulse_vol)  

    
    for i in range(start_time, stop_time, step_time):

        if insert_p == False and concatenated == False:
            WL_pulse[row].append(str(i)+time_unit)
            WL_pulse[row].append('0')
            WL_pulse[row].append(str(i+(step_time-1))+time_unit)
            WL_pulse[row].append('0')
            insert_p = True
            
        else:
            WL_pulse[row].append(str(i)+time_unit)
            WL_pulse[row].append(pulse_vol)
            WL_pulse[row].append(str(i+(step_time-1))+time_unit)
            WL_pulse[row].append(pulse_vol)
            insert_p = False
            concatenated = False
    
    if not SEL_voltage[row]:
        SEL_voltage[row] = 'Gate_V'


def pulses_to_string(in_pulses_list, rows, columns):

    WL_pulses = [[] for _ in range(rows)]
    SEL_voltage = [None] * rows
    BL_voltage = [[] for _ in range(columns)]


    for s in in_pulses_list:

        row,column = int(s[1]), int(s[2])

        if s[0].lower() == "read":
           create_pulse(1000, "Read_V", "u", WL_pulses, SEL_voltage, BL_voltage, row, column)
            
        elif s[0].lower() == "set":
            create_pulse(1000, "Set_V", "u", WL_pulses, SEL_voltage, BL_voltage, row, column)

        elif s[0].lower() == "reset":
            create_pulse(1000, "Reset_V", "u", WL_pulses, SEL_voltage, BL_voltage, row, column)
        
    if not WL_pulses:
        print("Empty list!")
        return
    
    
    pulses_str = ""
    c = 0
    for i in range(0, rows):
        pulses_str += f"V_WL{i} (r{i} Ground) vsource type=pwl wave=[\\\n"
        for k in range(0, len(WL_pulses[i])-1, 2):
            pulses_str += WL_pulses[i][k] + '\t' + WL_pulses[i][k+1] + '\t\\\n'
        pulses_str += ']\n\n'

        pulses_str += f"V_SEL{i} (g{i} Ground) vsource dc = {SEL_voltage[i]}\n\n"

    for j in range(0, columns):
        pulses_str += f"V_BL{j} (c{j} Ground) vsource type=pwl wave=[\\\n"
        for k in range(0, len(BL_voltage[j])-1, 2):
            pulses_str += BL_voltage[j][k] + '\t' + BL_voltage[j][k+1] + '\t\\\n'
        pulses_str += ']\n\n'
        
    
    return pulses_str

def calculate_xbar_size(in_pulses_list,rows,columns):

    for s in in_pulses_list:
        
        row,column = int(s[1]), int(s[2])
        
        if(row > rows): rows = row
        if(column > columns): columns = column

    rows = rows + 1
    columns = columns + 1
    
    print(f"Crossbar size: {rows} rows, {columns} columns.\n")

    return rows, columns

with open('pulses.csv', 'r') as file:
    reader = csv.reader(file)
    in_pulses_list = list(reader)



rows, columns = calculate_xbar_size(in_pulses_list,rows,columns)

print(pulses_to_string(in_pulses_list, rows, columns))





