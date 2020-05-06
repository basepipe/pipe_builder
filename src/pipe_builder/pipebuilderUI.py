import os
from Qt import QtWidgets, QtCore
import src.nodz.nodz_main as nodz
from settingsUI import NodeSettingWidget
from toolbarUI import Toolbar

######################################################################
# Test signals
######################################################################


def openStylesheet():
    filepath = '%s/stylesheet.css' % os.path.dirname(__file__)
    with open(filepath, 'r') as myfile:
        fileString = myfile.read()
        # remove comments
        # cleanString = re.sub('//.*?\n|/\*.*?\*/', '', fileString, re.S)
        return fileString


STYLESHEET = openStylesheet()


class PipeBuilder(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.title = 'New Data Mapping Session - Not Saved'
        self.setWindowTitle(self.title)
        self.graph = nodz.Nodz(None)
        self.graph.filepath = None
        # nodz.loadConfig(filePath='')

        self.graph.initialize()
        self.settingWidgets = NodeSettingWidget(parent=self)
        self.initialize_connections()
        self.graph.show()
        self.setStyleSheet(STYLESHEET)

        ###### LAYOUT ##########
        self.scroll = QtWidgets.QScrollArea()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.scroll.setSizePolicy(sizePolicy)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumWidth(330)
        # scroll.setFixedWidth(450)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.scroll.setWidget(self.settingWidgets)
        self.toolbar = Toolbar(parent=self)
        # v_lay = QtWidgets.QVBoxLayout()
        lay = QtWidgets.QVBoxLayout()
        lay.setSpacing(1)
        # lay.setMargin(5)

        lay.addWidget(self.toolbar)
        self.splitter.addWidget(self.graph)
        self.splitter.addWidget(self.scroll)
        lay.addWidget(self.splitter)
        self.setLayout(lay)
        self.scroll.hide()

        self.settingWidgets.signal_nothing_selected.connect(self.on_select_nothing)
        self.settingWidgets.signal_something_selected.connect(self.on_select_item)
        self.toolbar.filename_changed.connect(self.on_filename_changed)

    def on_filename_changed(self, data):
        self.title = data
        self.graph.filepath = data
        self.setWindowTitle(data)

    def on_select_nothing(self):
        self.scroll.hide()

    def on_select_item(self):
        self.scroll.show()

    @staticmethod
    def fix_name(name_):
        # replace spaces with _
        fixed_name = name_.replace(' ', '_').replace('.', '_').lower()
        return fixed_name

    # Nodes
    @QtCore.Slot(str)
    @staticmethod
    def on_nodeCreated(nodeName):
        #print 'node created : ', nodeName
        pass

    @QtCore.Slot(str)
    @staticmethod
    def on_nodeDeleted(nodeName):
        print 'node deleted : ', nodeName
        pass

    @QtCore.Slot(str, str)
    def on_nodeEdited(self, nodeName, newName):
        line_edit = self.settingWidgets.node_settings_box.attrs_dict['Settings']['name']
        fixed_name = self.fix_name(newName)
        line_edit.setText(fixed_name)
        # line_edit.setCursorPosition(100)
        print 'node edited : {0}, new name : {1}'.format(nodeName, fixed_name)

    @QtCore.Slot(str)
    def on_nodeSelected(self, nodesName):
        print 'node selected : ', nodesName
        self.settingWidgets.refresh(settingData=self.query_selected_node_info())

    @QtCore.Slot(str, object)
    @staticmethod
    def on_nodeMoved(nodeName, nodePos):
        print 'node {0} moved to {1}'.format(nodeName, nodePos)

    @QtCore.Slot(str)
    @staticmethod
    def on_nodeDoubleClick(nodeName):
        print 'double click on node : {0}'.format(nodeName)

    # Attrs
    @QtCore.Slot(str, int)
    def on_attrCreated(self, nodeName, attrId):
        # print 'attr created : {0} at index : {1}'.format(nodeName, attrId)
        self.on_nodeSelected(nodeName)

    @QtCore.Slot(str, int)
    @staticmethod
    def on_attrDeleted(nodeName, attrId):
        print 'attr Deleted : {0} at old index : {1}'.format(nodeName, attrId)

    @QtCore.Slot(str, int, int)
    @staticmethod
    def on_attrEdited(nodeName, oldId, newId):
        print 'attr Edited : {0} at old index : {1}, new index : {2}'.format(nodeName, oldId, newId)

    # Connections
    @QtCore.Slot(str, str, str, str)
    @staticmethod
    def on_connected(srcNodeName, srcPlugName, destNodeName, dstSocketName):
        #print 'connected src: "{0}" at "{1}" to dst: "{2}" at "{3}"'.format(srcNodeName, srcPlugName, destNodeName,
        #                                                                    dstSocketName)
        pass

    @QtCore.Slot(str, str, str, str)
    def on_disconnected(srcNodeName, srcPlugName, destNodeName, dstSocketName):
        print 'disconnected src: "{0}" at "{1}" from dst: "{2}" at "{3}"'.format(srcNodeName, srcPlugName,
                                                                                 destNodeName, dstSocketName)

    # Graph
    @QtCore.Slot()
    def on_graphSaved(self, data):
        self.on_filename_changed(data)
        # we don't save the .jpg here because it requires restart at this time.
        print 'graph saved: %s' % data

    @QtCore.Slot()
    def on_graphLoaded(self, data):
        print 'graph %s loaded !' % data

    @QtCore.Slot()
    @staticmethod
    def on_graphCleared():
        print 'graph cleared !'

    @QtCore.Slot()
    @staticmethod
    def on_graphEvaluated():
        print 'graph evaluated !'

    # Other
    @QtCore.Slot(object)
    def on_keyPressed(self, key):
        if key == QtCore.Qt.Key_Space:
            self.graph.block_disconnect = True
        else:
            self.graph.block_disconnect = False

    @QtCore.Slot(dict)
    def on_saveSettings(self, settings):
        settings = settings[0]
        query_attributes = ['description', 'pipeID', 'software']
        saved_attributes = {}
        for attr in query_attributes:
            saved_attributes[attr] = settings[attr]

        for item in self.graph.scene().selectedItems():
            self.graph.editNode(node=item, newName=settings['name'], **saved_attributes)
        print 'saving settings!'

        # nodeA = self.graph.createNode(name='nodeA', preset='node_preset_1', position=None)
    def initialize_connections(self):
        self.graph.signal_NodeCreated.connect(self.on_nodeCreated)
        self.graph.signal_NodeDeleted.connect(self.on_nodeDeleted)
        self.graph.signal_NodeEdited.connect(self.on_nodeEdited)
        self.graph.signal_NodeSelected.connect(self.on_nodeSelected)
        self.graph.signal_NodeMoved.connect(self.on_nodeMoved)
        # self.graph.signal_NodeDoubleClicked.connect(on_nodeDoubleClick)

        self.graph.signal_AttrCreated.connect(self.on_attrCreated)
        self.graph.signal_AttrDeleted.connect(self.on_attrDeleted)
        self.graph.signal_AttrEdited.connect(self.on_attrEdited)

        self.graph.signal_PlugConnected.connect(self.on_connected)
        self.graph.signal_SocketConnected.connect(self.on_connected)
        self.graph.signal_PlugDisconnected.connect(self.on_disconnected)
        self.graph.signal_SocketDisconnected.connect(self.on_disconnected)

        self.graph.signal_GraphSaved.connect(self.on_graphSaved)
        self.graph.signal_GraphLoaded.connect(self.on_graphLoaded)
        self.graph.signal_GraphCleared.connect(self.on_graphCleared)
        self.graph.signal_GraphEvaluated.connect(self.on_graphEvaluated)

        self.graph.signal_KeyPressed.connect(self.on_keyPressed)
        self.settingWidgets.signal_SaveSettings.connect(self.on_saveSettings)

    def query_selected_node_info(self):
        '''
        structures the node information from Nodz in an easy to access format
        :return:
        '''
        query_attributes = ['name', 'description', 'pipeID', 'software', 'preflight_data']
        all_info = []
        if self.graph.scene().selectedItems():
            item = self.graph.scene().selectedItems()[0]
            if isinstance(item, nodz.NodeItem):
                print 'made it'
                node_settings = {}
                for setting in query_attributes:
                    val = getattr(item, setting)
                    node_settings[setting] = val

                # add socket-plug data
                sockets = {}
                plugs = {}
                for socket in item.sockets.itervalues():
                    sockets[socket.index] = socket.attribute
                for plug in item.plugs.itervalues():
                    plugs[plug.index] = plug.attribute
                node_settings['sockets'] = sockets
                node_settings['plugs'] = plugs

                all_info.append(node_settings)
                return all_info
            elif isinstance(item, nodz.GroupItem):
                print item, 'is a group item'
            else:
                print 'instance is: %s' % type(item)



    def closeEvent(self, event):
        if self.graph.filepath:
            print 'Saving Graph to: %s' % self.graph.filepath
            self.graph.saveGraph(filePath=self.graph.filepath)
            print 'Saving Graph Image to: %s' % self.graph.filepath.replace('json', 'jpg')
            self.graph.exportImage(filePath=self.graph.filepath.replace('json', 'jpg'))
        else:
            print 'No Filepath set, skipping save'


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    pb = PipeBuilder()
    # nodz.loadConfig(filePath='')
    pb.show()
    pb.raise_()
    app.exec_()
