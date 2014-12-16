import serial
import threading
from collections import deque
import struct

DEFAULT_PORTNUMBER	 	= 3 		# COM 4
DEFAULT_BAUDRATE		= 250000 	
DEFAULT_TIMEOUT 		= 5 		# seconds
DEFAULT_CHUNK_SIZE		= 16 		# bytes


class SerialInterface(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

		self.data = deque()	
		self.data_length = 0

		self.serial = None
		self.serial_buf = ''	

		self.data_access_lock = threading.Lock()
		self.data_chunk_event = threading.Event()
		self.chunk_length = 0

		self.stop_thread = False

	def init_serial(self):
		self.serial = serial.Serial(DEFAULT_PORTNUMBER, DEFAULT_BAUDRATE, timeout = DEFAULT_TIMEOUT)
		self.serial_buf = ''

	def update_serial_config(self):
		pass

	def get_data_length(self):
		self.data_access_lock.acquire(True)
		data_length = self.data_length
		self.data_access_lock.release()

		return data_length

	def get_data(self):
		data = None
		self.data_access_lock.acquire(True)
		if self.data_length:
			data = self.data.pop()
			self.data_length -= 1
		self.data_access_lock.release()

		return data

	def get_data_chunk(self, chunk_length):
		chunk = []

		while True:
			
			self.data_access_lock.acquire(True)

			if self.data_length >= chunk_length:
				for l in range(chunk_length):
					chunk.append(self.data.pop())

				self.data_length -= chunk_length

			else:
				self.chunk_length = chunk_length
				self.data_chunk_event.clear()

			self.data_access_lock.release()

			if len(chunk) >= chunk_length:
				break

			self.data_chunk_event.wait(1)

			if self.stop_thread:
				break

		self.chunk_length = 0
		return chunk
		
	def read_serial_data(self):

		vector = None

		while True:

			line_end_idx = self.serial_buf.find('\xda')

			if line_end_idx == -1:
				data = self.serial.read(DEFAULT_CHUNK_SIZE)
				
				if data == None or len(data) == 0:
					break					
				else:
					self.serial_buf += data
					continue

			line = self.serial_buf[:line_end_idx]
			self.serial_buf = self.serial_buf[line_end_idx + 1:]

			if len(line) != 6:
				continue

			# vector = [a * 0.004 for a in struct.unpack('<hhh', line)]
			vector = [a * 2**(-8) for a in struct.unpack('<hhh', line)]

			break

		return vector

	def run(self):
		self.init_serial()

		while True:
			data = self.read_serial_data()

			self.data_access_lock.acquire(True)

			self.data.appendleft(data)
			self.data_length += 1

			if self.data_length >= self.chunk_length:
				self.data_chunk_event.set()

			self.data_access_lock.release()	

			if self.stop_thread:
				break

		print "Serial Interface has stopped"

	def stop(self):
		self.stop_thread = True
		