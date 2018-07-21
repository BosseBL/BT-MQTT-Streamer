#--------------- Imports ---------------------------------------------

import bluetooth
import sys
import time
import paho.mqtt.client as mqtt



#------------ Functions ---------------------------------------------

# Scan for bluetooth devices until <addr> is found. 
# When found, tries to connect to the device through <port>.
# Sets the recv timeout to <timeout>.
# This function blocks until it succeds

def discoverConnect(addr, port=1, timeout=5):
	while(True): 
		availableDevs = bluetooth.discover_devices()
		for availableDev in availableDevs:
			if availableDev == addr:
				try:
					socket = bluetooth.BluetoothSocket((bluetooth.RFCOMM))
					socket.connect((addr, port))
					socket.settimeout(timeout)
					break
				except bluetooth.btcommon.BluetoothError as error:
					socket.close()
					print "could not connect to ", addr, ".\nError: ", error, "\nTry reconnect in 3 sec"
					time.sleep(3)
					break
		sleep(5)
	return socket



#--------------------- Initialize --------------------------------------

# sets bd_addr, mqttBroker and topic to whats specified in argv or default

if len(sys.argv) == 4:
	bd_addr = sys.argv[1]
	mqttBroker = sys.argv[2]
	topic = sys.argv[3]
else:
	bd_addr = 20:13:06:14:30:50
	mqttBroker = "url"
	topic = ""


exit = 0
buff = ""



#---------------------- Main loop -----------------------------------------

# connects to bd_addr and loop (receive data from bd_addr, send data to mqttBroker).
# ctrl-c exits loop.
# If data receive timeout, try reconnect to bd_addr

socket = discoverConnect(bd_addr, timeout = 30)
while exit == 0:

	try:
		data = socket.recv(1)
		if data == '\n':
			publish.single(topic, data, qos=1, retain=True)
			print "published: ", buff, "\n"
			buff = ""
		else:
			buff += data
			
	except KeyboardInterrupt:
    	print "exiting\n"
    	exit = 1
	except bluetooth.btcommon.BluetoothError as error:
    	print "could not receive data.\n Error: ", error, "\nTry reconnect"
    	socket.close()
    	socket = discoverConnect(bd_addr)
    	
socket.close()




#---------------------do-list----------------------------------
# - tidsstämpla data?
# - hur lång timeout? arduino måste förmodligen sända data regelbundet (var 20 sek?)
# för att inte klienten ska tro att förbindelsen brutits.
# - qos och retain ?
# - ska data formateras om innan mqtt (ex splitta left,right på olika ämnen)
# - ska något ID sändas med för att mottagaren ska veta exakt vilken sensor modul?
#