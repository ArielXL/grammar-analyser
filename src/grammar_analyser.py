import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *

from uis.MainWindow import Ui_MainWindow
from uis.DialogHelp import Ui_DialogHelp
from uis.DialogWords import Ui_DialogWords
from uis.DialogAboutAuthors import Ui_DialogAboutAuthors
from uis.DialogAboutGrammarAnalyser import Ui_DialogAboutGrammarAnalyser

from cmp.html import Html
from cmp.parsers import *
from cmp.utils_parsers import UtilsParsers
from cmp.html_formatter import HtmlFormatter
from cmp.notification import NotificationWindow
from cmp.utils_grammar import UtilsGrammar, BadTextFormatException

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionNewGrammar.triggered.connect(self.NewGrammar)
        self.ui.actionLoadGrammar.triggered.connect(self.LoadGrammar)
        self.ui.actionSaveGrammar.triggered.connect(self.SaveGrammar)
        self.ui.actionAnalyse_2.triggered.connect(self.ShowWordsDialog)
        self.ui.actionQuickAnalyse_2.triggered.connect(self.QuickAnalyseGrammar)
        self.ui.actionExit.triggered.connect(self.Exit)
        self.ui.actionHelp_2.triggered.connect(self.Help)
        self.ui.actionAboutAuthors.triggered.connect(self.AboutAuthors)
        self.ui.actionAboutGrammarAnalyser.triggered.connect(self.AboutGrammarAnalyser)
        
        self.NewGrammar()

    def ClearResults(self):
        self.ui.tabWidget.setTabEnabled(1, False)
    
    def UpdateStatus(self):
        self.ui.tabWidget.setStatusTip(self.path if self.path else "*Nueva Gramática")

    def NewGrammar(self):
        self.path = None
        self.ui.textEditGrammar.setPlainText("")
        self.UpdateStatus()
        self.ClearResults()

    def DialogCritical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def LoadGrammar(self):
        path, _ = QFileDialog.getOpenFileName(self, "Cargar Gramática", "", "Documentos de texto (*.txt)")

        if not path:
            return

        try:
            with open(path, 'r') as f:
                text = f.read()
        except Exception as e:
            self.DialogCritical(str(e))
        else:
            self.path = path
            self.ui.textEditGrammar.setPlainText(text)
            self.UpdateStatus()
            self.ClearResults()

    def SaveGrammar(self):
        if self.path is None:
            return self.SaveGrammarAs()

        text = self.ui.textEditGrammar.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.DialogCritical(str(e))

    def SaveGrammarAs(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Gramática", "", "Documentos de texto (*.txt)")
        text = self.ui.textEditGrammar.toPlainText()

        if not path:
            return

        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.UpdateStatus()

    def Exit(self):
        self.close()

    def ShowWordsDialog(self):
        self.ui_dialog = Ui_DialogWords()
        dialog = QDialog()
        self.ui_dialog.setupUi(dialog)

        dialog.accepted.connect(self.NormalAnalyseGrammar)
        self.ui_dialog.wordsText.setFocus()

        dialog.exec()

    def NormalAnalyseGrammar(self):
        return self.AnalyseGrammar(self.ui_dialog.wordsText.toPlainText().split('\n'))

    def QuickAnalyseGrammar(self):
        return self.AnalyseGrammar()
    
    def AnalyseGrammar(self, words=[]):

        text = self.ui.textEditGrammar.toPlainText()

        try:
            grammar = UtilsGrammar.GetGrammar(text)
            grammar_html = HtmlFormatter.GrammarToHtml(grammar)

        except BadTextFormatException:
            print('La gamática no está escrita en el formato correcto. Lea la ayuda de Analizador de Gramáticas.')
            # NotificationWindow.error('Error', 
            #                         '''<html><head/><body><span style=" font-style:italic; color:teal;">
            #                         <p>La gamática no está escrita en el formato correcto.</p>
            #                         <p>Lea la ayuda de Analizador de Gramáticas.</p><p></p>
            #                         </span></body></html>''', callback=lambda: self.how_to_use())

        else:
            print('La gramática está siendo analizada. Espere unos segundos.')
            # NotificationWindow.info('Analizando', 
            #                         '''<html><head/><body><span style="color:gray;">
            #                         <p>La gramática está siendo analizada.</p>
            #                         <p>Espere unos instantes.</p><p></p>
            #                         </span></body></html>''')

            # parsear las cadenas a procesar
            words = [UtilsParsers.Tokenizer(grammar, word) for word in words]

            # eliminando producciones innecesarias, recursion izquierda inmediata y prefijos comunes
            grammar_clone = UtilsGrammar.CloneGrammar(grammar)
            is_not_null, acepted_symbols = UtilsGrammar.IsNotNull(grammar_clone)
            UtilsGrammar.RemoveUnnecessaryProductions(grammar_clone, keep_symbols=acepted_symbols)
            UtilsGrammar.RemoveLeftRecursion(grammar_clone)
            UtilsGrammar.RemoveCommonPrefix(grammar_clone)
            is_not_null_html = ''
            grammar_clone_html = HtmlFormatter.GrammarToHtml(grammar_clone)
            if not is_not_null:
                is_not_null_html = HtmlFormatter.ErrorMessageToHtml('Esta gramática genera el lenguaje: \N{LATIN CAPITAL LETTER O WITH STROKE}.')
            
            # analizando si la gramatica es regular, y en este caso, hallando automata regular y expresion regular
            regular_automaton, is_regular = UtilsGrammar.BuildAutomaton(grammar) 
            regular_expresion = UtilsGrammar.GetRegularExpression(regular_automaton)
            if is_regular:
                is_regular_html = HtmlFormatter.GoodMessageToHtml('La gramática es regular.')
                regular_automaton_html = regular_automaton._repr_svg_()
                regular_expresion_html = HtmlFormatter.MessageToHtml(regular_expresion)
            else:
                is_regular_html = HtmlFormatter.ErrorMessageToHtml('La gramática no es regular.')
                regular_automaton_html = HtmlFormatter.ErrorMessageToHtml('Imposible obtener el autómata, la gramática no es regular.')
                regular_expresion_html = HtmlFormatter.ErrorMessageToHtml('Imposible obtener la expresión regular, la gramática no es regular.')
            if regular_automaton_html is None:
                regular_automaton_html = HtmlFormatter.ErrorMessageToHtml('Imposible mostrar el autómata, ver problemas con el software Graphviz.')

            # obteniendo firsts
            firsts = UtilsParsers.ComputeFirsts(grammar)
            firsts_html = HtmlFormatter.FirstsToHtml(grammar, firsts)
            
            # obteniendo follows
            follows = UtilsParsers.ComputeFollows(grammar, firsts)
            follows_html = HtmlFormatter.FollowsToHtml(grammar, follows)
            
            parser, parse_type = None, None

            # analizando parser LL(1)
            ll1_table, is_ll1 = LL1Parser.Build_LL1_Table(grammar, firsts, follows)
            parser_ll1 = LL1Parser.NonRecursivePredictiveMethod(grammar, ll1_table, firsts, follows)
            ll1_table_html = HtmlFormatter.LL1TableToHtml(grammar, ll1_table, 'NoT-T')
            if is_ll1:
                is_ll1_html = HtmlFormatter.GoodMessageToHtml('La gramática es LL(1).')
                parser, parse_type = parser_ll1, 'left'
            else:
                is_ll1_html = HtmlFormatter.ErrorMessageToHtml('La gramática no es LL(1).')
            
            # analizando parser SLR(1)
            parser_slr1 = SLR1Parser(grammar)
            if parser_slr1.is_slr1:
                parser, parse_type = parser_slr1, 'right'
                is_slr1_html = HtmlFormatter.GoodMessageToHtml('La gramática es SLR(1).')
            else:
                is_slr1_html = HtmlFormatter.ErrorMessageToHtml('La gramática no es SLR(1).')
            items_collection_lr0_html = HtmlFormatter.ItemsCollectionToHtml(parser_slr1.automaton)
            automaton_lr0_html = parser_slr1.automaton._repr_svg_()
            if automaton_lr0_html is None:
                automaton_lr0_html = HtmlFormatter.ErrorMessageToHtml('Imposible mostrar el autómata, ver problemas con el software Graphviz.')
            action_slr1_html = HtmlFormatter.ActionGotoTableToHtml(parser_slr1.action, parser_slr1.G.terminals + [parser_slr1.G.EOF], 'ACTION')
            goto_slr1_html = HtmlFormatter.ActionGotoTableToHtml(parser_slr1.goto, parser_slr1.G.nonTerminals, 'GOTO')

            # analizando parser LR(1)
            parser_lr1 = LR1Parser(grammar)
            if parser_lr1.is_lr1:
                parser, parse_type = parser_lr1, 'right'
                is_lr1_html = HtmlFormatter.GoodMessageToHtml('La gramática es LR(1).')
            else:
                is_lr1_html = HtmlFormatter.ErrorMessageToHtml('La gramática no es LR(1).')
            items_collection_lr1_html = HtmlFormatter.ItemsCollectionToHtml(parser_lr1.automaton)
            automaton_lr1_html = parser_lr1.automaton._repr_svg_()
            if automaton_lr1_html is None:
                automaton_lr1_html = HtmlFormatter.ErrorMessageToHtml('Imposible mostrar el autómata, ver problemas con el software Graphviz.')
            action_lr1_html = HtmlFormatter.ActionGotoTableToHtml(parser_lr1.action, parser_lr1.G.terminals + [parser_lr1.G.EOF], 'ACTION')
            goto_lr1_html = HtmlFormatter.ActionGotoTableToHtml(parser_lr1.goto, parser_lr1.G.nonTerminals, 'GOTO')

            # analizando parser LALR
            parser_lalr = LALRParser(grammar)
            if parser_lalr.is_lr1:
                parser, parse_type = parser_lalr, 'right'
                is_lalr_html = HtmlFormatter.GoodMessageToHtml('La gramática es LALR.')
            else:
                is_lalr_html = HtmlFormatter.ErrorMessageToHtml('La gramática no es LALR.')
            items_collection_lalr_html = HtmlFormatter.ItemsCollectionToHtml(parser_lalr.automaton)
            automaton_lalr_html = parser_lalr.automaton._repr_svg_()
            if automaton_lalr_html is None:
                automaton_lalr_html = HtmlFormatter.ErrorMessageToHtml('Imposible mostrar el autómata, ver problemas con el software Graphviz.')
            action_lalr_html = HtmlFormatter.ActionGotoTableToHtml(parser_lalr.action, parser_lalr.G.terminals + [parser_lalr.G.EOF], 'ACTION')
            goto_lalr_html = HtmlFormatter.ActionGotoTableToHtml(parser_lalr.goto, parser_lr1.G.nonTerminals, 'GOTO')

            # hallando los arboles de derivacion de las cadenas provistas
            derivations = [parser(word) for word in words] if parser else []
            derivations = [DerivationTree.GetTree(derivation, parse_type)._repr_svg_() if derivation else None for derivation in derivations]
            derivations_html = HtmlFormatter.DerivationsToHtml(words, derivations) if derivations else HtmlFormatter.ErrorMessageToHtml('La gramática no es LL(1), ni SLR(1), ni LR(1), imposible obtener las derivaciones.') if words else HtmlFormatter.ErrorMessageToHtml('No se seleccionó ninguna cadena.')

            # hallando la gramatica aumentada
            augmented_grammar_html = HtmlFormatter.GrammarToHtml(parser_slr1.augmentedG)


            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.textResults.setHtml(Html % (grammar_html + is_not_null_html, grammar_clone_html,
                                            firsts_html, follows_html, ll1_table_html, is_ll1_html, 
                                            augmented_grammar_html, 
                                            items_collection_lr0_html, automaton_lr0_html, action_slr1_html, 
                                            goto_slr1_html, is_slr1_html,
                                            items_collection_lr1_html, automaton_lr1_html, action_lr1_html, 
                                            goto_lr1_html, is_lr1_html,
                                            items_collection_lalr_html, automaton_lalr_html, action_lalr_html, 
                                            goto_lalr_html, is_lalr_html, derivations_html,
                                            is_regular_html, regular_automaton_html, regular_expresion_html))

            print('Listo. El análisis de la gramática ha termiando. Todos los resultados están listos.')
            # NotificationWindow.success('Listo', 
            #                         '''<html><head/><body><span style="color:green;">
            #                         <p>El análisis de la gramática ha termiando.</p>
            #                         <p>Todos los resultados están listos.</p><p></p>
            #                         </span></body></html>''')

    def Help(self):
        dialog = QDialog()
        ui_dialog = Ui_DialogHelp()
        ui_dialog.setupUi(dialog)

        dialog.exec()

    def AboutAuthors(self):
        dialog = QDialog()
        ui_dialog = Ui_DialogAboutAuthors()
        ui_dialog.setupUi(dialog)

        dialog.exec()

    def AboutGrammarAnalyser(self):
        dialog = QDialog()
        ui_dialog = Ui_DialogAboutGrammarAnalyser()
        ui_dialog.setupUi(dialog)

        dialog.exec()

def Main():

    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    Main()
