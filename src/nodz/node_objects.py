from Qt import QtGui, QtCore, QtWidgets


class GroupNode(QtWidgets.QGraphicsItem):

    def __init__(self, scene, name):
        """
        :param name: string
        :param nodes: list of node names in the scene
        :param kwargs:
        """
        super(GroupNode, self).__init__()

        self.setZValue(0)
        self.nodes = scene.selectedItems()
        self.scene = scene
        self.name = name
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

    def get_rectangle(self):
        """
        Create a Group node for the selected nodes.
        :param name:
        :param preset:
        :param position:
        :param alternate:
        :param kwargs:
        :return:
        """
        # get the bounding box of the selected items:
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for n in self.nodes:
            if not min_x or n.pos().x() < min_x:
                min_x = n.pos().x()
            if not min_y or n.pos().y() < min_y:
                min_y = n.pos().y()
            if not max_x or n.pos().x() > max_x:
                max_x = n.pos().x()
            if not max_y or n.pos().y() > max_y:
                max_y = n.pos().y()
        center_x = min_x+((max_x-min_x)/2)
        center_y = min_y+((max_y-min_y)/2)
        center_pos = center_x, center_y
        rect = min_x, min_y, max_x, max_y
        return center_pos
        return rect

    def paint(self, painter, option, widget):
        painter.begin(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.green, 8, QtCore.Qt.DashLine))
        cx, cy = self.get_rectangle()
        painter.drawRect(cx, cy, 400, 400)
        # painter.end()