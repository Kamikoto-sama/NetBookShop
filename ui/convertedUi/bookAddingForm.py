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
        bookAddingForm.resize(272, 278)
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
        self.pageCountEdit = QtWidgets.QLineEdit(self.groupBox)
        self.pageCountEdit.setClearButtonEnabled(False)
        self.pageCountEdit.setObjectName("pageCountEdit")
        self.verticalLayout_10.addWidget(self.pageCountEdit, 0, QtCore.Qt.AlignLeft)
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
        self.countEdit = QtWidgets.QLineEdit(self.groupBox)
        self.countEdit.setObjectName("countEdit")
        self.verticalLayout_10.addWidget(self.countEdit, 0, QtCore.Qt.AlignLeft)
        self.priceEdit = QtWidgets.QLineEdit(self.groupBox)
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
        self.pageCountEdit.setPlaceholderText(_translate("bookAddingForm", "Page count"))
        self.label.setText(_translate("bookAddingForm", "Author name"))
        self.label_2.setText(_translate("bookAddingForm", "Publisher"))
        self.countEdit.setPlaceholderText(_translate("bookAddingForm", "Count"))
        self.priceEdit.setPlaceholderText(_translate("bookAddingForm", "Price"))
        self.addBtn.setText(_translate("bookAddingForm", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    bookAddingForm = QtWidgets.QWidget()
    ui = Ui_bookAddingForm()
    ui.setupUi(bookAddingForm)
    bookAddingForm.show()
    sys.exit(app.exec_())
