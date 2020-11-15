from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogWords(object):
    def setupUi(self, DialogWords):
        DialogWords.setObjectName("DialogWords")
        DialogWords.resize(507, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Qt.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogWords.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(DialogWords)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogWords)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.wordsText = QtWidgets.QPlainTextEdit(DialogWords)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        self.wordsText.setFont(font)
        self.wordsText.setPlainText("")
        self.wordsText.setObjectName("wordsText")
        self.gridLayout.addWidget(self.wordsText, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(DialogWords)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(DialogWords)
        self.buttonBox.accepted.connect(DialogWords.accept)
        self.buttonBox.rejected.connect(DialogWords.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogWords)

    def retranslateUi(self, DialogWords):
        _translate = QtCore.QCoreApplication.translate
        DialogWords.setWindowTitle(_translate("DialogWords", "Cadenas de Prueba"))
        self.label.setText(_translate("DialogWords", "<html><head/><body><p align=\"center\">Escriba algunas cadenas</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogWords = QtWidgets.QDialog()
    ui = Ui_DialogWords()
    ui.setupUi(DialogWords)
    DialogWords.show()
    sys.exit(app.exec_())
