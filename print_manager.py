# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 11:17:18 2022

@author: kasimoglu
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtWidgets import QMessageBox
from traceback import print_exception


class PrintManager(QWidget):
    """Notify the users of important information.
    
    This class is responsible for printing iteration results 
    and purpose of the tool (about func).     
    """
    def __init__(self):
        super().__init__()
    def print_det_results(self, parent):
        """Prints the determinant results"""
        self.det_val_to_be_printed = QTextEdit(parent)
     #   self.detPrnt = int(len(parent.det_of_testpoints)) / 2
        for i in range(parent.num_of_iter):
            print_val = str(i + 1) + ". iteration determinant value is " \
            + str(round(parent.det_of_testpoints[2*i + 1], 3))
            self.det_val_to_be_printed.append(print_val)
    
        max_value = max(parent.det_of_testpoints)
        max_index = parent.det_of_testpoints.index(max_value)
        self.det_val_to_be_printed.append("")         
        slctd_iter = str(round(((max_index - 1) / 2) + 1)) \
                   + ". iteration is selected"
        
        self.det_val_to_be_printed.append(slctd_iter)
   
        parent.variable_box_layout.addWidget(
            self.det_val_to_be_printed, 1, 0, 1, 1)

        self.det_val_to_be_printed.show()
    
    def info_about_program(self,parent):
        """Prints the information about tool"""
        msg = QMessageBox(parent)
        msg.setWindowTitle("Tutorial on PyQt5")
        msg.setText("This is the main text!")
        msg.setIcon(QMessageBox.Question)
    #    msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Retry|QMessageBox.Ignore|)
        msg.setDefaultButton(QMessageBox.Retry)
        msg.setInformativeText(
            "This application has two main abilities. DoE (Design of     \
            Experiment) point generation and test automation. \n\nDoE point  \
            generation is based on D-Optimal experiment design. Application \
            will provide local d-optimal but not global d-optimal. Right now \
            application is able to generate experiments only for 4 variables. \
            Not more, not less.\n\n Test automation is based on ATI's API. It\
            is designed to use with Vision ATI which have API tool as add-in. \
            There isn't any restriction on the variable number. One could \
            easily use test automation part without touching the DoE part")

        msg.setDetailedText("details")
        print("print managerdayız")
        msg.show()

    # def testProg(self,parent,i):
    #     msg = QMessageBox(self)
    #     msg.setWindowTitle("Tutorial on PyQt5")
    #     msg.setText("This is the main text!")
    #     msg.setIcon(QMessageBox.Question)
    #     msg.setDefaultButton(QMessageBox.Retry)
    #     msg.setInformativeText(str(i+1)+". Step \n" + " \n \n Test is in progress: \n")

    #     msg.setDetailedText("details")

    #     msg.show()