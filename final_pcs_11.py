####importing packages#########
#library for general packages
import os
import sys
import time
import datetime
import socket
import random
import serial
import multiprocessing
import ctypes

# for kill port
import signal
import subprocess

def timer_func(none):
	print ("Entering into timer processing..=",time_val.value)
	while True:
		time.sleep(.1)
		while (time_val.value != 0 ):
			time_val.value=time_val.value-1
			time.sleep(1)
			if time_val.value==0:
				boat_detect.value=False
			print ("timer=",time_val.value," ",boat_detect.value)



# Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO

#library for ble scannig
import blescan
import bluetooth._bluetooth as bluez

#library for config file data fetch
import configparser

#api call
import requests
import json

'''
boat_number="" #this variable will update by ble scan function
terminal="Vyttila"
serf_id="VY01" #its static id for each serf
my_pontoon="1" #its static id for each serf
static_timestamp="1658056738"
workstation_ip="10.2.8.2"
'''
#get_url = "http://10.2.8.15:4000/api/route_info/get_route_info?terminal_id=vyttila&boat_id=9157674"
#post_url_1 = "http://10.2.8.15:4000/api/postEvent"

#get_url_1 = "http://10.2.8.15:4000/api/route_info/get_route_info?terminal_id="+str(terminal)+"&boat_id="+boat_number
#post_url_1 = "http://"+ workstation_ip+":3001/occ/create"




#Switch flag
entry_flag = False
exit_flag = False

one_time_flag_entry = True
one_time_flag_exit = True

#///////////////////////////////////////////////////////////////////////////////////////******************************////////////////////////////////////////////////
from flask import Flask, jsonify, request
import json

from flask_cors import CORS,cross_origin
app=Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/
@app.route('/serf_server/route_info', methods = ['GET', 'POST'])
def home():
	try:

		if(request.method == 'GET'):
			data = "hello i am The serf in Vyttila terminal pontoon Number 1"
			return jsonify({'data': data})

		if(request.method == 'POST'):

			manual_mode.value="boarding_stop" #at first stop the process then  will start another one

			time.sleep(3)

			print(request.data)
			y = json.loads(request.data)
			vacancy_count.value =int(y["current_occupancy"])  #update the variable with current occupency
			capacity_count.value=int(y["boat_occupancy"]) ##update the variable with current occupency
			route_info.value =y["route_info"]
			terminal_id.value =y["jettyname"]
			boat_id.value=y["boat_id"]
			pontoonname.value=y["pontoonname"]
			boarding_mode.value=y["boarding_mode"]
			tripsrno.value=y["tripsrno"]
			scheduled_time.value=y["time"]
			print("SCR_trip_no=",tripsrno.value)
			print("SCR_boat_id=",boat_id.value)
			print("SCR_pontoonname=",pontoonname.value)
			print("SCR_route_info=",route_info.value)
			print("SCR_jettyname=",terminal_id.value)
			print("SCR_boarding_mode=",boarding_mode.value)
			print("SCR_boat_occupancy=",capacity_count.value)
			print("SCR_current_occupancy=",vacancy_count.value)
			print("SCR_scheduled_time=",scheduled_time.value)
			#if pontoonname.value==my_pontoon:
			if True:

				if boarding_mode.value=="manual" or boarding_mode.value=="automatic":
					workstation_request.value=True  #set the flag
					data = "Sucess"
				else:
					data="Boarding_mode is not valid"
			else:
				print("sorry pontoon number is not matched")
				data="Missmatch pontoonname"

			return jsonify({'status': data})

	except Exception as e:
		print("Error in POST/GET method(/route_info)=",e)
		pass


@app.route('/serf_server/entry_switch', methods = ['POST'])
def home1():

	global my_pontoon
	try:
		if(request.method == 'POST'):
			#print(request.data)
			y = json.loads(request.data)
			#print(y)
			mode=y["mode"]
			pontoonname.value=y["pontoonname"]
			entry_turnstile=y["entry_turnstile"]

			if(pontoonname.value==my_pontoon):
				if(mode=="manual"):
					if(entry_turnstile=="start"):
						manual_mode.value="start" #set manual mode state
						turnstile.entry_start()
						print("entry start by SCR(Manual)")
					if(entry_turnstile=="stop"):
						manual_mode.value="stop" #reset manual mode state
						turnstile.entry_stop()
						print("entry stop by SCR(Manual)")
					data = "Sucess"
				else:
					data="mode mismatch"
			else:
				print("sorry pontoon number is not matched")
				data="Missmatch pontoonname"


			response =jsonify({'message': data})
			return response
	except Exception as e:
		print("Error in POST method(/entry_switch)=",e)
		pass


@app.route('/serf_server/exit_switch', methods = ['POST'])
def home2():

	global my_pontoon
	try:
		if(request.method == 'POST'):
			#print(request.data)
			y = json.loads(request.data)
			#print(y)
			mode=y["mode"]
			pontoonname.value=y["pontoonname"]
			exit_turnstile=y["exit_turnstile"]

			if(pontoonname.value==my_pontoon):
				if(mode=="manual"):
					if(exit_turnstile=="start"):
						manual_mode.value="start" # manual mode state
						turnstile.exit_start()
						print("exit start by SCR(Manual)")
					if(exit_turnstile=="stop"):
						manual_mode.value="stop" # manual mode state
						turnstile.exit_stop()
						print("exit stop by SCR(Manual)")
					data = "Sucess"
				else:
					data="mode mismatch"
			else:
				print("sorry pontoon number is not matched")
				data="Missmatch pontoonname"


			response =jsonify({'message': data})
			return response
	except Exception as e:
		print("Error in POST method(/exit_switch)=",e)
		pass


@app.route('/serf_server/emergency_switch', methods = ['POST'])
def home3():

	global my_pontoon
	try:
		if(request.method == 'POST'):
			#print(request.data)
			y = json.loads(request.data)
			#print(y)
			mode=y["mode"]
			pontoonname.value=y["pontoonname"]
			if pontoonname.value==my_pontoon:
				if mode=="emergency":
					manual_mode.value="emergency" # manual mode state
					print("Emergency pressed from SCR room")
					data = "Sucess"
				else:
					data="mode mismatch"
			else:
				print("sorry pontoon number is not matched")
				data="Missmatch pontoonname"


			response =jsonify({'message': data})
			return response

	except Exception as e:
		print("Error in POST method(/emergency_switch)=",e)
		pass



@app.route('/serf_server/boarding_state', methods = ['POST'])
def home5():

	global my_pontoon
	try:

		if(request.method == 'POST'):
			#print(request.data)
			y = json.loads(request.data)
			#print(y)
			mode=y["mode"]
			pontoonname.value=y["pontoonname"]
			boarding_state=y["boarding_state"]
			if pontoonname.value==my_pontoon:
				if mode=="manual":
					if boarding_state == "stop":
						manual_mode.value="boarding_stop" # manual mode state
						print("boarding stop pressed from SCR room")
					if boarding_state == "start":
						manual_mode.value="boarding_start" # manual mode state
						print("boarding start pressed from SCR room")
					data = "Sucess"
				else:
					data="mode mismatch"
			else:
				print("sorry pontoon number is not matched")
				data="Missmatch pontoonname"


			response =jsonify({'message': data})
			return response
	except Exception as e:
		print("Error in POST method(/boarding_state)=",e)
		pass



@app.route('/serf_server/gate_status', methods = ['GET'])
def home4():

	global my_pontoon
	try:

		param_filter = request.args.get('pontoonname', default = '*', type = str)
		if(request.method == 'GET'):
			print("param_filter=",param_filter)
			if(param_filter==my_pontoon):
				response=jsonify({'entry_gate_status': entry_gate_status.value , 'exit_gate_status': exit_gate_status.value})
			else:
				response=jsonify({'message': "missmatch parameter value of \"pontoonname:\""})
			return response
	except Exception as e:
		print("Error in GET method(/gate_status)=",e)
		pass






#*****************************************************************///////////////////******************************************************************************
#config file data fetching
Config = configparser.ConfigParser()
Config.read("/home/pi/Final_Integration_Code/config.ini")


terminal=Config.get('UniqueID', 'terminal_id')
serf_id=Config.get('UniqueID', 'serf_id')
my_pontoon=Config.get('UniqueID', 'my_pontoon')
workstation_ip=Config.get('server', 'get_systemip')

entry_switch = Config.get('Switch', 'entry_switch')
exit_switch = Config.get('Switch', 'exit_switch')

#get_url = Config.get('Api', 'get_api')
post_url_1=Config.get('Api', 'post_api')
auth=Config.get('apikey','key')
headers = {'Content-Type': 'application/json','Authorization' :auth }

print ("Terminal=",terminal)
print ("serf_id=",serf_id)
print ("my_pontoon=",my_pontoon)
print ("workstation_ip=",workstation_ip)
print ("post_url=",post_url_1)
print ()

#configdata turnstile
Config1 = configparser.ConfigParser()
Config1.read("/home/pi/Final_Integration_Code/turnstile_config.ini")







#initialize all serial port & parameters
boarding_port=Config1.get('ports', 'boarding')
alighting_port=Config1.get('ports', 'alighting')
f_boarding_port='/dev/'+boarding_port
f_alighting_port='/dev/'+alighting_port

print (f_boarding_port)
print (f_alighting_port)

#initialize ports permissions
os.system("sudo chmod 777 "+f_boarding_port)
os.system("sudo chmod 777 "+f_alighting_port)

#serial comports connections
boarding_comport= serial.Serial(f_boarding_port)
alighting_comport= serial.Serial(f_alighting_port)


boarding_comport.baudrate = 9600 # set Baud rate to 9600
boarding_comport.bytesize = 8 # Number of data bits = 8
boarding_comport.parity = 'N' # No parity
boarding_comport.stopbits = 1 # Number of Stop bits = 1
boarding_comport.timeout = 2
boarding_comport.xonxoff = False
boarding_comport.rtscts = False
boarding_comport.dsrdtr = False

alighting_comport.baudrate = 9600 # set Baud rate to 9600
alighting_comport.bytesize = 8 # Number of data bits = 8
alighting_comport.parity = 'N' # No parity
alighting_comport.stopbits = 1 # Number of Stop bits = 1
alighting_comport.timeout = 2
alighting_comport.xonxoff = False
alighting_comport.rtscts = False
alighting_comport.dsrdtr = False


class turnstile:
	def __init__(self,comport):
		self.comport=comport
	def entry_start():
		entry_gate_status.value="open"
		data = bytes.fromhex('AA00010200000800040000000000000F')
		boarding_comport.write(data)
		time.sleep(0.3)
	def exit_start():
		exit_gate_status.value="open"
		data = bytes.fromhex('AA00010200000800040000000000000F')
		alighting_comport.write(data)
		time.sleep(0.3)
	def entry_stop():
		entry_gate_status.value="close"
		data = bytes.fromhex('AA000102000008000500000000000010')
		boarding_comport.write(data)
		time.sleep(0.3)
	def exit_stop():
		exit_gate_status.value="close"
		data = bytes.fromhex('AA000102000008000500000000000010')
		alighting_comport.write(data)
		time.sleep(0.3)
	def clear_vacancy_count():
		data = bytes.fromhex('AA00010200600801000000000000006C')
		alighting_comport.write(data)
		time.sleep(0.3)
		boarding_comport.write(data)
		time.sleep(0.3)

#********LED Display Declaration**********
IP_ADDRESS = "192.168.0.7"
IP_PORT = 23
disp_flag = 1

try:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.settimeout(2)
	client.connect((IP_ADDRESS, IP_PORT))
	client.settimeout(None)
except Exception as ex:
	print("display socket error")



def entry_switch_pressed(channel):
	global entry_flag,one_time_flag_entry
	time.sleep(0.1)
	print ("entry_switch pressed")
	if GPIO.input(channel) == GPIO.HIGH:
		entry_flag^=True
		print ("entry_flag=",entry_flag)
		if (entry_flag == True and one_time_flag_entry == True):
			print ("Entry gate Unlocked")
			one_time_flag_entry = False
			ent_flag.value=True
			manual_mode.value="start"
			turnstile.entry_start()
		elif (entry_flag == False and one_time_flag_entry == False):
			print ("Entry gate Locked")
			one_time_flag_entry = True
			ent_flag.value=False
			manual_mode.value="stop"
			turnstile.entry_stop()


def exit_switch_pressed(channel):
	global exit_flag,one_time_flag_exit
	time.sleep(0.1)
	print ("exit_switch pressed")
	if GPIO.input(channel) == GPIO.HIGH:
		exit_flag^=True
		print ("exit_flag=",exit_flag)
		if (exit_flag == True and one_time_flag_exit == True):
			print ("Exit gate Unlocked")
			one_time_flag_exit = False
			ext_flag.value=True
			manual_mode.value="start"
			turnstile.exit_start()
		elif (exit_flag == False and one_time_flag_exit == False):
			print ("Exit gate Locked")
			one_time_flag_exit = True
			ext_flag.value=False
			manual_mode.value="stop"
			turnstile.exit_stop()


#****************************************************************************
def switch_init():
	GPIO.setwarnings(False) # Ignore warning for now
	GPIO.setmode(GPIO.BCM) # Use physical pin numbering
	GPIO.setup(int(entry_switch), GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 15 to be an input pin and set initial value to be pulled low (off) 
	GPIO.setup(int(exit_switch), GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 16 to be an input pin and set initial value to be pulled low (off)
def switch_on():
	GPIO.add_event_detect(int(entry_switch),GPIO.RISING,callback=entry_switch_pressed,bouncetime=1000) # Setup event on pin rising edge
	GPIO.add_event_detect(int(exit_switch),GPIO.RISING,callback=exit_switch_pressed,bouncetime=1000) # Setup event on pin rising edge
def switch_off():
	GPIO.remove_event_detect(int(entry_switch))
	GPIO.remove_event_detect(int(exit_switch))

#ble initialization
dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	blescan.hci_le_set_scan_parameters(sock)
	blescan.hci_enable_le_scan(sock)
	print ("ble thread started")
except:
	print ("error accessing bluetooth device...")
	os.system("sudo	hciconfig hci0 reset")
	time.sleep(1)
	os.system("sudo hciconfig -a")
	sock = bluez.hci_open_dev(dev_id)
	blescan.hci_le_set_scan_parameters(sock)
	blescan.hci_enable_le_scan(sock)
	print ("ble thread started again..")

#getting network status
class networkping:
	def __init__(self):
		time.sleep(0.2)
		Config = configparser.ConfigParser()
		Config.read("/home/pi/finalcode/config.ini")
		self.get_serverip = Config.get('server', 'get_serverip')
		self.get_systemip= Config.get('server', 'get_systemip')
		#print (self.get_serverip , self.get_systemip)
	def ping_server(self):
		resp = os.system("ping -c 3 " + self.get_serverip)
		return  (1 if resp == 0 else 0)
	def ping_system(self):
		sys_resp = os.system("ping -c 1 " + self.get_systemip)
		return (1 if sys_resp == 0 else 0)

#switch init
switch_init()
switch_off()


#turnstile comport listen
def boarding_listen(boarding_data,entry_trigger):
	while True:
		boarding_comport.flush()
		boarding_count=0
		s=boarding_comport.read(16)
		boarding_count= s.hex()
		#print ("entry_turnstile=",boarding_count)
		if (boarding_count[14:18]== "0f03"):
			return_data = int(boarding_count[24:30],16)
			boarding_data.value=return_data
			print ("boardig count = ",return_data)
			entry_trigger.value = 1
		elif (boarding_count[14:18]== "0703" or boarding_count[14:18]== "0d03"):
			entry_gate_status.value="open"
			print ("entry_open")
		elif(boarding_count[14:18]== "0003"):
			entry_gate_status.value="close"
			print ("entry_close")
		elif(boarding_count[14:18]== "0d07" or boarding_count[14:18]== "0707"):
			print ("Emergency  detected...")
			entry_gate_status.value="emergency"
			exit_gate_status.value="emergency"
			manual_mode.value="boarding_stop"
			emergency_detect.value=True
		elif(boarding_count[14:18]== "6109"): #6008  for forward intrusion
			print ("Intrusion detected in Entry Gate.........")
			time.sleep(5)
			if ent_flag.value==True:
				turnstile.entry_start()
			else:
				turnstile.entry_stop()
		elif(boarding_count[14:18]== "0000"):   #after coming to emergency then its show close
			exit_gate_status.value="close"
			entry_gate_status.value="close"


def alighting_listen(alighting_data,exit_trigger):
	while True:
		alighting_comport.flush()
		aighting_count=0
		s1=alighting_comport.read(16)
		alighting_count= s1.hex()
		#print ("exit_turnstile=",alighting_count)
		if (alighting_count[14:18]== "0f03"):
			return_data = int(alighting_count[24:30],16)
			alighting_data.value = return_data
			print ("alighting count = ",return_data)
			exit_trigger.value = 1
		elif (alighting_count[14:18]== "0703" or alighting_count[14:18]== "0d03"):
			exit_gate_status.value="open"
			print ("exit_open")
		elif(alighting_count[14:18]== "0003"):
			exit_gate_status.value="close"
			print ("exit_close")
		elif(alighting_count[14:18]== "0d07" or alighting_count [14:18]== "0707"):
			print ("emergency detected...")
			exit_gate_status.value="emergency"
			entry_gate_status.value="emergency"
			manual_mode.value="boarding_stop"
			emergency_detect.value=True
		elif(alighting_count[14:18]== "6109"): #6008  for forward intrusion
			print ("Intrusion detected in Exit Gate..........")
			time.sleep(5)
			if ext_flag.value==True:
				turnstile.exit_start()
			else:
				turnstile.exit_stop()
		elif(alighting_count[14:18]== "0000"):   #after coming to emergency then its show close
			exit_gate_status.value="close"
			entry_gate_status.value="close"



def pis_display(display_flag,vacancy_count,boat_id,terminal_id,route_info):
	disp_flag = 1
	while True:
		if (display_flag.value == "welcome_display"):
			cmd = "SS"+"Welcome to Kochi Water Metro"+"\n"
			data = client.sendall((cmd.encode()))
			print((cmd.encode()))
			time.sleep(10)
		elif (display_flag.value == "msg_display"):
			cmd1 = "L2"+"Vaccancy:" + str(vacancy_count.value) +"\n"
			data = client.sendall((cmd1.encode()))
			print((cmd1.encode()))

			cmd = "S1"+"Route:"+ route_info.value +"\n"
			data = client.sendall((cmd.encode()))
			print((cmd.encode()))
			#print ("length of route:", len(route_info.value),"int:",(int( len(route_info.value))*0.20))
			time.sleep(5)

			'''if (disp_flag == 1):
				cmd = "S1"+"Boat-ID:"+ boat_id.value +"\n"
				data = client.sendall((cmd.encode()))
				print((cmd.encode()))
				disp_flag = 2
				time.sleep(3)
			elif (disp_flag == 2):
				cmd = "S1"+ "Terminal:" + terminal_id.value +"\n"
				data = client.sendall((cmd.encode()))
				print((cmd.encode()))
				disp_flag = 3
				time.sleep(3)
			elif (disp_flag == 3):
				cmd = "S1"+"Route:"+ route_info.value +"\n"
				data = client.sendall((cmd.encode()))
				print((cmd.encode()))
				disp_flag = 1
				time.sleep(5)'''
		elif (display_flag.value == "end_display"):
			cmd = "SS"+"Happy and Safe Journey!"+"\n"
			data = client.sendall((cmd.encode()))
			print((cmd.encode()))
			time.sleep(7)
			if workstation_request.value==False:
				display_flag.value="welcome_display" #extra adding this ##############################
			else:
				display_flag.value="msg_display"
		elif (display_flag.value == "maintain_display"):
			cmd = "SS"+"Its Under Maintainance"+"\n"
			data = client.sendall((cmd.encode()))
			print((cmd.encode()))
			time.sleep(10)

none=""
def ble_scan(none):
	while True:
		returnedList = blescan.parse_events(sock, 10)
		for beacon in returnedList:
				if beacon['major'] == 7200:
					ble_boat_id.value = str(beacon['uuid'][25:32])
					print("BLE Scanning:got boat id=",ble_boat_id.value)
					if(ble_boat_id.value ==boat_id.value):
						boat_detect.value=True
						time_val.value=30 #0 sec timmer after getting boat id
					else:
						boat_detect.value=False
						print ("Different Boat_id detected from ble....")
					#####time_val.value=30 #0 sec timmer after getting boat id
def server(none):
        while True:
                app.run(host='0.0.0.0', port=6000)


#*******************************Multiprocessing  defined for threading************************

manager = multiprocessing.Manager()

#Declrion of global variable for  multiprocess
boarding_data=multiprocessing.Value(ctypes.c_int,0)
alighting_data=multiprocessing.Value(ctypes.c_int,0)
entry_trigger=multiprocessing.Value(ctypes.c_int,0)
exit_trigger=multiprocessing.Value(ctypes.c_int,0)

vacancy_count=multiprocessing.Value(ctypes.c_int,0)
terminal_id=manager.Value(ctypes.c_char_p,0)
route_info=manager.Value(ctypes.c_char_p,0)
boat_id=manager.Value(ctypes.c_char_p,0)
display_flag=manager.Value(ctypes.c_char_p,0)
boat_detect=manager.Value(ctypes.c_char_p,0)
pontoonname=manager.Value(ctypes.c_char_p,0)
entry_gate_status=manager.Value(ctypes.c_char_p,0)
exit_gate_status=manager.Value(ctypes.c_char_p,0)
capacity_count=manager.Value(ctypes.c_int,0)
workstation_request=manager.Value(ctypes.c_char_p,0)
manual_mode=manager.Value(ctypes.c_char_p,0)
boarding_mode=manager.Value(ctypes.c_char_p,0)
ent_flag=manager.Value(ctypes.c_char_p,0)
ext_flag=manager.Value(ctypes.c_char_p,0)
time_val=manager.Value(ctypes.c_int,0)
ble_boat_id=manager.Value(ctypes.c_char_p,0)
emergency_detect=manager.Value(ctypes.c_char_p,0)
tripsrno=manager.Value(ctypes.c_char_p,0)
scheduled_time=manager.Value(ctypes.c_char_p,0)

b= multiprocessing.Process(target= boarding_listen,args=(boarding_data,entry_trigger,))
a= multiprocessing.Process(target= alighting_listen,args=(alighting_data,exit_trigger,))
disp= multiprocessing.Process(target= pis_display,args=(display_flag,vacancy_count,boat_id,terminal_id,route_info,))
ble_multi= multiprocessing.Process(target= ble_scan,args=(none,))
host_server=multiprocessing.Process(target=server,args=(none,))
countdown_timer=multiprocessing.Process(target=timer_func,args=(none,))




host_server.start()
b.start()
a.start()
disp.start()
ble_multi.start()
countdown_timer.start()


boat_detect.value=False
boat_id.value=""
terminal_id.value=""
route_info.value=""
pontoonname.value=""
vacancy_count.value=0
capacity_count.value=0
workstation_request.value=False
manual_mode.value="none"  # this flag will global var for indicate start/stop/emergency
boarding_mode.value="none" # its become manual /automatic based on workstation post  request
ent_flag.value=False # used for intrustion detection and auto set last state of turnstile
ext_flag.value=False # used for intrustion detection and auto set last state of turnstile
time_val.value=0
emergency_detect.value=False
entry_gate_status.value="close"
exit_gate_status.value="close"
tripsrno.value=""
scheduled_time.value=""

'''
def get_route():

	try:
		payload={}
		headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7Il9pZCI6IjYyM2YwZGM2NjA4Yzc1NGUyNjEwMDY2OCIsImZpcnN0X25hbWUiOiJ0ZXN0MSIsImVtYWlsIjoidGVzdDF1c2VyQGdtYWlsLmNvbSIsIm1vYmlsZSI6OTg3NDU2MTIzMH0sImlhdCI6MTY1MDcxMDg4M30.XVzck643LSmvz1S0L3cV4_WyvIw_9vMqvr8KIGLLxGA'} 
		response = requests.request("GET", get_url_1, headers=headers, data=payload)
		y=json.loads(response.text)
		#print(response.text)
		active_session=y["data"]['active_session']
		route_info.value=y["data"]["route_info"]
		terminal_id.value=y["data"]["terminals"][0]["jettyname"]
		pontoonname.value=y["data"]["terminals"][0]["pontoonname"]
		terminal_type=y["data"]["terminals"][0]["terminal_type"]
		terminal_status=y["data"]["terminals"][0]["terminal_status"]
		starting_terminal_stat=y["data"]["starting_terminal_state"]
		capacity_count.value=int(y["data"]["boat_occupancy"])
		vacancy_count.value=int(y["data"]["current_occupancy"])
		print("active_session=",active_session)
		print("route_info=",route_info.value)
		print("jettyname=",terminal_id.value)
		print("pontoonname=",pontoonname)
		print("terminal_type=",terminal_type)
		print("terminal_status=",terminal_status)
		print("boat_occupancy=",capacity_count.value)
		print("current_occupancy=",vacancy_count.value)
		print("starting_terminal_stat=",starting_terminal_stat)
	except Exception as e:
		print("Error during calling OCC server by /api/route_info/get_route_info= ",e)
		pass
'''


def post_alarm():
	global auth
	try:
		payload = json.dumps({
		"pontoonname":"1",
		"entry_gate_status": "close",
		"exit_gate_status": "close",
		"intrusion_entry":"True",
		"intrusion_exit":"True",
		"Emergency":"False"

                })
		print ("Calling to post alarm()and payload is:", payload)

		#headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7Il9pZCI6IjYyM2YwZGM2NjA4Yzc1NGUyNjEwMDY2OCIsImZpcnN0X25hbWUiOiJ0ZXN0MSIs$                # headers declartion in the starting
		response = requests.request("POST", post_url_1, headers=headers, data=payload,timeout=2)
		print (response)
	except requests.Timeout:
		# back off and retry
		print ("2 sec Time_out happend  in Post_alarm api..")
		pass

	except Exception as e:
		print("Error during calling post_alarm = ",e)
		pass



#**************************************************
is_completed=False

def post_event():
	global serf_id,is_completed,auth,my_pontoon
	try:
		payload = json.dumps({
		"serf_id": serf_id,
		"boat_id": str(boat_id.value),
		"terminal_id" :str(terminal_id.value),
		"pontoonname" : str(pontoonname.value),
		"boat_occupancy": str(capacity_count.value),
		"current_occupancy": str(vacancy_count.value),
		"is_completed":str(is_completed),
		"route_info":str(route_info.value),
		"tripsrno":str(tripsrno.value),
		"time":str(scheduled_time.value)
		})
		print ("Calling to post event()and payload is:", payload)

		#headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7Il9pZCI6IjYyM2YwZGM2NjA4Yzc1NGUyNjEwMDY2OCIsImZpcnN0X25hbWUiOiJ0ZXN0MSIsImVtYWlsIjoidGVzdDF1c2VyQGdtYWlsLmNvbSIsIm1vYmlsZSI6OTg3NDU2MTIzMH0sImlhdCI6MTY1MDcxMDg4M30.XVzck643LSmvz1S0L3cV4_WyvIw_9vMqvr8KIGLLxGA','Content-Type': 'application/json'}
		# headers declartion in the starting
		response = requests.request("POST", post_url_1, headers=headers, data=payload,timeout=3)
		print (response)
	except requests.Timeout:
		# back off and retry
		print ("5 sec Time_out happend  in Post_event api..")
		pass

	except Exception as e:
		print("Error during calling post_event api = ",e)
		pass

def both_switch_reset():
	global entry_flag,exit_flag,one_time_flag_entry,one_time_flag_exit
	entry_flag = False
	exit_flag = False
	one_time_flag_entry = True
	one_time_flag_exit = True
	manual_mode.value="none"


def both_turnstile_stop():
	turnstile.entry_stop()
	turnstile.exit_stop()
	entry_trigger.value=0 # discard the triger count 
	exit_trigger.value=0  # discard the triger count

def both_turnstile_start():
	turnstile.entry_start()
	turnstile.exit_start()


def count_start_and_auto_lock():

	if (vacancy_count.value >= 0 and entry_trigger.value == 1):
		entry_trigger.value = 0
		if vacancy_count.value>0 :
			vacancy_count.value = vacancy_count.value - 1
		print ("Available count(by entry)=", vacancy_count.value)
		if (vacancy_count.value == 0):
			manual_mode.value="stop"
			time.sleep(0.5)
			turnstile.entry_stop()
			turnstile.entry_stop()
			turnstile.entry_stop()
			print ("Entry Gate locked automatically")
			#post_event()


	elif (vacancy_count.value <= capacity_count.value and exit_trigger.value == 1):
		exit_trigger.value = 0
		if vacancy_count.value<capacity_count.value :
			vacancy_count.value = vacancy_count.value + 1
		print ("Available count(by exit)=", vacancy_count.value)
		if (vacancy_count.value == capacity_count.value):
			manual_mode.value="stop"
			time.sleep(0.5)
			turnstile.exit_stop()
			turnstile.exit_stop()
			turnstile.exit_stop()
			print ("Exit Gate locked automatically")
			#post_event()




	if (vacancy_count.value == 0 and manual_mode.value=="start"): 
		manual_mode.value="stop"
		time.sleep(0.5)
		turnstile.entry_stop()
		turnstile.entry_stop()
		turnstile.entry_stop()
		print ("Entry Gate locked automatically by start button")


	if (vacancy_count.value == capacity_count.value and manual_mode.value=="start"): 
		manual_mode.value="stop"
		time.sleep(0.5)
		turnstile.exit_stop()
		turnstile.exit_stop()
		turnstile.exit_stop()
		print ("Exit Gate locked automatically by start button")



def clear_boat_data():
	workstation_request.value=False
	manual_mode.value="none"
	vacancy_count.value=0
	capacity_count.value=0
	route_info.value=""
	terminal_id.value=""
	boat_id.value=""
	tripsrno.value=""
	scheduled_time.value=""
	turnstile.clear_vacancy_count()





display_flag.value="welcome_display"
both_turnstile_stop() #both turnstile should  forefully
switch_on() #turn on the switch interrupt



while True:
	try:

		if workstation_request.value==True:
			print ("boat_detect from Workstation=",boat_id.value)
			turnstile.clear_vacancy_count()
			both_switch_reset() #reset the flag of boath switch
			both_turnstile_stop() #both turnstile should  forefully


			if(boarding_mode.value=="manual"):
				is_completed=False  #additional flag to understand the whole process has complited or not
				display_flag.value="msg_display"
				while (manual_mode.value != "boarding_stop") :
					#time.sleep(.5)
					if(boat_detect.value == True):
						print ("Ëntering into ble loop")
						turnstile.clear_vacancy_count()
						both_switch_reset() #reset the flag of boath switch
						both_turnstile_stop() #both turnstile should  forefully
						while (manual_mode.value != "boarding_stop" and  boat_detect.value == True):
							count_start_and_auto_lock() # start to count and auto ock when its reach the count
							#if(manual_mode.value=="stop"):
								#manual_mode.value="none"
								#print("Calling Function post_event...")
								#post_event()
						manual_mode.value="boarding_stop"

					if(manual_mode.value=="boarding_start"):
						print ("Ëntering into manual mode loop")
						turnstile.clear_vacancy_count()
						both_switch_reset() #reset the flag of boath switch
						both_turnstile_stop() #both turnstile should  forefully
						while (manual_mode.value != "boarding_stop"):
							count_start_and_auto_lock() # start to count and auto ock when its reach the count
							#if(manual_mode.value=="stop"):
								#manual_mode.value="none"
								#post_event()
						manual_mode.value="boarding_stop"


				display_flag.value="end_display"  #showing have a safe journey message
				is_completed=True #process completed
				post_event()
				clear_boat_data()
				both_turnstile_stop() #both turnstile off forcefully
				both_switch_reset() #reset the flag of boath switch
				print ("Process completed.........")
				#if(emergency_detect.value==True):
					#emergency_detect.value=False
					#entry_gate_status.value="emergency"
					#exit_gate_status.value="emergency"
		if(manual_mode.value == "boarding_stop"):
			manual_mode.value="none"
			both_turnstile_stop() #both turnstile off forcefully
		if(emergency_detect.value==True):
			emergency_detect.value=False
			entry_gate_status.value="emergency"
			exit_gate_status.value="emergency"




	except KeyboardInterrupt:
		print ("KeyboardInterrupt......")
		host_server.terminate()
		b.terminate()
		a.terminate()
		disp.terminate()
		ble_multi.terminate()
		countdown_timer.terminate()
		GPIO.cleanup() # Clean up
		sys.exit(0)
