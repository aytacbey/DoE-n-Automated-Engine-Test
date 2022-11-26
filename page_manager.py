# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 10:21:17 2022

@author: kasimoglu
"""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot


class PageManager(QWidget):
    """Helps to switch between pages and intermediary step for signal-slot 
    processes
    """
    go_to_func_sgnl = QtCore.pyqtSignal(str)
    clear_cells_func_sgnl = QtCore.pyqtSignal(str)
    import_csv_func_sgnl = QtCore.pyqtSignal(str)
    export_csv_func_sgnl = QtCore.pyqtSignal(str)
    lock_cells_func_sgnl = QtCore.pyqtSignal(str)
    unlock_cells_func_sgnl = QtCore.pyqtSignal(str)
    add_column_func_sgnl = QtCore.pyqtSignal(str)
    remove_column_func_sgnl = QtCore.pyqtSignal(str)
    add_row_func_sgnl = QtCore.pyqtSignal(str)
    remove_row_func_sgnl = QtCore.pyqtSignal(str)
    doe_points_trnsfr_func_sgnl = QtCore.pyqtSignal(list,list,str,str,int)

    data_btw_page_signal = QtCore.pyqtSignal(str)


    def skip_to(self, name):
        """Signal which triggers skipping to next page is emitted"""
        self.go_to_func_sgnl.emit(name)

    def sent_doe_points(self): #,receiveDoeLabel,final_doe_points,tDuration, nRow, nColumn
        """Sent DoE results to table"""
        self.doe_points_trnsfr_func_sgnl.emit(
            self.get_doe_labels, self.final_doe_points, self.test_step_time, 
            self.num_of_row, self.num_of_col)
    
    # def data_to_next_page(self):
    #     """Sent the data on the first page to second page"""
    #     self.data_btw_page_signal.emit("yeni veri transferi")
        
    def import_csv_from_master(self):
        """Release of import csv func which is activated from main module"""
        self.import_csv_func_sgnl.emit("done")
        
    def export_csv_from_master(self):
        """Release of export csv func which is activated from main module"""
        self.export_csv_func_sgnl.emit("done")
