import sys
import matplotlib
matplotlib.use('Qt4Agg')
import pylab

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide import QtCore, QtGui

def main():
	app = QtGui.QApplication(sys.argv)

	fig = Figure(figsize=(600, 600), dpi = 72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
	ax = fig.add_subplot(311)
	ax.plot([0, 1])
	ax = fig.add_subplot(312)
	ax.plot([0, 3])
	ax = fig.add_subplot(313)
	ax.plot([0, 10])

	canvas = FigureCanvas(fig)
	wind = QtGui.QMainWindow()

	wind.setCentralWidget(canvas)

	wind.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()