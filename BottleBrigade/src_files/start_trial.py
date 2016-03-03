#############################################################################
# File: start_trail.py
#
# Description: Reads signals from two pressure sensors on the top and bottom 
#              of the sewn sleeve. Registers the current state and previous
#              state of the sleeve (on or off). Writes each sensor's 
#              individual data to raw_sensors.txt. Writes errors to 
#              error_log.txt. Writes valid on/off data to trial_data.txt.
#              All log files include timestamps for each event. Stops 1 min
#              before the scheduled shutdown.
#
# Authors: Written by Team Bottle Brigade for research trial purposes.
# Primary Author: Audrey Bruscia (abruscia@calpoly.edu)
#
# Date: February 29, 2016
#############################################################################

from gpiozero import Button
from time import sleep 
import datetime
import os
import calc_trial_length

#Log File paths
raw_sensors = "/boot/BottleBrigade/raw_sensors.txt"
trial_data = "/boot/BottleBrigade/trial_data.txt"
error_log = "/boot/BottleBrigade/error_log.txt"

#Date Time files
trial_start_time = "/boot/BottleBrigade/trial_start_time.txt" 

#Possible states
ON = 1 #Sleeve is fully on the bottle
OFF = 0 #Sleeve is fully off the bottle
ILLEGAL = 3 
state = OFF

#illegal state flag
illegal = False

#Analog sensor values, initialize off
top_sensor = 0 
bottom_sensor = 0
prev_sensor_top = 0 
prev_sensor_bottom = 0 

#Initialize timestamp info
curDateTime = datetime.datetime(1,1,1)

#System run flag
run = True

def init_files():
   timestamp = curDateTime.now().ctime() #get the timestamp string

   f_raw_sensors = open(raw_sensors, 'a')
   f_raw_sensors.write("\n\n*****************Start of Trial*****************" + "\n")
   f_raw_sensors.write(timestamp + "\n")
   f_raw_sensors.write("************************************************\n\n")
   f_raw_sensors.close()

   f_trial_data = open(trial_data, 'a')
   f_trial_data.write("\n\n*****************Start of Trial*****************" + "\n")
   f_trial_data.write(timestamp + "\n")
   f_trial_data.write("************************************************\n\n")
   f_trial_data.close()

   f_error_log = open(error_log, 'a')
   f_error_log.write("\n\n*****************Start of Trial*****************" + "\n")
   f_error_log.write(timestamp + "\n")
   f_error_log.write("************************************************\n\n")
   f_error_log.close()
   
def init_sensors():
   global top_sensor
   global bottom_sensor
   
   #****PINOUT INFO****
   top_sensor = Button(12, True)
   print "Top sensor initialized" 
   bottom_sensor = Button(16, True)
   print "Bottom sensor initialized" 
   
def update_state():
   global state
   global illegal

   if state == ON and top_sensor.is_pressed and bottom_sensor.is_pressed:
      state = ON
      illegal = False
   elif state == OFF and not top_sensor.is_pressed and not bottom_sensor.is_pressed:
      state = OFF
      illegal = False
   elif state == ON and not top_sensor.is_pressed and not bottom_sensor.is_pressed:
      state = OFF
      illegal = False
   elif state == OFF and top_sensor.is_pressed and bottom_sensor.is_pressed:
      state = ON
      illegal = False
   elif not top_sensor.is_pressed and bottom_sensor.is_pressed:
      state = ILLEGAL
      if not illegal:
         print "ILLEGAL state" 
         write_to_raw_sensors("ERROR")
   else:
      pass
         
def update_raw_log():
   global prev_sensor_top
   global prev_sensor_bottom 

   if not prev_sensor_top and top_sensor.is_pressed:
      write_to_raw_sensors("Top sensor on")
      prev_sensor_top = 1
   elif prev_sensor_top and not top_sensor.is_pressed:
      write_to_raw_sensors("Top sensor off")
      prev_sensor_top = 0 
   if prev_sensor_bottom and not bottom_sensor.is_pressed:
      write_to_raw_sensors("Bottom sensor off")
      prev_sensor_bottom = 0
   elif not prev_sensor_bottom and bottom_sensor.is_pressed:
      write_to_raw_sensors("Bottom sensor on")
      prev_sensor_bottom = 1

def update_data_logs(prev_state):
   global state
   global illegal

   if prev_state == state: 
      #do nothing
      pass
   elif prev_state == ON:
      if state == ILLEGAL:
         if not illegal: 
            illegal = True
            #error
            write_to_error_log("ERROR: prev_state ON")
            print "Error" 
         state = prev_state
      else:
         print "Sleeve off" 
         write_to_trial_data("Sleeve off")
         write_to_raw_sensors("Top sensor off")
   elif prev_state == OFF:
      if state == ILLEGAL:
         if not illegal: 
            illegal = True
            #error
            write_to_error_log("ERROR: prev_state OFF")
            print "Error" 
         state = prev_state
      else:
         print "Sleeve on" 
         write_to_trial_data("Sleeve on")
         write_to_raw_sensors("Bottom sensor on")
   else:
      if not illegal: 
         illegal = True
         #error
         write_to_error_log("ERROR: prev_state unknown")
         print "Error"
      state = OFF

def write_to_raw_sensors(sensor): #parameter is string "Top sensor" or "Bottom sensor"
   timestamp = curDateTime.now().ctime() #get the timestamp string

   f_raw_sensors = open(raw_sensors, 'a')
   f_raw_sensors.write(sensor.ljust(20) + "\t"  + timestamp + "\n") 
   f_raw_sensors.close()
   
def write_to_trial_data(on_or_off): #parameter is string "Sleeve On" or "Sleeve Off"
   timestamp = curDateTime.now().ctime() #get the timestamp string 

   f_trial_data = open(trial_data, 'a')
   f_trial_data.write(on_or_off + "\t" + timestamp + "\n") 
   f_trial_data.close()
   
def write_to_error_log(error_message): #parameter is string of an error message
   timestamp = curDateTime.now().ctime() #get the timestamp string

   f_error_log = open(error_log, 'a')
   f_error_log.write(error_message + "\t" + timestamp + "\n") 
   f_error_log.close()

   
def main():
   global run

   init_files()
   init_sensors()

   #clear the trial_start_time.txt so reboots will not reset system time
   f_trial_start_time = open(trial_start_time, 'w+') #open in truncate
   f_trial_start_time.close()
   
   while run:
      sleep(1)
      prev_state = state
      update_state()
      update_raw_log()
      update_data_logs(prev_state)

      if(calc_trial_length.calc_length() == 1):
         run = False;

   print "Program Ending.  Shutting Down."
   
   return 0
     
   
main()
