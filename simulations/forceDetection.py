import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt




def parse_testfile(filename):
	f = open(filename, 'r')

	x = []
	y = []
	z = []
	while True:
		line = f.readline()

		if line == '':
			break

		line = line.strip()

		if line == '' or line[0] == '#':
			continue

		line = [float(a.strip()) for a in line.split(',')]

		if len(x) == 0:
			x = line

		elif len(y) == 0:
			y = line

		elif len(z) == 0:
			z = line
		
	return (x, y, z)

def main():
	# in_file = '../samples/cristina.txt'
	# in_file = '../samples/mihaib.txt'
	in_file = '../samples/andrei.txt'
	

	x, y, z = parse_testfile(in_file)

	# plt.figure()
	# plt.subplot(311)
	# plt.title('x axis')
	# plt.plot(x)

	# plt.subplot(312)
	# plt.title('y axis')
	# plt.plot(y)

	# plt.subplot(313)
	# plt.title('z axis')
	# plt.plot(z)


	r1 = np.power(x, 2)
	r2 = np.power(y, 2)
	r3 = np.power(z, 2)

	r = np.sqrt(r1 + r2 + r3)

	# plt.figure()
	# plt.subplot(311)
	# plt.plot(r1)

	# plt.subplot(312)
	# plt.plot(r2)

	# plt.subplot(313)
	# plt.plot(r3)


	filter_size = 39
	r1filt = sp.signal.medfilt(r1, [filter_size])
	r2filt = sp.signal.medfilt(r2, [filter_size])
	r3filt = sp.signal.medfilt(r3, [filter_size])

	rfilt = sp.signal.medfilt(r, [filter_size])
	

	plt.figure()
	plt.subplot(211)
	plt.grid()
	plt.plot(r1)

	plt.subplot(212)
	plt.grid()
	plt.plot(r1filt)

	



	plt.show()



if __name__ == '__main__':
	main()

