#!/usr/bin/python

# (C) 2015 Copyright Dougie Lawson, All rights reserved
# (C) 2016 Copyright Darkside Logic (One) Ltd. All rights reserved
# Version 0.9.1

import smbus

ADDR = 0x27 
IODIRA = 0x00
IODIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13
OLATA = 0x14
OLATB = 0x15

bus=smbus.SMBus(1)

bus.write_byte_data(ADDR,IODIRA,0x00)
bus.write_byte_data(ADDR,IODIRB,0x00)
global valueA
global valueB
valueA=0
valueB=0

def pinOff(bank, pin):
#  print (bank,  pin, "== ON")
  global valueA
  global valueB
  bit = pin - 1
  if bank == 'top': 
    valueB = valueB | (1 << bit)
    bus.write_byte_data(ADDR, OLATB, valueB)
  else:
    valueA = valueA | (1 << bit)
    bus.write_byte_data(ADDR, OLATA, valueA)

def pinOn(bank, pin):
#  print (bank, pin, "== OFF")
  global valueA
  global valueB
  bit = pin - 1
  if (bank == 'top'): 
    valueB = valueB & (0xff - (1 << bit))
    bus.write_byte_data(ADDR, OLATB, valueB)
  else:
    valueA = valueA & (0xff - (1 << bit))
    bus.write_byte_data(ADDR, OLATA, valueA)

def pinStatus(bank, pin):
  global valueA
  global valueB
  bit = pin - 1
  if (bank == 'top'):
    state = ((valueB&(1<<bit))!=0)
  else:
    state = ((valueA&(1<<bit))!=0)
  return state

def pinAllOff():
#  print "All off called"
  global valueA
  global valueB
  valueA = 0xFF
  bus.write_byte_data(ADDR, OLATA, valueA)
  valueB = 0xFF
  bus.write_byte_data(ADDR, OLATB, valueB)
