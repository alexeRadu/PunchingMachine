import serialInterface
# import computeEngine
import time

def main():
	serial_interface = serialInterface.SerialInterface()
	# compute_engine = computeEngine.ComputeEngine(serial_interface)

	# compute_engine.start()
	serial_interface.start()


	time.sleep(10000)


if __name__ == '__main__':
	main()