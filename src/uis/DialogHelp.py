# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogHelp.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogHelp(object):
    def setupUi(self, DialogHelp):
        DialogHelp.setObjectName("DialogHelp")
        DialogHelp.resize(760, 521)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Qt.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogHelp.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(DialogHelp)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogHelp)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(DialogHelp)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(DialogHelp)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(DialogHelp)
        self.buttonBox.accepted.connect(DialogHelp.accept)
        self.buttonBox.rejected.connect(DialogHelp.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogHelp)

    def retranslateUi(self, DialogHelp):
        _translate = QtCore.QCoreApplication.translate
        DialogHelp.setWindowTitle(_translate("DialogHelp", "Ayuda"))
        self.textBrowser.setHtml(_translate("DialogHelp", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">Para analizar una gramática siga los siguientes pasos:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">1. La grámatica debe ser libre del contexto y se escribe en el siguiente formato:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">S -&gt; A | B</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">A -&gt; a A | epsilon</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">B -&gt; b B | epsilon</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Usa \'</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">-&gt;</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">\' para indicar una </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">producción</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">, y \'</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">|</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">\' para indicar múltiples producciones con la misma cabecera.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Usa \'</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">epsilon</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">\' para indicar el símbolo </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">Terminal</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\"> especial de la </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">grámatica</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Todos los símbolos que sean cabecera de alguna </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">producción</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\"> serán los </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">No Terminales</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">, el resto serán considerados como </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">Terminales</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">. Use de ser posible solo letras en la defeinición de los </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">No Terminales</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Entre dos símbolos contiguos deje siempre al menos un espacio.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Se le notificará si la </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:600;\">gramática</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\"> no se encuentra en el formato apropiado.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">2. Si no desea analizar ninguna cadena, continue con &quot;Análisis rápido (F9)&quot;.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Verá los resultados en la pestaña &quot;Resultados&quot;.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">3. Si desea analizar además algunas cadenas, continue con &quot;Analizar (F5)&quot;.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">A continuación deberá entrar las cadenas deseadas, debe dejar al menos un espacio entre dos tokens contiguos.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">Luego verá los resultados en la pestaña &quot;Resultados&quot;.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">4. Al finalizar, usted puede además guardar la gramática en formato de texto, para su uso futuro.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:18pt; color:#000000;\">•</span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:8pt; color:#e6db74;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">De igual forma se puede cargar una gramática en formato de texto, en cuyo caso deberá realizar los</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt;\">pasos desde el inicio.</span></p></body></html>"))
        self.label.setText(_translate("DialogHelp", "<html><head/><body><p align=\"center\">Ayuda</p></body></html>"))
