# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 11:13:05 2022

@author: kasimoglu
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5 import Qt
from traceback import print_exception


class ButtonManager(QWidget):
    """Generates the buttons and bind them with functions"""
    def __init__(self):
        super().__init__()

    def set_buttons(self, parent):
        """Generates the buttons for DoE page and bind them with functions"""
        self.Font = QFont()
        self.Font.setBold(True)

        self.button_import_csv = QPushButton("Import CSV", parent)
        self.button_export_csv = Qt.QPushButton("Export CSV", parent)
        self.button_lock_cells = Qt.QPushButton("Lock Cells", parent)
        self.button_unlock_cells = Qt.QPushButton("Unlock Cells", parent)
        self.button_clear_cells = Qt.QPushButton("Clear Cells", parent)
        self.button_add_col = Qt.QPushButton("Add Col", parent)
        self.button_remove_col = QPushButton("Remove Col", parent)
        self.button_add_row = QPushButton("Add Row", parent)
        self.button_remove_row = QPushButton("Remove Row", parent)
        
        self.button_import_csv.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.button_export_csv.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.button_lock_cells.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.button_unlock_cells.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.button_clear_cells.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")  
        self.button_add_col.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.button_remove_col.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.button_add_row.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.button_remove_row.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")        
        self.button_import_csv.setFont(self.Font) 
        self.button_export_csv.setFont(self.Font)  
        self.button_lock_cells.setFont(self.Font)  
        self.button_unlock_cells.setFont(self.Font)
        self.button_clear_cells.setFont(self.Font)
        self.button_add_col.setFont(self.Font) 
        self.button_remove_col.setFont(self.Font)  
        self.button_add_row.setFont(self.Font)  
        self.button_remove_row.setFont(self.Font)

        self.button_auto_test_page = QtWidgets.QPushButton(parent)
        self.button_auto_test_page.setText("Next")

        parent.doe_buttons_layout.addWidget(self.button_import_csv)        
        parent.doe_buttons_layout.addWidget(self.button_export_csv)
        parent.doe_buttons_layout.addWidget(self.button_lock_cells)
        parent.doe_buttons_layout.addWidget(self.button_unlock_cells)
        parent.doe_buttons_layout.addWidget(self.button_clear_cells) 
        parent.doe_buttons2_layout.addWidget(self.button_add_col)        
        parent.doe_buttons2_layout.addWidget(self.button_remove_col)
        parent.doe_buttons2_layout.addWidget(self.button_add_row)
        parent.doe_buttons2_layout.addWidget(self.button_remove_row)
        parent.doe_buttons2_layout.addWidget(self.button_auto_test_page)  
        parent.exprment_box_layout.addLayout(parent.doe_buttons_layout)
        parent.exprment_box_layout.addLayout(parent.doe_buttons2_layout)

        self.button_auto_test_page.setFont(self.Font)
        self.button_auto_test_page.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
            
        self.button_import_csv.clicked.connect(parent.import_csv) 
        self.button_export_csv.clicked.connect(parent.export_csv) 
        self.button_lock_cells.clicked.connect(parent.lock_cells)
        self.button_unlock_cells.clicked.connect(parent.unlock_cells)        
        self.button_clear_cells.clicked.connect(parent.clear_cells)
        self.button_add_col.clicked.connect(parent.add_column)
        self.button_remove_col.clicked.connect(parent.remove_column)           
        self.button_add_row.clicked.connect(parent.add_row)
        self.button_remove_row.clicked.connect(parent.remove_row)
        self.button_auto_test_page.clicked.connect(parent.skip_next_page)
        
        self.button_auto_test_page.clicked.connect(
            parent.make_handle_button("engine test manager"))
