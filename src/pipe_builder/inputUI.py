import os
from Qt import QtWidgets, QtGui
from functools import partial

WORKFLOW_DIR = os.path.join(os.path.expanduser('~\\Documents'), 'cglumberjack', 'workflows')
if not os.path.exists(WORKFLOW_DIR):
    os.makedirs(WORKFLOW_DIR)

SOFTWARE = ['maya', 'nuke', 's3', 'e3', 'aws sqs', 'lumbermill', 'dashboard', 'google sheets', 'asana', 'ftrack',
            'shotgun', 'github', 'pycharm', 'google forms']


class CreateNodeDialog(QtWidgets.QDialog):
    def __init__(self):
        super(CreateNodeDialog, self).__init__()
        self.button = 'Cancel'
        self.setWindowTitle("Create New Step")
        layout = QtWidgets.QVBoxLayout(self)
        grid = QtWidgets.QGridLayout()
        name_label = QtWidgets.QLabel("Name:")
        software_label = QtWidgets.QLabel("Software:")
        description_label = QtWidgets.QLabel("Description:")
        self.name_line_edit = QtWidgets.QLineEdit()
        self.software_line_edit = QtWidgets.QLineEdit()
        self.description_text_box = QtWidgets.QTextEdit()
        button_layout = QtWidgets.QHBoxLayout()
        ok_button = QtWidgets.QPushButton('Ok')
        cancel_button = QtWidgets.QPushButton('Cancel')
        button_layout.addStretch(1)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(description_label, 1, 0)
        grid.addWidget(self.description_text_box, 1, 1)
        grid.addWidget(software_label, 2, 0)
        grid.addWidget(self.software_line_edit, 2, 1)
        row = 3
        self.software_objects = []
        self.checked_software = []
        for i, each in enumerate(SOFTWARE):
            if i < 5:
                column = 1
                new_row = row

            if i >= 5 and i < 10:
                column = 2
                if row >= 8 and row < 13:
                    new_row = row-5
            if i >= 10:
                column = 3
                if row >= 13:
                    new_row = row-10
            check_box = QtWidgets.QCheckBox(each)
            self.software_objects.append(check_box)
            check_box.clicked.connect(self.on_software_checked)
            grid.addWidget(check_box, new_row, column)
            row += 1

        layout.addLayout(grid)
        layout.addLayout(button_layout)

        ok_button.clicked.connect(self.on_ok_clicked)

    def on_software_checked(self):
        software_string = ''

        for each in self.software_objects:
            if each.isChecked():
                if each not in self.checked_software:
                    self.checked_software.append(each)
        for i, each in enumerate(self.checked_software):
            if i == 0:
                software_string = each.text()
            else:
                software_string = '%s, %s' % (software_string, each.text())
        self.software_line_edit.setText(software_string)

    def on_ok_clicked(self):
        self.button = 'Ok'
        self.accept()

    def get_software_list(self):
        return 'software retrieval not implemented'


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

    # def on_name_edited(self):
    #     name_ = self.output.text()
    #     fixed_name = name_.replace(' ', '_').replace('.', '_')
    #     self.output.setText(fixed_name)
    #     # TODO - this needs to be smarter - there has to be a way to get the last position and set it there.
    #     # self.output.setCursorPosition(100)
    #     return fixed_name

    def return_output(self):
        name_ = self.output.text().replace(' ', '_').replace('.', '_').lower()
        pretty_name = self.output.text()
        return name_, pretty_name


class FileBrowserDialog(QtWidgets.QFileDialog):
    def __init__(self, title, type_):
        super(FileBrowserDialog, self).__init__()
        self.title = title
        self.setDirectory(WORKFLOW_DIR)
        #self.setFileMode(QtWidgets.QFileDialog.AnyFile)

        if type_ == 'open':
            self.setNameFilter(("CGL Graphs (*.json)"))
            self.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        elif type_ == 'save':
            self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        # i need to filter files by .json
        # i need to set the default folder
        # i need to Set the Title for the window



