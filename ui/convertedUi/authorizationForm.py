# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/authorizationForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AuthorizationForm(object):
    def setupUi(self, AuthorizationForm):
        AuthorizationForm.setObjectName("AuthorizationForm")
        AuthorizationForm.setEnabled(False)
        AuthorizationForm.resize(191, 144)
        self.verticalLayout = QtWidgets.QVBoxLayout(AuthorizationForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.loginEdit = QtWidgets.QLineEdit(AuthorizationForm)
        self.loginEdit.setText("")
        self.loginEdit.setObjectName("loginEdit")
        self.verticalLayout.addWidget(self.loginEdit)
        self.passwordEdit = QtWidgets.QLineEdit(AuthorizationForm)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.verticalLayout.addWidget(self.passwordEdit)
        self.haveAccessCode = QtWidgets.QCheckBox(AuthorizationForm)
        self.haveAccessCode.setObjectName("haveAccessCode")
        self.verticalLayout.addWidget(self.haveAccessCode)
        self.accessCodeEdit = QtWidgets.QLineEdit(AuthorizationForm)
        self.accessCodeEdit.setObjectName("accessCodeEdit")
        self.verticalLayout.addWidget(self.accessCodeEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.signInBtn = QtWidgets.QPushButton(AuthorizationForm)
        self.signInBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.signInBtn.setObjectName("signInBtn")
        self.horizontalLayout.addWidget(self.signInBtn)
        self.signUpBtn = QtWidgets.QPushButton(AuthorizationForm)
        self.signUpBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.signUpBtn.setObjectName("signUpBtn")
        self.horizontalLayout.addWidget(self.signUpBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AuthorizationForm)
        QtCore.QMetaObject.connectSlotsByName(AuthorizationForm)

    def retranslateUi(self, AuthorizationForm):
        _translate = QtCore.QCoreApplication.translate
        AuthorizationForm.setWindowTitle(_translate("AuthorizationForm", "AuthorizationForm"))
        self.loginEdit.setPlaceholderText(_translate("AuthorizationForm", "Login"))
        self.passwordEdit.setPlaceholderText(_translate("AuthorizationForm", "Password"))
        self.haveAccessCode.setText(_translate("AuthorizationForm", "I have an access code"))
        self.accessCodeEdit.setPlaceholderText(_translate("AuthorizationForm", "Your access code"))
        self.signInBtn.setText(_translate("AuthorizationForm", "Sign in"))
        self.signUpBtn.setText(_translate("AuthorizationForm", "Sign up"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AuthorizationForm = QtWidgets.QWidget()
    ui = Ui_AuthorizationForm()
    ui.setupUi(AuthorizationForm)
    AuthorizationForm.show()
    sys.exit(app.exec_())
