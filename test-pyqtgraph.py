import sys
from PySide import QtGui

import dashboard as dshb
import serialInterface
import computeEngine

def main():
	app = QtGui.QApplication(sys.argv)

	dashboard = dshb.Dashboard()

	serial_interface = serialInterface.SerialInterface()
	compute_engine = computeEngine.ComputeEngine(serial_interface, dashboard)

	dashboard.set_references(serial_interface, compute_engine)

	compute_engine.start()
	serial_interface.start()


	sys.exit(app.exec_())

if __name__ == "__main__":
	main()