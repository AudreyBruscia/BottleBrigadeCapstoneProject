#############################################################################
# File: calc_trial_length.py
#
# Description: Calculates the remaining duration left in the trial based on
#              dates and times provided in trial_start_time.txt and 
#              trial_end_time.txt.
#
# Authors: Written by Team Bottle Brigade for research trial purposes.
# Primary Author: Jill Thetford (jthetfor@calpoly.edu)
#
# Date: March 3, 2016
#############################################################################

import datetime
import math
import os.path

def calc_length():
	# if trial_end_time.txt does not exist or is empty, don't calculate trial length
	if (not os.path.exists("/boot/BottleBrigade/trial_end_time.txt")):
		return -1
	if (not (os.path.getsize("/boot/BottleBrigade/trial_end_time.txt") > 0)):
		return -1
	
	# open trial start and end time files
	f_end_time = open("/boot/BottleBrigade/trial_end_time.txt", "r")

	# format string that dates are in
	fmt_str = "%d %b %Y %H:%M:%S"

	# get the time from the files

	# strip off newline character if it exists
	str_end = f_end_time.readline()
	str_end = str_end.strip()

	# close the files
	f_end_time.close()

	# get the time from strings as datetime objects
	start = datetime.datetime.now()
	end = datetime.datetime.strptime(str_end, fmt_str)

	# calculate the time between the start and end times
	trial_len = end - start

	# calculate trial length in minutes
	minutes = int(math.ceil(trial_len.total_seconds() / 60))

	return minutes

def main():
	print calc_length()

main()
