from PySide import QtGui
import pyqtgraph as pg
import serialInterface
import computeEngine
import string

DEFAULT_DATA_LENGTH = 9600

class Dashboard(QtGui.QMainWindow):
	
	def __init__(self):
		super(Dashboard, self).__init__()
		# QtGui.QMainWindow.__init__(self)

		self.setWindowTitle('Punching Machine Dashboard')
		
		self.create_graph()
		self.create_actions()
		self.create_toolbar()

		# self.showFullScreen()
		self.showMaximized()

		self.serial_interface = None
		self.compute_engine = None

		self.pause_flag = False

		self.sample_number = 1



	def set_references(self, serial_interface, compute_engine):
		self.serial_interface = serial_interface
		self.compute_engine = compute_engine


	def create_graph(self):
		
		self.plot_widget = pg.GraphicsWindow(parent=self)
		
		self.x_plot = self.plot_widget.addPlot(title='X Axis', pen = (1, 3))
		self.x_plot.setRange(yRange=(-20.0, 20.0))
		self.x_curve = self.x_plot.plot()

		self.y_plot = self.plot_widget.addPlot(title='Y Axis', pen = (2, 3))
		self.y_plot.setRange(yRange=(-20.0, 20.0))
		self.y_curve = self.y_plot.plot()

		self.z_plot = self.plot_widget.addPlot(title='Z Axis')
		self.z_plot.setRange(yRange=(-20.0, 20.0))
		self.z_curve = self.z_plot.plot()

		self.x_data = []
		self.y_data = []
		self.z_data = []
		self.max_data_length = DEFAULT_DATA_LENGTH

		self.setCentralWidget(self.plot_widget)		


	def create_actions(self):
		self.exitAction = QtGui.QAction(QtGui.QIcon('icons/logout.png'), 'Exit', self)
		self.exitAction.setShortcut('Ctrl+Q')
		self.exitAction.setStatusTip('Exit application')
		self.exitAction.triggered.connect(self.close)

		self.clearAction = QtGui.QAction(QtGui.QIcon('icons/clear.png'), 'Clear', self, triggered=self.clear_plot)
		self.clearAction.setStatusTip('Clear the graphs')

		self.pauseAction = QtGui.QAction(QtGui.QIcon('icons/pause.png'), 'Pause', self, triggered=self.pause)

		self.saveAction = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self, triggered=self.save)

		self.fullscreeAction = QtGui.QAction(QtGui.QIcon('icons/fullscreen.gif'), 'Fullscreen', self, triggered = self.fullscreen)
		self.in_fullscreen = False;

		self.aboutAction = QtGui.QAction(QtGui.QIcon('icons/about.png'), 'About', self, triggered=self.about)

	def create_toolbar(self):
		toolbar = self.addToolBar('Main')

		toolbar.addAction(self.exitAction)
		toolbar.addSeparator()

		toolbar.addAction(self.clearAction)
		toolbar.addAction(self.fullscreeAction)

		toolbar.addSeparator()
		toolbar.addAction(self.pauseAction)
		toolbar.addAction(self.saveAction)

		toolbar.addSeparator()
		toolbar.addAction(self.aboutAction)

	def fullscreen(self):
		if self.in_fullscreen:
			self.in_fullscreen = False
			self.showMaximized()
		else:
			self.in_fullscreen = True
			self.showFullScreen()

	def pause(self):
		if self.pause_flag:
			self.pause_flag = False
		else:
			self.pause_flag = True

	def save(self):
		self.pause()

		fname, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save Samples As...', './samples')

		if fname != '':

			try:
				f = open(fname, 'w')
				f.write('# x samples\n\n')

				self.save_data(self.x_data, f)
				
				f.write('# y samples\n\n')
				self.save_data(self.y_data, f)

				f.write('# z samples\n\n')
				self.save_data(self.z_data, f)

				f.close()
			except IOError:
				pass

		self.pause()

	def save_data(self, vector, fd):
		# print [int(a * 2**8) for a in vector[:100]]

		# fd.write(''.join([str(int(a * 2**8)) + ', ' for a in vector]))
		fd.write(','.join([str(a) for a in vector]))
		fd.write('\n\n\n')


	def about(self):
		QtGui.QMessageBox.about(self, "Thanks",
			"<p>The Punching Machine </p><br> 		\
			 <p>Main contributors:<br>				\
			 - Macarascu Cristian (a.k.a. the boss)<br>	\
			 - Mihai <br></p>")

	def closeEvent(self, event):

		if self.serial_interface:
			self.serial_interface.stop()

		if self.compute_engine:
			self.compute_engine.stop()

		event.accept()


	def update_plot(self, x, y, z):

		if self.pause_flag:
			return

		self.x_data += x
		self.y_data += y
		self.z_data += z

		left_limit = -1 * self.max_data_length

		self.x_data = self.x_data[left_limit:]
		self.y_data = self.y_data[left_limit:]
		self.z_data = self.z_data[left_limit:]

		self.x_curve.setData(self.x_data)
		self.y_curve.setData(self.y_data)
		self.z_curve.setData(self.z_data)

		self.plot_widget.update()

	def clear_plot(self):
		self.x_data = []
		self.y_data = []
		self.z_data = []

		self.x_curve.clear()
		self.y_curve.clear()
		self.z_curve.clear()
