# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 11:03:38 2022

@author: kasimoglu
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtWidgets import QFileDialog
import csv
from doe_point_generator import DoEPointGenerator
from engine_test_manager import EngineTestManager


class tableManager(QWidget):
    """Generates table which displays the DoE points"""
    def __init__(self):
        super().__init__() 

    def generate_table(self, parent):
        """Generates an initial table by 7*21"""
        self.table_generator = QTableWidget(parent)
        self.table_generator.setRowCount(21)
        self.table_generator.setColumnCount(7)

        self.get_test_var = DoEPointGenerator()
        self.test_variables = self.get_test_var.get_variable_name(self)

        for j in range(0,len(self.test_variables)):
            if j==0:
                self.table_generator.setItem(0,0, QTableWidgetItem("Step"))    
            self.table_generator.setItem(
                0, j + 1, QTableWidgetItem(str(self.test_variables[j])))            


        parent.variable_box_layout.addWidget(self.table_generator, 0, 0, 1, 2)
        self.table_generator.setMaximumHeight(500)
        return self.table_generator

    def adapt_row_n_column(self,parent):
        """Changes the row and column number of initial table based on DoE 
        results
        """
        self.table_generator.setRowCount(int(parent.row_num) + 1)
        self.table_generator.setColumnCount(int(parent.col_num) + 2)
        return self.table_generator

    def doe_points_to_table(self,doeLabelFinal,doePointFinal,duration,Row, Column):
        """Copies the DoE results to the table"""
        # Step number, duration, signals and test points are merged into a matrice.       
        self.doeActMatrixFinal=[]
        print(len(doePointFinal)+1)
        for i in range(len(doePointFinal)+1):
            self.doeActMatrixFinal.append([])
            if i==0:
                self.doeActMatrixFinal[i].append("Step") 
                for j in range(len(doeLabelFinal)):
                    self.doeActMatrixFinal[i].append(doeLabelFinal[j])
                self.doeActMatrixFinal[i].append("Time")

            else:
                self.doeActMatrixFinal[i].append(i)                
                for k in range(int(Column)):    
                    self.doeActMatrixFinal[i].append(doePointFinal[i-1][k])
                self.doeActMatrixFinal[i].append(duration)
        print(self.doeActMatrixFinal)
        for i in range(len(doePointFinal)+1): 
            for j in range(int(Column)+2):
                self.table_generator.setItem(
                    i, j, QTableWidgetItem(str(self.doeActMatrixFinal[i][j])))
        return self.table_generator
    
    def enable_read_only(self,parent):
        """Enables read only mode for table"""
        self.table_generator.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers)

    def enable_read_write(self,parent):     
        """Enables read and write mode for table"""
        self.table_generator.setEditTriggers(
            QtWidgets.QTableWidget.AllEditTriggers)

    def clear_cells(self,parent):
        """Clear cells in the table"""
        num_of_var=self.table_generator.columnCount()
        num_of_step=self.table_generator.rowCount()
        for i in range(num_of_step): 
            for j in range(int(num_of_var)):
                self.table_generator.setItem(i, j, QTableWidgetItem(str(''))) 
                
    def add_column(self,parent):
        """Add 1 column to table"""
        num_of_col = self.table_generator.columnCount()
        self.table_generator.setColumnCount(num_of_col + 1)

    def remove_column(self,parent):
        """Remove 1 column from table"""
        num_of_col = self.table_generator.columnCount()
        self.table_generator.setColumnCount(num_of_col - 1)

    def add_row(self,parent):
        """Add 1 row to table"""
        num_of_row = self.table_generator.rowCount()
        self.table_generator.setRowCount(num_of_row + 1)

    def remove_row(self,parent):
        """Remove 1 row from table"""
        num_of_row = self.table_generator.rowCount()
        self.table_generator.setRowCount(num_of_row - 1)
            
    def import_csv(self,parent):
        """Imports the csv to table"""
        file_data, not_used = QFileDialog.getOpenFileNames(self)
        with open(file_data[0], "rt")as f:         
            data = csv.reader(f)
 
            num_of_var = 0
            num_of_step = 0
            self.importedCsv=[]
            for row in data:
                num_of_step+=1
                self.importedCsv.append([])
                for j in range(len(row)):
                    self.importedCsv[num_of_step - 1].append(row[j])
                 
            num_of_var = len(row)
            self.table_generator.setRowCount(num_of_step)
            self.table_generator.setColumnCount(num_of_var)            
           
            for i in range(num_of_step): 
                for j in range(num_of_var):
                    self.table_generator.setItem(
                        i, j, QTableWidgetItem(str(self.importedCsv[i][j]))) 
                    
    def export_csv(self,parent):
        """Exports the table to csv"""
        column = self.table_generator.columnCount()
        row = self.table_generator.rowCount()
        export_csv = []
        print(row, column)
        for i in range(row): 
            export_csv.append([])
            for j in range(column):
                a=self.table_generator.item(i, j)
                if a == None:
                    a = 0
                else:
                    a = self.table_generator.item(i,j).text()
                export_csv[i].append(a)
        # print(export_csv)
        export=QFileDialog.getSaveFileName()
        with open(str(export[0] + ".csv"), 
                  mode='w', newline='') as experiment_list:            
            experiment_list_final = csv.writer(
                experiment_list, delimiter=',', quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
            experiment_list_final.writerows(export_csv)

    def data_to_next_page(self,parent):
        """Copies data in the table from first page to second page.
        
        First page: DoE Manager
        Second page: Engine Test Manager
        """
        EngineTestManager.data_transfer = []           
        num_of_col = self.table_generator.columnCount()
        num_of_row = self.table_generator.rowCount()

        empty_col=0
        empty_row=0
        
        # Here to copy info in the table to the table in Engine Test Manager \
        # empy rows and columns are determined and simply dropped.
        for i in range(num_of_row):

            for j in range(num_of_col):
                a = self.table_generator.item(i, j)
                if a == None and i == 0:
                    empty_col += 1
                elif a == None and j == 0:
                    empty_row += 1
        num_of_col = num_of_col - empty_col
        num_of_row = num_of_row - empty_row            
        for i in range(num_of_row):

            EngineTestManager.data_transfer.append([])
            for j in range(num_of_col):
                a = self.table_generator.item(i, j)
                if a == None:
                    a = 0
                else:
                    a = self.table_generator.item(i, j).text()
                EngineTestManager.data_transfer[i].append(a)
        
        return EngineTestManager.data_transfer 