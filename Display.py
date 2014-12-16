import serial as ser

COM_PORT 	= 4 # COM 5
BAUD_RATE 	= 115200
TIMEOUT 	= 1

class Display:
	def __init__(self):
		self.serial = ser.Serial()

		self.serial.baudrate 	= BAUD_RATE
		self.serial.port 		= COM_PORT
		self.serial.timeout		= TIMEOUT

		self.serial.open()

		self.vals = [[150, 140, 130], [120, 114, 106], [100, 90, 80], [75, 64, 60], [50, 45, 40]]

	def move(self, sect, section):
		msg = r'' + 'n' + str(self.vals[sect][section]) + '\r'
		self.serial.write(msg)

	def move_osc(self, sect, section):
		msg = r'' + 'o' + str(self.vals[sect][section]) + '\r'
		self.serial.write(msg)


	def base(self):
		base_angle = r'' + 'n' + '150' + '\r'
		self.serial.write(base_angle);

	