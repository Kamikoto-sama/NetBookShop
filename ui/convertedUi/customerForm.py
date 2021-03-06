# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/customerForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_customerForm(object):
    def setupUi(self, customerForm):
        customerForm.setObjectName("customerForm")
        customerForm.resize(940, 568)
        self.horizontalLayout = QtWidgets.QHBoxLayout(customerForm)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabs = QtWidgets.QTabWidget(customerForm)
        self.tabs.setElideMode(QtCore.Qt.ElideMiddle)
        self.tabs.setObjectName("tabs")
        self.booksTab = QtWidgets.QWidget()
        self.booksTab.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.booksTab.setObjectName("booksTab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.booksTab)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.booksTable = QtWidgets.QTableWidget(self.booksTab)
        self.booksTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.booksTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.booksTable.setTabKeyNavigation(False)
        self.booksTable.setProperty("showDropIndicator", False)
        self.booksTable.setDragDropOverwriteMode(False)
        self.booksTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.booksTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.booksTable.setShowGrid(False)
        self.booksTable.setCornerButtonEnabled(False)
        self.booksTable.setObjectName("booksTable")
        self.booksTable.setColumnCount(7)
        self.booksTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.booksTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.booksTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.booksTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.booksTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.booksTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.booksTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.booksTable.setHorizontalHeaderItem(6, item)
        self.booksTable.horizontalHeader().setCascadingSectionResizes(False)
        self.booksTable.horizontalHeader().setStretchLastSection(True)
        self.booksTable.verticalHeader().setCascadingSectionResizes(False)
        self.horizontalLayout_2.addWidget(self.booksTable)
        self.widget = QtWidgets.QWidget(self.booksTab)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.orderBtn = QtWidgets.QPushButton(self.widget_2)
        self.orderBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.orderBtn.setObjectName("orderBtn")
        self.verticalLayout.addWidget(self.orderBtn)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox = QtWidgets.QGroupBox(self.widget_4)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.nameFilterEdit = QtWidgets.QLineEdit(self.groupBox)
        self.nameFilterEdit.setClearButtonEnabled(False)
        self.nameFilterEdit.setObjectName("nameFilterEdit")
        self.verticalLayout_10.addWidget(self.nameFilterEdit, 0, QtCore.Qt.AlignHCenter)
        self.genreFilterEdit = QtWidgets.QLineEdit(self.groupBox)
        self.genreFilterEdit.setObjectName("genreFilterEdit")
        self.verticalLayout_10.addWidget(self.genreFilterEdit, 0, QtCore.Qt.AlignHCenter)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout_10.addWidget(self.label)
        self.authorsList = QtWidgets.QComboBox(self.groupBox)
        self.authorsList.setEditable(True)
        self.authorsList.setObjectName("authorsList")
        self.authorsList.addItem("")
        self.authorsList.setItemText(0, "")
        self.verticalLayout_10.addWidget(self.authorsList)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_10.addWidget(self.label_2)
        self.publishersList = QtWidgets.QComboBox(self.groupBox)
        self.publishersList.setEditable(True)
        self.publishersList.setObjectName("publishersList")
        self.publishersList.addItem("")
        self.publishersList.setItemText(0, "")
        self.verticalLayout_10.addWidget(self.publishersList)
        self.searchBtn = QtWidgets.QPushButton(self.groupBox)
        self.searchBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchBtn.setObjectName("searchBtn")
        self.verticalLayout_10.addWidget(self.searchBtn)
        self.resetBtn = QtWidgets.QPushButton(self.groupBox)
        self.resetBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.resetBtn.setObjectName("resetBtn")
        self.verticalLayout_10.addWidget(self.resetBtn)
        self.verticalLayout_9.addWidget(self.groupBox)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.booksUpdateBtn = QtWidgets.QPushButton(self.widget_3)
        self.booksUpdateBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.booksUpdateBtn.setObjectName("booksUpdateBtn")
        self.verticalLayout_3.addWidget(self.booksUpdateBtn)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.horizontalLayout_2.addWidget(self.widget)
        self.tabs.addTab(self.booksTab, "")
        self.ordersTab = QtWidgets.QWidget()
        self.ordersTab.setObjectName("ordersTab")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.ordersTab)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ordersTable = QtWidgets.QTableWidget(self.ordersTab)
        self.ordersTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.ordersTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ordersTable.setTabKeyNavigation(False)
        self.ordersTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ordersTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ordersTable.setShowGrid(False)
        self.ordersTable.setObjectName("ordersTable")
        self.ordersTable.setColumnCount(2)
        self.ordersTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ordersTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ordersTable.setHorizontalHeaderItem(1, item)
        self.ordersTable.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout_5.addWidget(self.ordersTable)
        self.widget_16 = QtWidgets.QWidget(self.ordersTab)
        self.widget_16.setObjectName("widget_16")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_16)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_17 = QtWidgets.QWidget(self.widget_16)
        self.widget_17.setObjectName("widget_17")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_17)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.cancelOrderBtn = QtWidgets.QPushButton(self.widget_17)
        self.cancelOrderBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelOrderBtn.setObjectName("cancelOrderBtn")
        self.verticalLayout_8.addWidget(self.cancelOrderBtn)
        self.verticalLayout_7.addWidget(self.widget_17)
        self.widget_18 = QtWidgets.QWidget(self.widget_16)
        self.widget_18.setObjectName("widget_18")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_18)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ordersUpdateBtn = QtWidgets.QPushButton(self.widget_18)
        self.ordersUpdateBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ordersUpdateBtn.setObjectName("ordersUpdateBtn")
        self.verticalLayout_4.addWidget(self.ordersUpdateBtn)
        self.verticalLayout_7.addWidget(self.widget_18)
        self.widget_19 = QtWidgets.QWidget(self.widget_16)
        self.widget_19.setObjectName("widget_19")
        self.verticalLayout_7.addWidget(self.widget_19)
        self.horizontalLayout_5.addWidget(self.widget_16)
        self.tabs.addTab(self.ordersTab, "")
        self.horizontalLayout.addWidget(self.tabs)

        self.retranslateUi(customerForm)
        self.tabs.setCurrentIndex(0)
        self.authorsList.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(customerForm)

    def retranslateUi(self, customerForm):
        _translate = QtCore.QCoreApplication.translate
        customerForm.setWindowTitle(_translate("customerForm", "Library: Customer"))
        item = self.booksTable.horizontalHeaderItem(0)
        item.setText(_translate("customerForm", "Name"))
        item = self.booksTable.horizontalHeaderItem(1)
        item.setText(_translate("customerForm", "Genres"))
        item = self.booksTable.horizontalHeaderItem(2)
        item.setText(_translate("customerForm", "Page count"))
        item = self.booksTable.horizontalHeaderItem(3)
        item.setText(_translate("customerForm", "Author"))
        item = self.booksTable.horizontalHeaderItem(4)
        item.setText(_translate("customerForm", "Publisher"))
        item = self.booksTable.horizontalHeaderItem(5)
        item.setText(_translate("customerForm", "Count"))
        item = self.booksTable.horizontalHeaderItem(6)
        item.setText(_translate("customerForm", "Price"))
        self.orderBtn.setText(_translate("customerForm", "Order"))
        self.groupBox.setTitle(_translate("customerForm", "Filters"))
        self.nameFilterEdit.setPlaceholderText(_translate("customerForm", "Book name"))
        self.genreFilterEdit.setPlaceholderText(_translate("customerForm", "Genre"))
        self.label.setText(_translate("customerForm", "Author name"))
        self.label_2.setText(_translate("customerForm", "Publisher"))
        self.searchBtn.setText(_translate("customerForm", "Search"))
        self.resetBtn.setText(_translate("customerForm", "Reset"))
        self.booksUpdateBtn.setText(_translate("customerForm", "Update"))
        self.tabs.setTabText(self.tabs.indexOf(self.booksTab), _translate("customerForm", "Books"))
        item = self.ordersTable.horizontalHeaderItem(0)
        item.setText(_translate("customerForm", "Book name"))
        item = self.ordersTable.horizontalHeaderItem(1)
        item.setText(_translate("customerForm", "Order date"))
        self.cancelOrderBtn.setText(_translate("customerForm", "Cancel"))
        self.ordersUpdateBtn.setText(_translate("customerForm", "Update"))
        self.tabs.setTabText(self.tabs.indexOf(self.ordersTab), _translate("customerForm", "My orders"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    customerForm = QtWidgets.QWidget()
    ui = Ui_customerForm()
    ui.setupUi(customerForm)
    customerForm.show()
    sys.exit(app.exec_())
