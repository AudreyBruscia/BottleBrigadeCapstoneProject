CPE CAPSTONE PROJECT

Team Bottle Brigade Members: Audrey Bruscia, Brandon Eng, Daniel Griffith, Jill Thetford, Myron Zhao
Advisor: Dr. John Oliver
Client: Dr. Alison Ventura
Date: 3/9/2016

Problem Statement: Dr. Alison Ventura will conduct research studies to determine how infant feeding habits effect dietary choices later in life. All trial participants receive a neoprene sleeve that they put on their baby bottle when feeding so that they cannot see how much liquid the infant consumes.

Objective: Our goal is to develop a sensor system to measure and record when the baby bottle is inserted and removed from the neoprene sleeve, using log files to verify the sleeve is being used properly in the study.

State of the Project: We developed multiple prototype sleeves, with sewn sensors and 3D printed enclosure, and improved the design each time. The final sleeve design produces data in a log file stating when the sleeve is on or off the bottle. We concluded that the Raspberry Pi Zero has extensive functionality, which worked well for development, but that causes it to have a large power draw from our battery. Future work would be to find an inexpensive board that can be powered by a household battery.

Associated Files:
  -TrialStart
  -start_trial.py
  -calc_trial_length.py
  -trial_start_time.txt
  -trial_end_time.txt
  
Output Files:
  -trial_data.txt
  -raw_sensors.txt
  -error_log.txt

FORMATTING trial_start_time.txt and trial_end_time.txt files:
    DD MMM YYYY HH:MM:SS
  Example:
    03 Feb 2016 10:40:00
