# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/bookAddingForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_bookAddingForm(object):
    def setupUi(self, bookAddingForm):
        bookAddingForm.setObjectName("bookAddingForm")
        bookAddingForm.resize(272, 335)
        self.verticalLayout = QtWidgets.QVBoxLayout(bookAddingForm)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(bookAddingForm)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.nameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.nameEdit.setObjectName("nameEdit")
        self.verticalLayout_10.addWidget(self.nameEdit)
        self.genreEdit = QtWidgets.QLineEdit(self.groupBox)
        self.genreEdit.setObjectName("genreEdit")
        self.verticalLayout_10.addWidget(self.genreEdit)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_10.addWidget(self.label_3)
        self.pageCountEdit = QtWidgets.QSpinBox(self.groupBox)
        self.pageCountEdit.setSuffix("")
        self.pageCountEdit.setMinimum(1)
        self.pageCountEdit.setMaximum(999999999)
        self.pageCountEdit.setProperty("value", 1)
        self.pageCountEdit.setDisplayIntegerBase(10)
        self.pageCountEdit.setObjectName("pageCountEdit")
        self.verticalLayout_10.addWidget(self.pageCountEdit, 0, QtCore.Qt.AlignLeft)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout_10.addWidget(self.label)
        self.authorsList = QtWidgets.QComboBox(self.groupBox)
        self.authorsList.setEditable(True)
        self.authorsList.setObjectName("authorsList")
        self.verticalLayout_10.addWidget(self.authorsList)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_10.addWidget(self.label_2)
        self.publishersList = QtWidgets.QComboBox(self.groupBox)
        self.publishersList.setEditable(True)
        self.publishersList.setObjectName("publishersList")
        self.verticalLayout_10.addWidget(self.publishersList)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.countEdit = QtWidgets.QSpinBox(self.groupBox)
        self.countEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.countEdit.setMaximum(999999999)
        self.countEdit.setObjectName("countEdit")
        self.verticalLayout_10.addWidget(self.countEdit, 0, QtCore.Qt.AlignLeft)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_10.addWidget(self.label_5)
        self.priceEdit = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.priceEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.priceEdit.setDecimals(2)
        self.priceEdit.setMinimum(1.0)
        self.priceEdit.setMaximum(999999.0)
        self.priceEdit.setObjectName("priceEdit")
        self.verticalLayout_10.addWidget(self.priceEdit, 0, QtCore.Qt.AlignLeft)
        self.addBtn = QtWidgets.QPushButton(self.groupBox)
        self.addBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addBtn.setObjectName("addBtn")
        self.verticalLayout_10.addWidget(self.addBtn)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(bookAddingForm)
        QtCore.QMetaObject.connectSlotsByName(bookAddingForm)

    def retranslateUi(self, bookAddingForm):
        _translate = QtCore.QCoreApplication.translate
        bookAddingForm.setWindowTitle(_translate("bookAddingForm", "Add book"))
        self.groupBox.setTitle(_translate("bookAddingForm", "Book"))
        self.nameEdit.setPlaceholderText(_translate("bookAddingForm", "Name"))
        self.genreEdit.setPlaceholderText(_translate("bookAddingForm", "Genre"))
        self.label_3.setText(_translate("bookAddingForm", "Page count"))
        self.label.setText(_translate("bookAddingForm", "Author name"))
        self.label_2.setText(_translate("bookAddingForm", "Publisher"))
        self.label_4.setText(_translate("bookAddingForm", "Count"))
        self.label_5.setText(_translate("bookAddingForm", "Price"))
        self.priceEdit.setSuffix(_translate("bookAddingForm", "$"))
        self.addBtn.setText(_translate("bookAddingForm", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    bookAddingForm = QtWidgets.QWidget()
    ui = Ui_bookAddingForm()
    ui.setupUi(bookAddingForm)
    bookAddingForm.show()
    sys.exit(app.exec_())
