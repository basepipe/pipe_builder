from Qt import QtWidgets, QtGui, QtCore


class NodeSettingWidget(QtWidgets.QWidget):
    signal_SaveSettings = QtCore.Signal(dict)
    signal_nothing_selected = QtCore.Signal()
    signal_something_selected = QtCore.Signal()

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)
        self.setObjectName('NodeSettingWidget')
        self.parent = parent
        self.graph = parent.graph
        self.settings = {}

        self.initialize()

        self.setMinimumWidth(350)
        # self.setMaximumHeight(740)
        self.setMinimumHeight(740)
        self.setLayout(self.lay)
        self.node_settings_box = None


    def initialize(self):
        '''
        creates top bar
        :return:
        '''

        self.lay = QtWidgets.QVBoxLayout()
        self.lay.setAlignment(QtCore.Qt.AlignTop)
        self.settings_box = QtWidgets.QVBoxLayout()
        self.lay.addLayout(self.settings_box)

    def refresh(self, settingData):
        # clear out widget
        self.settings = settingData
        if self.settings:
            self.signal_something_selected.emit()
            for i in reversed(range(self.settings_box.count())):
                self.settings_box.itemAt(i).widget().setParent(None)

            # add default settings
            for settings in settingData:
                self.node_settings_box = NodeSettingsBox(parent=self.parent, values=settings, save=self._savesettings)
                self.settings_box.addWidget(self.node_settings_box)
        else:
            self.signal_nothing_selected.emit()

    def _savesettings(self):
        for i in reversed(range(self.settings_box.count())):
            self.settings_box.itemAt(i).widget()._save_properties()
        self.signal_SaveSettings.emit(self.settings)


class NodeSettingsBox(QtWidgets.QTabWidget):

    def __init__(self, parent, values, save):
        QtWidgets.QTabWidget.__init__(self)

        self.old_name = None
        self.tab_settings = QtWidgets.QWidget()
        self.tab_preflights = QtWidgets.QWidget()
        self.tab_shelf = QtWidgets.QWidget()
        self.tab_attrs = QtWidgets.QWidget()
        self.tab_outputs = QtWidgets.QWidget()
        self.values = values
        self.setObjectName('NodeSettingsBox')
        self.parent = parent
        self.widget = QtWidgets.QWidget()
        self.lay_settings = QtWidgets.QVBoxLayout(self.tab_settings)
        self.lay_attrs = QtWidgets.QVBoxLayout(self.tab_attrs)
        self.lay_shelf = QtWidgets.QVBoxLayout(self.tab_shelf)
        self.lay_preflights = QtWidgets.QVBoxLayout(self.tab_preflights)
        self.attrs_dict = {'Settings': {},
                           'Connections': {},
                           'Shelf': {},
                           'Preflights': {}}

        self.addTab(self.tab_settings, 'Settings')
        self.addTab(self.tab_attrs, 'Connections')
        self.addTab(self.tab_shelf, 'Shelf')
        self.addTab(self.tab_preflights, 'Preflights')

        # add node properties
        header_items = ['Name', 'Automation Level', 'Priority', 'Methodology', 'Duration',
                        'Frequency', 'Number People Effected', 'Pretty Name']

        # add the input table
        self.inputs_table = QtWidgets.QTableWidget()
        self.inputs_table.setColumnCount(len(header_items))
        self.inputs_table.setHorizontalHeaderLabels(header_items)
        header = self.inputs_table.horizontalHeader()
        # TODO - looks like my mac is pulling QT5 rather than QT4 - need to solve that.
        # header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        self.outputs_table = QtWidgets.QTableWidget()
        self.outputs_table.setColumnCount(len(header_items))
        self.outputs_table.setHorizontalHeaderLabels(header_items)
        self.outputs_table.horizontalHeader().setStretchLastSection(True)
        self.preflights_table = QtWidgets.QTableWidget()
        self.preflights_table.horizontalHeader().setStretchLastSection(True)
        self.preflights_table.setColumnCount(4)
        self.preflights_table.setHorizontalHeaderLabels(['Name', 'Description', 'Required', 'Module'])

        self.inputs_label = QtWidgets.QLabel('Inputs')
        self.outputs_label = QtWidgets.QLabel("Outputs")
        self.preflights_label = QtWidgets.QLabel("Preflights")

        self.add_preflight = QtWidgets.QToolButton()
        self.add_preflight.setText('+')
        self.preflight_line_edit = QtWidgets.QLineEdit()

        self.pref_layout = QtWidgets.QHBoxLayout()
        self.pref_layout.addWidget(self.preflights_label)
        self.pref_layout.addWidget(self.preflight_line_edit)
        self.pref_layout.addWidget(self.add_preflight)

        self.spawn_properties(values=values, save=save)
        self.lay_attrs.addWidget(self.inputs_label)
        self.lay_attrs.addWidget(self.inputs_table)
        self.lay_attrs.addWidget(self.outputs_label)
        self.lay_attrs.addWidget(self.outputs_table)
        self.lay_preflights.addLayout(self.pref_layout)
        self.lay_preflights.addWidget(self.preflights_table)

        self.populate_attrs()
        self.populate_preflights()
        self.inputs_table.itemChanged.connect(self.save_attrs_to_node)
        self.outputs_table.itemChanged.connect(self.save_attrs_to_node)
        self.outputs_table.itemClicked.connect(self.name_changed)
        self.inputs_table.itemClicked.connect(self.name_changed)
        self.add_preflight.clicked.connect(self.create_preflight)

    def create_preflight(self):
        # add a row to the table_widget
        node = self.parent.graph.scene().selectedItems()[0]
        # create this as the first column of that table widget row
        count = self.preflights_table.rowCount()
        self.preflights_table.setRowCount(count+1)
        new_name = QtWidgets.QTableWidgetItem(self.preflight_line_edit.text())
        new_description = QtWidgets.QTableWidgetItem('')
        required = QtWidgets.QTableWidgetItem('False')
        module = QtWidgets.QTableWidgetItem('None')
        self.preflights_table.setItem(count, 0, new_name)
        self.preflights_table.setItem(count, 1, new_description)
        self.preflights_table.setItem(count, 2, required)
        self.preflights_table.setItem(count, 3, module)
        node.create_preflight(self.preflight_line_edit.text(), '', False, None)

    def populate_preflights(self):
        preflights = self.parent.graph.scene().selectedItems()[0].preflight_data
        self.preflights_table.setRowCount(len(preflights))
        for i, preflight in enumerate(preflights):
            name = QtWidgets.QTableWidgetItem(preflights[preflight]['name'])
            description = QtWidgets.QTableWidgetItem(preflights[preflight]['description'])
            module = QtWidgets.QTableWidgetItem(str(preflights[preflight]['module']))
            required = QtWidgets.QTableWidgetItem(str(preflights[preflight]['required']))
            self.preflights_table.setItem(i, 0, name)
            self.preflights_table.setItem(i, 1, description)
            self.preflights_table.setItem(i, 2, required)
            self.preflights_table.setItem(i, 3, module)

    def populate_attrs(self):
        attrsData = self.parent.graph.scene().selectedItems()[0].attrsData
        outputs = 0
        inputs = 0
        ip = -1
        isoc = -1
        for key in attrsData:
            if attrsData[key]['plug']:
                outputs += 1
            if attrsData[key]['socket']:
                inputs += 1
        self.outputs_table.setRowCount(outputs)
        self.inputs_table.setRowCount(inputs)
        print 2222222222222222
        print attrsData
        for attr_name in attrsData:
            name = QtWidgets.QTableWidgetItem(str(attr_name))
            pretty_name = QtWidgets.QTableWidgetItem(str(attrsData[attr_name]['pretty_name']))
            automation_level = QtWidgets.QTableWidgetItem(str(attrsData[attr_name]['automation_level']))
            priority = QtWidgets.QTableWidgetItem(attrsData[attr_name]['priority'])
            methodology = QtWidgets.QTableWidgetItem(attrsData[attr_name]['methodology'])
            duration = QtWidgets.QTableWidgetItem(attrsData[attr_name]['duration'])
            frequency = QtWidgets.QTableWidgetItem(attrsData[attr_name]['frequency'])
            number_effected = QtWidgets.QTableWidgetItem(attrsData[attr_name]['number_effected'])
            if attrsData[attr_name]['plug']:
                ip += 1
                i = ip
                table = self.outputs_table
            elif attrsData[attr_name]['socket']:
                isoc += 1
                i = isoc
                table = self.inputs_table
            table.setItem(i, 0, name)
            table.setItem(i, 1, automation_level)
            table.setItem(i, 2, priority)
            table.setItem(i, 3, methodology)
            table.setItem(i, 4, duration)
            table.setItem(i, 5, frequency)
            table.setItem(i, 6, number_effected)
            table.setItem(i, 7, pretty_name)

    def spawn_properties(self, values, save):
        for attr, val in values.iteritems():
            if attr in ['sockets', 'plugs']:
                pass
            elif attr == 'preflight_data':
                pass
            else:
                newproperty = SettingField(title=attr, value=str(val), save=save)
                self.attrs_dict['Settings'][attr] = newproperty.textbox
                self.lay_settings.addWidget(newproperty)
        self.lay_settings.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum,
                         QtWidgets.QSizePolicy.Expanding))

    def save_attrs_to_node(self, item):
        nodz = self.parent.graph
        node = self.parent.graph.scene().selectedItems()[0]
        plugs = self.parent.graph.scene().selectedItems()[0].attrsData
        name = self.sender().item(item.row(), 0).text()

        if item.column() == 1:
            plugs[name]['automation_level'] = self.sender().item(item.row(), 1).text()
        elif item.column() == 2:
            plugs[name]['priority'] = self.sender().item(item.row(), 2).text()
        elif item.column() == 3:
            plugs[name]['methodology'] = self.sender().item(item.row(), 3).text()
        elif item.column() == 4:
            plugs[name]['duration'] = self.sender().item(item.row(), 4).text()
        elif item.column() == 5:
            plugs[name]['frequency'] = self.sender().item(item.row(), 5).text()
        elif item.column() == 6:
            plugs[name]['number_effected'] = self.sender().item(item.row(), 6).text()
        elif item.column() == 7:
            plugs[name]['pretty_name'] = self.sender().item(item.row(), 7).text()
        elif item.column() == 0:
            index_ = node.attrs.index(self.old_name)
            nodz.editAttribute(node=node, index=index_, newName=name,
                               newIndex=index_)

        self.parent.graph.sc.updateScene()

    def name_changed(self, item):
        self.old_name = self.sender().item(item.row(), 0).text()

    def save_preflight_attrs_to_node(self, item):
        # TODO i need to create some kind of node for storing preflights
        pass

    @staticmethod
    def get_item_text(item):
        try:
            return item.text()
        except AttributeError:
            return ''

    def add_input_connection(self):
        pass
        #self.parent.create_new_attribute()

    def _save_properties(self):
        for i in reversed(range(self.lay_settings.count())):
            widget = self.lay_settings.itemAt(i).widget()
            if hasattr(widget, 'objectname'):
                self.parent.settingWidgets.settings[0][widget.objectname] = widget.value


class SettingField(QtWidgets.QWidget):
    '''
    Contains a label and a text box
    '''
    def __init__(self, title, value='', save=None):
        QtWidgets.QWidget.__init__(self)
        lay = QtWidgets.QHBoxLayout()
        self.setMaximumHeight(42)
        self.setMinimumHeight(22)
        self.objectname = title
        setname = QtWidgets.QLabel('%s: ' % title)
        setname.setFixedWidth(80)
        self.textbox = QtWidgets.QLineEdit(value)
        self.textbox.setFixedWidth(200)
        self.textbox.setFixedHeight(22)
        if save:
            self.textbox.textChanged.connect(save)
        lay.addWidget(setname)
        lay.addWidget(self.textbox)
        lay.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.setLayout(lay)

    @property
    def value(self):
        return self.textbox.text()


class ComboSetting(QtWidgets.QWidget):
    def __init__(self, title, value=None):
        QtWidgets.QWidget.__init__(self)

        lay = QtWidgets.QHBoxLayout()
        self.objectname = title
        setname = QtWidgets.QLabel('%s: ' % title)
        self.combobox = QtWidgets.QComboBox()
        self.combobox.setMinimumWidth(62)
        if isinstance(value, dict):
            for val in value.values():
                self.combobox.addItems(val)
        else:
            for val in value:
                self.combobox.addItems(val)

        lay.addWidget(setname)
        lay.addWidget(self.combobox)
        self.setLayout(lay)

    @property
    def value(self):
        return 'combobox'


