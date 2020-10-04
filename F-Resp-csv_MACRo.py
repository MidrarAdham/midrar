# Midrar Adham
# June-24-2020
# This file is meant to control NHR 9410 (Grid Simulator) frequency via SCPI Commands.
# The frequency values provided here is just an example.
# An array of different values is used to accomplish this task.
# The equipment accepts values between 30-880 Hz.(Accodring to NHR 9400 Series AC/DC Power Module Programmer’s Reference Manual)
# For each command below, a brief description is provided.
# This file is available to anyone who would like to use it. Feel free to copy,edit, and develop its content.

# Each command will be executed after the connection is closed. This means that for each command, we have to establish the connection, sent the command, close the connection.
# As you read through this file, you'll find flags. These flags are not important. They were used just for learning purposes.

# Here the code begins:
import csv
import socket					#Import libraries
import time
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
# import matplotlib.dates as mdates
# import datetime as dt
# from datetime import timedelta
# import pandas as pd

def conn():
	global s
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(1000)
	s.connect(('192.168.0.149',5025)) # NHR 9410 IP address
	output = 'SYST:RWL\n'			  # Lock the touch panel screen (Safety purpose)
	s.send(output.encode('utf-8'))	  # For each SCPI command, it MUST encoded into utf-8.
	return s
def clos(s):							  # This function is meant to close the connection
	output5 = 'SYST:LOC\n'			  # Unlock the touch panel screen
	s.send(output5.encode('utf-8'))
	s.close()						  # Close the connection



def Gs():

	arr = []
	with open("Aug_25.csv") as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		for rows in csv_reader:
			y = rows['STATION_1:Freq']
			# print(y)
			#print(y)
			arr.append(float(y))
	#	for i in arr:
	#		print(i(0))

	conn()
	# s.send('FREQ 60.00 \n'.encode('utf-8'))
	s.send('MACR:LEAR 1 \n'.encode('utf-8'))
	# print("sent1")
	s.send('MACR:OPER:SYNC:INST1 SYNC \n'.encode('utf-8'))
	# print("sent2")
	s.send('MACR:LEAR 0 \n'.encode('utf-8'))
	# print("sent4")
	s.send('MACR:RUN \n'.encode('utf-8'))
	# print("sent5")
	output2 = 'FREQ '
	liss = []
	freq_val = []
	p = 0
	for i in arr:
		if 0 <= p <= 5000:
			x = 0.0310
		if 5001 <= p <= 10000: 
			x = 0.02500
		if 10001 <= p <= 15000:
			x = 0.02800
		if 15001 <= p <= 18000:
			x = 0.028000
		print(i)
		start_time = time.time()
		# print('Starting time is ',start_time)
		t_end = time.time() + x
		while time.time() < t_end:
			k = 1
		var = output2 + str(i)+'\n'
		# print(var)
		s.send(var.encode('utf-8'))
		end_time = time.time()
		# print('Time ends here ',end_time)
		diff = end_time - start_time
		# print(diff)
		diff_list = liss.append(diff)
		s.send('FREQ?\n'.encode('utf-8'))
		msg = s.recv(1024).decode()
		freq_val.append(msg)
		p = p + 1

		# print('response: ',msg)
	# for l in diff_list:
	# 	print(l)

	return diff_list, freq_val, arr
	clos(s)
Gs()

def real_time():

	diff_list, freq_val, arr = Gs()
	df = pd.read_csv('freq_Gs.txt',usecols=['freq'],engine='python',index_col=None)
	y1 = [dt.datetime.now() + dt.timedelta(microseconds=i) for i in range(len(arr))]
	y2 = [dt.datetime.now() + dt.timedelta(microseconds=i) for i in range(len(df))]
	plt.plot(y1,arr)
	plt.plot(y1,df)
	plt.title('Original and PMU Freq Data')
	plt.grid()
	plt.gcf().autofmt_xdate()
	plt.show()

# real_time()
