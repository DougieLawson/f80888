#!/usr/bin/python

# (C) 2015 Copyright Dougie Lawson, All rights reserved
# (C) 2016 Copyright Darkside Logic (One) Ltd. All rights reserved
# Version 0.9.1

from time import sleep             # lets us have a delay
import mosquitto
import os
import time
import sys
import syslog
import signal
import pinControl as p

syslog.syslog('Control server started')

def term_handler(signal, frame):
	syslog.syslog('Term signal received')
	syslog.syslog('Control server terminated')
	sys.exit(0)

def on_connect(self, userd, rc):
	syslog.syslog('MQTT connect rc:'+str(rc))


def on_message(self, userd, msg):
#	print "Message received on topic: "+msg.topic+ "... with QoS: "+str(msg.qos)+ "... and payload: "+str(msg.payload)
#	syslog.syslog( "Message received on topic: "+msg.topic+ " payload: "+str(msg.payload))
	t1, bank, pin = msg.topic.split('/')
	if pin == 'all':
		for i in range(1,9):
			if msg.payload == 'on':
				p.pinOn(bank, i)
			else:
				p.pinOff(bank, i)
	else:
		pin = int(pin)
		#print  " Bank:", bank, " Pin:", pin, msg.payload
		if msg.payload == 'on':
			p.pinOn(bank, pin)
		else:
			p.pinOff(bank, pin)
		print ("Status: ", bank, pin, p.pinStatus(bank, pin))

def main():
	# Start with all off
	p.pinAllOff()

	signal.signal(signal.SIGTERM, term_handler)
	broker = "pi-server"
	port = 1883

	mypid = os.getpid()
	sub_uniq = "subclient_"+str(mypid)
	mqtts = mosquitto.Mosquitto(sub_uniq)
	mqtts.on_connect = on_connect
	mqtts.on_message = on_message

	while True:
		mqtts.connect(broker, port, 60)
		mqtts.subscribe("relay/#", 0)

		try:
			rc = 0
			while rc == 0:
				rc = mqtts.loop()
#			syslog.syslog('Try: Exception caught rc:' +str(rc))

		except Exception as inst:
			p.pinAllOff()
			print type(inst)
			print inst.args
			print inst 
			mqtts.disconnect()
			syslog.syslog(syslog.LOG_ERR, 'Except: Exception caught'+str(inst))
			return 4

if __name__ == "__main__":
	sys.exit(main())
