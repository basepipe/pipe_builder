from Qt import QtWidgets, QtGui, QtCore

from inputUI import FileBrowserDialog


class NavBar(QtWidgets.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        lay = QtGui.QHBoxLayout()
        self.title = QtGui.QLabel('File')
        lay.addWidget(self.title)
        self.setLayout(lay)


class Toolbar(QtWidgets.QWidget):
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
        self.savebtn = QtWidgets.QPushButton('Save Graph')
        self.loadbtn = QtWidgets.QPushButton('Load Graph')
        # self.csvbtn = QtWidgets.QPushButton('Create CSV')
        # self.pdfbtn = QtWidgets.QPushButton('Create PDF')

        self.addbtn.clicked.connect(self.graph_create_node)
        self.savebtn.clicked.connect(self.save)
        self.loadbtn.clicked.connect(self.load)
        # self.csvbtn.clicked.connect(self.csv)
        # self.pdfbtn.clicked.connect(self.pdf)

        lay.addWidget(self.addbtn)
        # lay.addWidget(self.toolbtn)
        lay.addWidget(self.savebtn)
        lay.addWidget(self.loadbtn)
        # lay.addWidget(self.csvbtn)
        # lay.addWidget(self.pdfbtn)
        lay.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.setLayout(lay)

    def graph_create_node(self):
        defaults = {'description': 'None', 'pipeID': 1, 'software': '', 'other': 'Test', 'preflight_data': {}}
        self.graph.createNode(name='NewNode', preset='node_preset_1', position=None, **defaults)

    def save(self):
        dialog = FileBrowserDialog('Save Pipeline Graph', 'save')
        dialog.exec_()
        self.graph.saveGraph(filePath=dialog.selectedFiles()[0])

    def load(self):
        dialog = FileBrowserDialog('Open Pipeline File', 'open')
        dialog.exec_()
        self.graph.loadGraph(filePath=dialog.selectedFiles()[0])

    def csv(self):
        dialog = FileBrowserDialog("Export CSV", "save")
        dialog.exec_()
        self.graph.saveCSV(filePath=dialog.selectedFiles()[0])

    def pdf(self):
        dialog = FileBrowserDialog("Export Graph Image", "save")
        dialog.exec_()
        self.graph.exportImage(filePath=dialog.selectedFiles()[0])