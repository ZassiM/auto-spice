sim_time = 12
pulse = []
time_edge=0
for i in range(0, sim_time):
	if !time_edge:
		pulse.append(i)
		time_edge = True
	else:
		pulse.append(i+0.9)
		time_edge = False

	if i%2==0:
		pulse.append(0)
	elif i==1 or i==5 or i==9:
		pulse.append(0.2)
	elif i==3:
		pulse.append(-0.75)
	elif i==7:
		pulse.append(1.5)

print(pulse)