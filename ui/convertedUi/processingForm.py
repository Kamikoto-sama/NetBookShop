# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/processingForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_processingForm(object):
    def setupUi(self, processingForm):
        processingForm.setObjectName("processingForm")
        processingForm.resize(454, 48)
        processingForm.setAutoFillBackground(False)
        processingForm.setStyleSheet("background-color: rgb(231, 231, 231);")
        self.verticalLayout = QtWidgets.QVBoxLayout(processingForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.message = QtWidgets.QLabel(processingForm)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.message.setFont(font)
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setObjectName("message")
        self.verticalLayout.addWidget(self.message)
        self.statusBar = QtWidgets.QProgressBar(processingForm)
        self.statusBar.setMinimumSize(QtCore.QSize(0, 30))
        self.statusBar.setProperty("value", 24)
        self.statusBar.setAlignment(QtCore.Qt.AlignCenter)
        self.statusBar.setTextVisible(True)
        self.statusBar.setInvertedAppearance(False)
        self.statusBar.setObjectName("statusBar")
        self.verticalLayout.addWidget(self.statusBar)

        self.retranslateUi(processingForm)
        QtCore.QMetaObject.connectSlotsByName(processingForm)

    def retranslateUi(self, processingForm):
        _translate = QtCore.QCoreApplication.translate
        processingForm.setWindowTitle(_translate("processingForm", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    processingForm = QtWidgets.QWidget()
    ui = Ui_processingForm()
    ui.setupUi(processingForm)
    processingForm.show()
    sys.exit(app.exec_())
