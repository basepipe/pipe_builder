from Qt import QtWidgets, QtGui, QtCore
import random
from .inputUI import FileBrowserDialog, CreateNodeDialog


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
        lay = QtWidgets.QHBoxLayout()
        # self.toolbtn = QtWidgets.QPushButton('tools')
        # self.setbtn = QtWidgets.QPushButton('settings')
        self.addbtn = QtWidgets.QPushButton('New Step')
        self.toolbtn = QtWidgets.QPushButton('tools')
        self.savebtn = QtWidgets.QPushButton('Save As')
        self.loadbtn = QtWidgets.QPushButton('Import Graph')
        self.openbtn = QtWidgets.QPushButton('Open Graph')
        # self.csvbtn = QtWidgets.QPushButton('Create CSV')
        self.pdfbtn = QtWidgets.QPushButton('Export JPG')
        self.failure_points_label = QtWidgets.QLabel('Failure Points:')
        self.failure_points_number = QtWidgets.QLabel('Not Calculated')

        self.addbtn.clicked.connect(self.graph_create_node)
        self.savebtn.clicked.connect(self.save_as)
        self.loadbtn.clicked.connect(self.load)
        self.openbtn.clicked.connect(self.open)
        # self.csvbtn.clicked.connect(self.csv)
        self.pdfbtn.clicked.connect(self.pdf)

        lay.addWidget(self.addbtn)
        # lay.addWidget(self.toolbtn)
        lay.addWidget(self.savebtn)
        lay.addWidget(self.loadbtn)
        lay.addWidget(self.openbtn)
        # lay.addWidget(self.csvbtn)
        lay.addWidget(self.pdfbtn)
        lay.addStretch(1)
        lay.addWidget(self.failure_points_label)
        lay.addWidget(self.failure_points_number)
        lay.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.setLayout(lay)

    def graph_create_node(self):
        dialog = CreateNodeDialog()
        dialog.exec_()
        if dialog.button == 'Ok':
            defaults = {'description': dialog.description_text_box.toPlainText(),
                        'pipeID': random.randint(1, 1001),
                        'software': dialog.software_line_edit.text().replace(' ', '_').replace('.', '_').lower(),
                        'other': 'Test', 'preflight_data': {}}
            self.graph.createNode(name=dialog.name_line_edit.text().replace(' ', '_').replace('.', '_').lower(),
                                  preset='node_preset_1',
                                  position=None,
                                  **defaults)

    def save_as(self):
        dialog = FileBrowserDialog('Save Pipeline Graph', 'save')
        dialog.exec_()
        self.graph.saveGraph(filePath=dialog.selectedFiles()[0])
        self.filename_changed.emit(dialog.selectedFiles()[0])

    def load(self):
        dialog = FileBrowserDialog('Open Pipeline File', 'open')
        dialog.exec_()
        self.graph.loadGraph(filePath=dialog.selectedFiles()[0])

    def update_failure_points(self):
        automated, manual = self.graph.analyze_connections()
        self.failure_points_number.setText('%s/%s' % (str(manual), str(automated*2+manual)))

    def open(self):
        # TODO - clear the current graph
        dialog = FileBrowserDialog('Open Pipeline File', 'open')
        dialog.exec_()
        self.graph.clearGraph()
        self.graph.loadGraph(filePath=dialog.selectedFiles()[0])
        self.filename_changed.emit(dialog.selectedFiles()[0])
        self.update_failure_points()

    def csv(self):
        dialog = FileBrowserDialog("Export CSV", "save")
        dialog.exec_()
        self.graph.saveCSV(filePath=dialog.selectedFiles()[0])

    def pdf(self):
        # TODO Save the graph first
        import os
        dialog = FileBrowserDialog("Export Graph Image", "save")
        dialog.exec_()
        self.graph.saveGraph()
        self.graph.exportImage(filePath=dialog.selectedFiles()[0])
        # TODO - currently my only option is to close the app when saving pdf files because we
        # end up locking the interface when we create pdfs.
        self.parent.accept()

