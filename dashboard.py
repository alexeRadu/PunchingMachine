from PySide import QtGui
import pyqtgraph as pg
import serialInterface
import computeEngine

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

	def set_references(self, serial_interface, compute_engine):
		self.serial_interface = serial_interface
		self.compute_engine = compute_engine


	def create_graph(self):
		
		self.plot_widget = pg.GraphicsWindow(parent=self)
		
		self.x_plot = self.plot_widget.addPlot(title='X Axis', pen = (1, 3))
		self.x_plot.setRange(yRange=(-16.0, 16.0))
		self.x_curve = self.x_plot.plot()

		self.y_plot = self.plot_widget.addPlot(title='Y Axis', pen = (2, 3))
		self.y_plot.setRange(yRange=(-16.0, 16.0))
		self.y_curve = self.y_plot.plot()

		self.z_plot = self.plot_widget.addPlot(title='Z Axis')
		self.z_plot.setRange(yRange=(-16.0, 16.0))
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
		toolbar.addAction(self.aboutAction)

	def fullscreen(self):
		if self.in_fullscreen:
			self.in_fullscreen = False
			self.showMaximized()
		else:
			self.in_fullscreen = True
			self.showFullScreen()


	def about(self):
		QtGui.QMessageBox.about(self, "Thanks",
			"<p>The Punching Machine </p><br> 		\
			 <p>Main contributors:<br>				\
			 - Macarascu Cristian (a.k.a. the boss)<br>	\
			 - others<br></p>")

	def closeEvent(self, event):

		if self.serial_interface:
			self.serial_interface.stop()

		if self.compute_engine:
			self.compute_engine.stop()

		event.accept()


	def update_plot(self, x, y, z):
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
