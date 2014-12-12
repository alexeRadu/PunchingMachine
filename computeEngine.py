import threading
import serialInterface
import dashboard as dash
import numpy as np
import scipy as sp

DEFAULT_DATA_LENGTH 	= 1024

class ComputeEngine(threading.Thread):
	def __init__(self, serial_interface, dashboard):
		threading.Thread.__init__(self)

		self.serial_interface = serial_interface
		self.dashboard = dashboard

		self.data_length = DEFAULT_DATA_LENGTH

		self.stop_thread = False

	def filter(self, data):
		output = []


	def run(self):
		
		while True:

			data = self.serial_interface.get_data_chunk(self.data_length)

			if self.stop_thread:
				self.stop_thread = False
				break
			
			x = [val[0] for val in data]
			y = [val[1] for val in data]
			z = [val[2] for val in data]

			self.dashboard.update_plot(x, y, z)

			
		print "Compute Engine has stopped"

	def stop(self):
		self.stop_thread = True