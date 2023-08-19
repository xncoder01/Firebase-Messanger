# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\profile.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Profile(object):
    def setupUi(self, Profile):
        Profile.setObjectName("Profile")
        Profile.resize(602, 712)
        Profile.setStyleSheet("QDialog{\n"
"    background-color: rgb(13, 27, 67);\n"
"    border: 1px solid rgb(2, 130, 202);\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Profile)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_3 = QtWidgets.QFrame(Profile)
        self.frame_3.setMinimumSize(QtCore.QSize(50, 40))
        self.frame_3.setMaximumSize(QtCore.QSize(50, 40))
        self.frame_3.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout.addWidget(self.frame_3, 2, 2, 1, 1)
        self.frame_2 = QtWidgets.QFrame(Profile)
        self.frame_2.setStyleSheet("QFrame{\n"
"    color: rgb(2, 125, 202);\n"
"    border:none;\n"
"}\n"
"QLineEdit{\n"
"    border: 1px solid rgb(2, 125, 202);\n"
"    border-radius: 5px;\n"
"    background-color:rgba(0, 0, 0, 0);\n"
"}\n"
"QLabel{\n"
"    background-color: rgb(13, 27, 67);\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame_14 = QtWidgets.QFrame(self.frame_4)
        self.frame_14.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_14)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_14)
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(29)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout_7.addWidget(self.frame_14)
        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_5)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.frame_5)
        self.frame_7.setMinimumSize(QtCore.QSize(500, 0))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_9 = QtWidgets.QFrame(self.frame_7)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3.addWidget(self.frame_9)
        self.frame_10 = QtWidgets.QFrame(self.frame_7)
        self.frame_10.setMinimumSize(QtCore.QSize(450, 580))
        self.frame_10.setStyleSheet("QLineEdit{\n"
"    padding: 0 5px 0 5px ;\n"
"}")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.label_2 = QtWidgets.QLabel(self.frame_10)
        self.label_2.setGeometry(QtCore.QRect(40, 190, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_10)
        self.lineEdit.setGeometry(QtCore.QRect(20, 202, 201, 46))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.frame_10)
        self.label_3.setGeometry(QtCore.QRect(280, 190, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_10)
        self.lineEdit_2.setGeometry(QtCore.QRect(260, 202, 201, 46))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.frame_10)
        self.label_4.setGeometry(QtCore.QRect(40, 270, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_10)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 282, 441, 46))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame_10)
        self.lineEdit_4.setGeometry(QtCore.QRect(20, 362, 441, 46))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit_4.setText("")
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(self.frame_10)
        self.label_5.setGeometry(QtCore.QRect(40, 350, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame_10)
        self.lineEdit_5.setGeometry(QtCore.QRect(20, 440, 301, 46))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit_5.setText("")
        self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_6 = QtWidgets.QLabel(self.frame_10)
        self.label_6.setGeometry(QtCore.QRect(40, 428, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(self.frame_10)
        self.pushButton.setGeometry(QtCore.QRect(165, 530, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
"    color: rgb(42, 42, 42);\n"
"    border-radius: 5px;\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_10)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 450, 111, 35))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
"    color: rgb(42, 42, 42);\n"
"    border-radius: 5px;\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.frame_10)
        self.pushButton_6.setGeometry(QtCore.QRect(165, 530, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
"    color: rgb(42, 42, 42);\n"
"    border-radius: 5px;\n"
"}")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.frame_10)
        self.pushButton_7.setGeometry(QtCore.QRect(165, 530, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
"    color: rgb(42, 42, 42);\n"
"    border-radius: 5px;\n"
"}")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.frame_10)
        self.pushButton_8.setGeometry(QtCore.QRect(340, 530, 111, 0))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
"    color: rgb(42, 42, 42);\n"
"    border-radius: 5px;\n"
"}")
        self.pushButton_8.setObjectName("pushButton_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.frame_10)
        self.lineEdit_9.setGeometry(QtCore.QRect(20, 520, 301, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit_9.setText("")
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_8 = QtWidgets.QLabel(self.frame_10)
        self.label_8.setGeometry(QtCore.QRect(40, 508, 41, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.frame_10)
        self.label_9.setGeometry(QtCore.QRect(330, 530, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setText("")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_12 = QtWidgets.QLabel(self.frame_10)
        self.label_12.setGeometry(QtCore.QRect(160, 30, 171, 141))
        self.label_12.setStyleSheet("border:none;\n"
"border-radius: 70px;")
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap(".\\../../../Res/Images/temp.png"))
        self.label_12.setScaledContents(True)
        self.label_12.setObjectName("label_12")
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.label_3.raise_()
        self.lineEdit_3.raise_()
        self.label_4.raise_()
        self.lineEdit_4.raise_()
        self.label_5.raise_()
        self.lineEdit_5.raise_()
        self.label_6.raise_()
        self.pushButton_2.raise_()
        self.label_2.raise_()
        self.pushButton_7.raise_()
        self.pushButton_6.raise_()
        self.pushButton.raise_()
        self.lineEdit_9.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.pushButton_8.raise_()
        self.label_12.raise_()
        self.verticalLayout_3.addWidget(self.frame_10)
        self.frame_11 = QtWidgets.QFrame(self.frame_7)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_3.addWidget(self.frame_11)
        self.horizontalLayout_2.addWidget(self.frame_7)
        self.frame_8 = QtWidgets.QFrame(self.frame_5)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_2.addWidget(self.frame_8)
        self.verticalLayout_7.addWidget(self.frame_5)
        self.horizontalLayout_5.addWidget(self.frame_4)
        self.frame_15 = QtWidgets.QFrame(self.frame_2)
        self.frame_15.setMaximumSize(QtCore.QSize(0, 16777215))
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_15)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_16 = QtWidgets.QFrame(self.frame_15)
        self.frame_16.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_16)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.frame_16)
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_8.addWidget(self.label_7)
        self.verticalLayout.addWidget(self.frame_16)
        self.frame_17 = QtWidgets.QFrame(self.frame_15)
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_18 = QtWidgets.QFrame(self.frame_17)
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_18)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_6.addWidget(self.frame_18)
        self.frame_19 = QtWidgets.QFrame(self.frame_17)
        self.frame_19.setMinimumSize(QtCore.QSize(500, 0))
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_19)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.frame_21 = QtWidgets.QFrame(self.frame_19)
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_21)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_9.addWidget(self.frame_21)
        self.frame_22 = QtWidgets.QFrame(self.frame_19)
        self.frame_22.setMinimumSize(QtCore.QSize(0, 400))
        self.frame_22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame_22)
        self.lineEdit_6.setGeometry(QtCore.QRect(50, 50, 391, 46))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit_6.setText("")
        self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_6.setReadOnly(False)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.frame_22)
        self.lineEdit_7.setGeometry(QtCore.QRect(50, 140, 391, 46))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit_7.setText("")
        self.lineEdit_7.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_7.setReadOnly(False)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.frame_22)
        self.lineEdit_8.setGeometry(QtCore.QRect(50, 230, 391, 46))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit_8.setText("")
        self.lineEdit_8.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_8.setReadOnly(False)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_22)
        self.pushButton_4.setGeometry(QtCore.QRect(270, 320, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
"    color: rgb(42, 42, 42);\n"
"    border-radius: 5px;\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_22)
        self.pushButton_5.setGeometry(QtCore.QRect(100, 320, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
"    color: rgb(42, 42, 42);\n"
"    border-radius: 5px;\n"
"}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_9 = QtWidgets.QPushButton(self.frame_22)
        self.pushButton_9.setGeometry(QtCore.QRect(270, 320, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
"    color: rgb(42, 42, 42);\n"
"    border-radius: 5px;\n"
"}")
        self.pushButton_9.setObjectName("pushButton_9")
        self.label_10 = QtWidgets.QLabel(self.frame_22)
        self.label_10.setGeometry(QtCore.QRect(70, 303, 41, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.frame_22)
        self.label_11.setGeometry(QtCore.QRect(330, 323, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setText("")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.frame_22)
        self.lineEdit_10.setGeometry(QtCore.QRect(50, 315, 271, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setStyleSheet("color: rgb(2, 125, 202);\n"
"padding-left: 23px;\n"
"padding-right: 23px;")
        self.lineEdit_10.setText("")
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.pushButton_10 = QtWidgets.QPushButton(self.frame_22)
        self.pushButton_10.setGeometry(QtCore.QRect(340, 320, 101, 0))
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.955, stop:0 rgba(0, 157, 255, 255), stop:0.552239 rgba(12, 188, 207, 255));\n"
"    color: rgb(42, 42, 42);\n"
"    border-radius: 5px;\n"
"}")
        self.pushButton_10.setObjectName("pushButton_10")
        self.lineEdit_6.raise_()
        self.lineEdit_7.raise_()
        self.lineEdit_8.raise_()
        self.pushButton_5.raise_()
        self.label_11.raise_()
        self.lineEdit_10.raise_()
        self.pushButton_10.raise_()
        self.label_10.raise_()
        self.pushButton_4.raise_()
        self.pushButton_9.raise_()
        self.verticalLayout_9.addWidget(self.frame_22)
        self.frame_23 = QtWidgets.QFrame(self.frame_19)
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_23)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_9.addWidget(self.frame_23)
        self.horizontalLayout_6.addWidget(self.frame_19)
        self.frame_20 = QtWidgets.QFrame(self.frame_17)
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_20)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_6.addWidget(self.frame_20)
        self.verticalLayout.addWidget(self.frame_17)
        self.horizontalLayout_5.addWidget(self.frame_15)
        self.gridLayout.addWidget(self.frame_2, 1, 1, 1, 1)
        self.frame = QtWidgets.QFrame(Profile)
        self.frame.setMinimumSize(QtCore.QSize(550, 0))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)
        self.frame_12 = QtWidgets.QFrame(Profile)
        self.frame_12.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;")
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_12)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_12)
        self.pushButton_3.setMinimumSize(QtCore.QSize(50, 40))
        self.pushButton_3.setMaximumSize(QtCore.QSize(50, 40))
        self.pushButton_3.setWhatsThis("")
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"    height: 50px;\n"
"    border:none;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgba(14, 163, 255, 70);\n"
"}")
        self.pushButton_3.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\feather/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_6.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.gridLayout.addWidget(self.frame_12, 0, 2, 1, 1)
        self.frame_13 = QtWidgets.QFrame(Profile)
        self.frame_13.setMinimumSize(QtCore.QSize(50, 40))
        self.frame_13.setMaximumSize(QtCore.QSize(50, 40))
        self.frame_13.setStyleSheet("border:none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.gridLayout.addWidget(self.frame_13, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Profile)
        QtCore.QMetaObject.connectSlotsByName(Profile)
        Profile.setTabOrder(self.pushButton_3, self.lineEdit)
        Profile.setTabOrder(self.lineEdit, self.lineEdit_2)
        Profile.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        Profile.setTabOrder(self.lineEdit_3, self.lineEdit_4)
        Profile.setTabOrder(self.lineEdit_4, self.lineEdit_5)
        Profile.setTabOrder(self.lineEdit_5, self.pushButton)
        Profile.setTabOrder(self.pushButton, self.pushButton_6)
        Profile.setTabOrder(self.pushButton_6, self.lineEdit_9)
        Profile.setTabOrder(self.lineEdit_9, self.pushButton_7)
        Profile.setTabOrder(self.pushButton_7, self.pushButton_2)
        Profile.setTabOrder(self.pushButton_2, self.lineEdit_6)
        Profile.setTabOrder(self.lineEdit_6, self.lineEdit_7)
        Profile.setTabOrder(self.lineEdit_7, self.lineEdit_8)
        Profile.setTabOrder(self.lineEdit_8, self.pushButton_9)
        Profile.setTabOrder(self.pushButton_9, self.lineEdit_10)
        Profile.setTabOrder(self.lineEdit_10, self.pushButton_4)
        Profile.setTabOrder(self.pushButton_4, self.pushButton_5)
        Profile.setTabOrder(self.pushButton_5, self.pushButton_10)
        Profile.setTabOrder(self.pushButton_10, self.pushButton_8)

    def retranslateUi(self, Profile):
        _translate = QtCore.QCoreApplication.translate
        Profile.setWindowTitle(_translate("Profile", "Dialog"))
        self.label.setText(_translate("Profile", "User Profile"))
        self.label_2.setText(_translate("Profile", "First name"))
        self.label_3.setText(_translate("Profile", "Last name"))
        self.label_4.setText(_translate("Profile", "Email"))
        self.label_5.setText(_translate("Profile", "UserId"))
        self.label_6.setText(_translate("Profile", "Password"))
        self.pushButton.setText(_translate("Profile", "Edit"))
        self.pushButton_2.setText(_translate("Profile", "Change"))
        self.pushButton_6.setText(_translate("Profile", "Send OTP"))
        self.pushButton_7.setText(_translate("Profile", "Save"))
        self.pushButton_8.setText(_translate("Profile", "Resend"))
        self.lineEdit_9.setPlaceholderText(_translate("Profile", "000000"))
        self.label_8.setText(_translate("Profile", "OTP"))
        self.label_7.setText(_translate("Profile", "Change Password"))
        self.lineEdit_6.setPlaceholderText(_translate("Profile", "Current Password"))
        self.lineEdit_7.setPlaceholderText(_translate("Profile", "New Password"))
        self.lineEdit_8.setPlaceholderText(_translate("Profile", "Retype-Password"))
        self.pushButton_4.setText(_translate("Profile", "Save"))
        self.pushButton_5.setText(_translate("Profile", "Back"))
        self.pushButton_9.setText(_translate("Profile", "Send OTP"))
        self.label_10.setText(_translate("Profile", "OTP"))
        self.lineEdit_10.setPlaceholderText(_translate("Profile", "000000"))
        self.pushButton_10.setText(_translate("Profile", "Resend"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Profile = QtWidgets.QDialog()
    ui = Ui_Profile()
    ui.setupUi(Profile)
    Profile.show()
    sys.exit(app.exec_())
