# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/publisherAddingForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_publisherAddingForm(object):
    def setupUi(self, publisherAddingForm):
        publisherAddingForm.setObjectName("publisherAddingForm")
        publisherAddingForm.resize(205, 112)
        self.verticalLayout = QtWidgets.QVBoxLayout(publisherAddingForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.nameEdit = QtWidgets.QLineEdit(publisherAddingForm)
        self.nameEdit.setObjectName("nameEdit")
        self.verticalLayout.addWidget(self.nameEdit)
        self.label = QtWidgets.QLabel(publisherAddingForm)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.dateEdit = QtWidgets.QDateEdit(publisherAddingForm)
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout.addWidget(self.dateEdit, 0, QtCore.Qt.AlignLeft)
        self.addBtn = QtWidgets.QPushButton(publisherAddingForm)
        self.addBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addBtn.setObjectName("addBtn")
        self.verticalLayout.addWidget(self.addBtn)

        self.retranslateUi(publisherAddingForm)
        self.nameEdit.returnPressed.connect(self.addBtn.click)
        QtCore.QMetaObject.connectSlotsByName(publisherAddingForm)

    def retranslateUi(self, publisherAddingForm):
        _translate = QtCore.QCoreApplication.translate
        publisherAddingForm.setWindowTitle(_translate("publisherAddingForm", "Add publisher"))
        self.nameEdit.setPlaceholderText(_translate("publisherAddingForm", "Publisher name"))
        self.label.setText(_translate("publisherAddingForm", "Creation date"))
        self.addBtn.setText(_translate("publisherAddingForm", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    publisherAddingForm = QtWidgets.QWidget()
    ui = Ui_publisherAddingForm()
    ui.setupUi(publisherAddingForm)
    publisherAddingForm.show()
    sys.exit(app.exec_())
