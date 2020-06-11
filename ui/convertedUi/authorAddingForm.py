# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/authorAddingForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_authorAddingForm(object):
    def setupUi(self, authorAddingForm):
        authorAddingForm.setObjectName("authorAddingForm")
        authorAddingForm.resize(273, 172)
        self.verticalLayout = QtWidgets.QVBoxLayout(authorAddingForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.nameEdit = QtWidgets.QLineEdit(authorAddingForm)
        self.nameEdit.setObjectName("nameEdit")
        self.verticalLayout.addWidget(self.nameEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dateEdit = QtWidgets.QDateEdit(authorAddingForm)
        self.dateEdit.setObjectName("dateEdit")
        self.horizontalLayout.addWidget(self.dateEdit)
        self.label = QtWidgets.QLabel(authorAddingForm)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.bioEdit = QtWidgets.QTextEdit(authorAddingForm)
        self.bioEdit.setObjectName("bioEdit")
        self.verticalLayout.addWidget(self.bioEdit)
        self.addBtn = QtWidgets.QPushButton(authorAddingForm)
        self.addBtn.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.addBtn.setObjectName("addBtn")
        self.verticalLayout.addWidget(self.addBtn)

        self.retranslateUi(authorAddingForm)
        self.nameEdit.returnPressed.connect(self.addBtn.click)
        QtCore.QMetaObject.connectSlotsByName(authorAddingForm)

    def retranslateUi(self, authorAddingForm):
        _translate = QtCore.QCoreApplication.translate
        authorAddingForm.setWindowTitle(_translate("authorAddingForm", "Add author"))
        self.nameEdit.setPlaceholderText(_translate("authorAddingForm", "Author name"))
        self.label.setText(_translate("authorAddingForm", "Birth date"))
        self.bioEdit.setPlaceholderText(_translate("authorAddingForm", "Biography"))
        self.addBtn.setText(_translate("authorAddingForm", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    authorAddingForm = QtWidgets.QWidget()
    ui = Ui_authorAddingForm()
    ui.setupUi(authorAddingForm)
    authorAddingForm.show()
    sys.exit(app.exec_())
