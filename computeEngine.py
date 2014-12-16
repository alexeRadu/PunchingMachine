import threading
import serialInterface
import dashboard as dash
import Display as display
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

		self.measuring = False
		self.treshold = 8 # g**2
		self.samples = 0
		self.samples_measured = 6400 # samples ~ 2 sec
		self.metric = 0

		self.display  = display.Display()

	def filter(self, data):
		output = []


	def run(self):
		
		while True:

			data = self.serial_interface.get_data_chunk(self.data_length)
			cur_sampl = 0

			if self.stop_thread:
				self.stop_thread = False
				break
			
			x = [val[0] for val in data]
			y = [val[1] for val in data]
			z = [val[2] for val in data]

			self.dashboard.update_plot(x, y, z)

			if self.measuring == False:
				cur_sampl = 0

				for samp in x:
					cur_sampl += 1
					val = samp * samp
					
					if val > self.treshold:
						self.metric = 0
						self.measuring = True
						break


			if self.measuring == True:

				while True:

					if cur_sampl  == len(x):
						cur_sampl = 0
						break

					samp = x[cur_sampl]
					cur_sampl += 1

					val = samp * samp
					self.metric += val
					self.samples += 1

					if self.samples >= self.samples_measured:
						print self.metric

						if self.metric < 30000:
							print 'level 1'
							self.display.move_osc(0, 1)
						elif self.metric < 40000:
							print 'level 2'
							self.display.move_osc(1, 1)
						elif self.metric < 50000:
							print 'level 3'
							self.display.move_osc(2, 1)
						elif self.metric < 60000:
							print 'level 4'
							self.display.move_osc(3, 2)
						else:
							print 'level 5'
							self.display.move_osc(4, 1)

						self.measuring = False
						self.samples = 0
						self.metric = 0
						break


			
		print "Compute Engine has stopped"

	def stop(self):
		self.stop_thread = True