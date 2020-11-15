from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogAboutGrammarAnalyser(object):
    def setupUi(self, DialogAboutGrammarAnalyser):
        DialogAboutGrammarAnalyser.setObjectName("DialogAboutGrammarAnalyser")
        DialogAboutGrammarAnalyser.resize(619, 370)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Qt.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogAboutGrammarAnalyser.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(DialogAboutGrammarAnalyser)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogAboutGrammarAnalyser)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(DialogAboutGrammarAnalyser)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(DialogAboutGrammarAnalyser)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(DialogAboutGrammarAnalyser)
        self.buttonBox.accepted.connect(DialogAboutGrammarAnalyser.accept)
        self.buttonBox.rejected.connect(DialogAboutGrammarAnalyser.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAboutGrammarAnalyser)

    def retranslateUi(self, DialogAboutGrammarAnalyser):
        _translate = QtCore.QCoreApplication.translate
        DialogAboutGrammarAnalyser.setWindowTitle(_translate("DialogAboutGrammarAnalyser", "Acerca de Analizador de Gramáticas"))
        self.textBrowser.setHtml(_translate("DialogAboutGrammarAnalyser", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">Analizador de Gramáticas</span><span style=\" font-size:16pt; color:#005500;\"> </span><span style=\" font-size:16pt; color:#000000;\">es una aplicación que permita realizar determinados procesamientos sobre gramáticas. Dada una gramática libre del contexto verifica el análisis de los parsers LL(1), SLR(1), LR(1) y LALR, dando a conocer en cada caso la colección de items, su autómata y las tablas ACTION - GOTO. Además se mostrarán los conjuntos First y Follow, las derivaciones según el parser y en caso de gramática regular un autómata y expresión regular.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#000000;\">Esta aplicación corre tanto en Window como en Linux, siempre y cuando esté instalado </span><span style=\" font-size:16pt; font-weight:600; color:#000000;\">python3</span><span style=\" font-size:16pt; color:#000000;\"> y </span><span style=\" font-size:16pt; font-weight:600; color:#000000;\">PyQt5</span><span style=\" font-size:16pt; color:#000000;\">.</span></p></body></html>"))
        self.label.setText(_translate("DialogAboutGrammarAnalyser", "<html><head/><body><p align=\"center\">Acerca de Analizador de Gramáticas</p></body></html>"))
