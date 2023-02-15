from PySide6.QtCore import Signal, Qt, QTimer, Slot, QModelIndex    
from PySide6.QtWidgets import QComboBox, QListView
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor, QBrush

class MultiComboBox(QComboBox):
    closedPopup = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))

        first_item = QStandardItem("None")
        first_item.setBackground(QBrush(QColor(200, 200, 200)))
        first_item.setSelectable(False)
        first_item.setCheckable(False)
        self.model().appendRow(first_item)

        self.cancel_close = False

    @Slot(QModelIndex)
    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if not item.isCheckable():
            return
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setCheckState(Qt.CheckState.Checked)
        checked = self.checkedItems()
        if len(checked) > 0:
            string = ", ".join(checked)
        else:
            string = "None"
        first_index = self.model().index(0, 0)
        self.model().itemFromIndex(first_index).setText(string)
        self.cancel_close = True

    def checkedItems(self):
        l = []
        for i in range(self.model().rowCount()):
            it = self.model().item(i)
            if it.checkState() == Qt.CheckState.Checked:
                l.append(it.text())
        return l

    def hidePopup(self):
        if self.cancel_close:
            self.cancel_close = False
            return
        self.closedPopup.emit()
        super().hidePopup()
        QTimer.singleShot(0, lambda: self.setCurrentIndex(0))