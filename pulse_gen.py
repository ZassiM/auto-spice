

def create_pulse(step_time, pulse_vol, time_unit, pulses = []):
	
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
			pulses.append(str(pulse_vol))
			pulses.append(str(i+(step_time-1))+time_unit)
			pulses.append(str(pulse_vol))
			insert_p = False
			concatenated = False
			

def create_netlist_vol(pulses):
	if not pulses:
		print("Empty list!")
		return

	pulse_str = ''
	pulse_str += "V0 (r0 0) vsource type=pwl wave=[\\\n"
	for i in range(0, len(pulses)-1, 2):
		pulse_str += pulses[i] + '\t' + pulses[i+1] + '\t\\\n'
	pulse_str += ']'

	return pulse_str



def main():
	pulses = []
	create_pulse(1000, 0.2, 'n',pulses) # Read

	create_pulse(1000, -1.05, 'n',pulses) # Set

	create_pulse(1000, 0.2, 'n',pulses) # Read

	create_pulse(1000, -1.05, 'n',pulses) # Read

	print(pulses)

	#print(pulses)
	pulse_string = create_netlist_vol(pulses)
	print(pulse_string)



main()