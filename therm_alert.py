
#!/usr/bin/env python
#
__author__ = "Zong-Xiao He"
__copyright__ = "Copyright 2015 Zong-Xiao He"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "zongxiah@bcm.edu"
__date__ = "2015-11-15"

from instapush import Instapush, App
from datetime import datetime, time
import sys
import json
THERMFILE = "/sys/bus/w1/devices/28-000005212010/w1_slave"
TEMP_LOWER, TEMP_UPPER = 24, 26

# read config
with open('.config') as jfile:
	dat = json.load(jfile)
	INSTAPUSH_ID = dat['instapush_id']
	INSTAPUSH_SECRET = dat['instapush_secret']
	YEELINK_KEY = dat['yeelink_key']

def push_notification(message):
	app = App(appid=INSTAPUSH_ID, secret=INSTAPUSH_SECRET)
	app.notify(event_name='ThermAlert', trackers={ 'message': message})

def read_temperature():
	tfile = open(THERMFILE) 
	# Read all of the text in the file. 
	text = tfile.read() 
	# Close the file now that the text has been read. 
	tfile.close() 
	# Split the text with new lines (\n) and select the second line. 
	secondline = text.split("\n")[1] 
	temperaturedata = secondline.split(" ")[9] 
	temperature = float(temperaturedata[2:]) 
	temperature = temperature / 1000 
	return temperature

def mona_is_sleeping():
	now = datetime.now()
	if now.time() <= time(7,00) or now.time() >= time(20,00): 
		return True 
	else:
		return False

# def write_to_yeelink():
# 	"""
# 	yeelink key: YEELINK_KEY
# 	"""

if __name__ == '__main__':
	temp = read_temperature()
	# TODO: write temp

	# send notification
	if mona_is_sleeping():
		if temp < TEMP_LOWER:
			push_notification("It's too cold for Mona ({:4.2f} now)!".format(temp))
		elif temp > TEMP_UPPER:
			push_notification("It's too hot for Mona ({:4.2f} now)!".format(temp))


