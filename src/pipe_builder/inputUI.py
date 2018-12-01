
from Qt import QtWidgets
from functools import partial


class NameInputs(QtWidgets.QDialog):
    def __init__(self, _type):
        super(NameInputs, self).__init__()

        lay = QtWidgets.QHBoxLayout()

        lbl_plug = QtWidgets.QLabel('New %s:' % _type)
        self.output = QtWidgets.QLineEdit()
        self.btn_confirm = QtWidgets.QPushButton('Ok')
        self.btn_confirm.clicked.connect(partial(self.closeEvent, self.sender()))

        lay.addWidget(lbl_plug)
        lay.addWidget(self.output)
        lay.addWidget(self.btn_confirm)

        self.setLayout(lay)

    def return_output(self):
        return self.output.text()


class FileBrowserDialog(QtWidgets.QFileDialog):
    def __init__(self, title, type_):
        super(FileBrowserDialog, self).__init__()
        self.title = title
        self.setDirectory('/Users/tmikota/cg_lumberjack')
        self.setFileMode(QtWidgets.QFileDialog.AnyFile)
        if type_ == 'open':
            self.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        elif type_ == 'save':
            self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        # i need to filter files by .json
        # i need to set the default folder
        # i need to Set the Title for the window



