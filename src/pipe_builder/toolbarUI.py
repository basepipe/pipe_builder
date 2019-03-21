from Qt import QtWidgets, QtGui, QtCore
import random
from inputUI import FileBrowserDialog


class NavBar(QtWidgets.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        lay = QtGui.QHBoxLayout()
        self.title = QtGui.QLabel('File')
        lay.addWidget(self.title)
        self.setLayout(lay)


class Toolbar(QtWidgets.QWidget):
    filename_changed = QtCore.Signal(object)

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent
        self.graph = parent.graph
        self.setMaximumWidth(100)
        self.setMinimumWidth(100)
        lay = QtWidgets.QVBoxLayout()
        # self.toolbtn = QtWidgets.QPushButton('tools')
        # self.setbtn = QtWidgets.QPushButton('settings')
        self.addbtn = QtWidgets.QPushButton('Add Node')
        self.toolbtn = QtWidgets.QPushButton('tools')
        self.savebtn = QtWidgets.QPushButton('Save As')
        self.loadbtn = QtWidgets.QPushButton('Import Graph')
        self.openbtn = QtWidgets.QPushButton('Open Graph')
        # self.csvbtn = QtWidgets.QPushButton('Create CSV')
        # self.pdfbtn = QtWidgets.QPushButton('Create PDF')

        self.addbtn.clicked.connect(self.graph_create_node)
        self.savebtn.clicked.connect(self.save_as)
        self.loadbtn.clicked.connect(self.load)
        self.openbtn.clicked.connect(self.open)
        # self.csvbtn.clicked.connect(self.csv)
        # self.pdfbtn.clicked.connect(self.pdf)

        lay.addWidget(self.addbtn)
        # lay.addWidget(self.toolbtn)
        lay.addWidget(self.savebtn)
        lay.addWidget(self.loadbtn)
        lay.addWidget(self.openbtn)
        # lay.addWidget(self.csvbtn)
        # lay.addWidget(self.pdfbtn)
        lay.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.setLayout(lay)

    def graph_create_node(self):
        defaults = {'description': 'None', 'pipeID': random.randint(1, 1001), 'software': '',
                    'other': 'Test', 'preflight_data': {}}
        self.graph.createNode(name='NewNode', preset='node_preset_1', position=None, **defaults)

    def save_as(self):
        dialog = FileBrowserDialog('Save Pipeline Graph', 'save')
        dialog.exec_()
        self.graph.saveGraph(filePath=dialog.selectedFiles()[0])
        self.filename_changed.emit(dialog.selectedFiles()[0])

    def load(self):
        dialog = FileBrowserDialog('Open Pipeline File', 'open')
        dialog.exec_()
        self.graph.loadGraph(filePath=dialog.selectedFiles()[0])

    def open(self):
        # TODO - clear the current graph
        dialog = FileBrowserDialog('Open Pipeline File', 'open')
        dialog.exec_()
        self.graph.loadGraph(filePath=dialog.selectedFiles()[0])
        self.filename_changed.emit(dialog.selectedFiles()[0])

    def csv(self):
        dialog = FileBrowserDialog("Export CSV", "save")
        dialog.exec_()
        self.graph.saveCSV(filePath=dialog.selectedFiles()[0])

    def pdf(self):
        dialog = FileBrowserDialog("Export Graph Image", "save")
        dialog.exec_()
        self.graph.exportImage(filePath=dialog.selectedFiles()[0])