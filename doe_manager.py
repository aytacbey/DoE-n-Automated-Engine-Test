# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 10:24:40 2022

@author: kasimoglu
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLineEdit

from page_manager import PageManager
from table_manager import tableManager
from button_manager import ButtonManager
from print_manager import PrintManager
from doe_point_generator import DoEPointGenerator


class DoEManager(PageManager):
    """Arrange all things related to DoE"""
    def __init__(self):
        super().__init__()
      
        self.initUI()
    
    def initUI(self):
        """Initialize UI"""
        self.UiComponents()

    def UiComponents(self):
        self.font = QFont()
        self.font.setBold(True)       

        # Groupbox layoutis generated
        self.form_group_box = QGroupBox("Project")
        self.init_layout = QGridLayout()
        self.form_group_box.setLayout(self.init_layout)

        # Variables groupbox layout

        self.inner_group_box = QGroupBox("Variables")
        self.variable_box_layout = QGridLayout()

        # Basic commands groupbox layout
        self.exprment_group_box = QGroupBox("Basic Commands")
        self.exprment_box_layout = QVBoxLayout()  
        self.doe_buttons_layout = QHBoxLayout()
        self.doe_buttons2_layout = QHBoxLayout()
    

        self.exprment_group_box.setLayout(self.exprment_box_layout)
        self.inner_group_box.setLayout(self.variable_box_layout)
        # self.form_group_box.setLayout(self.init_layout)       
        
        # Main layout
        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.form_group_box)
        self.main_layout.addWidget(self.inner_group_box)
        self.main_layout.addWidget(self.exprment_group_box)       
        self.setLayout(self.main_layout)

        #  Buttons are generated
        self.table_widget = tableManager()
        self.table_widget.generate_table(self) #self.returnedtabloWidget = 
        self.button_generator = ButtonManager()
        self.button_generator.set_buttons(self)
        self.print_widget = PrintManager()
        self.font = QFont()
        self.font.setBold(True)

        # Labels for boundaries of sample space
        self.label_var_boundary = QtWidgets.QLabel(self)
        self.label_min_boundary = QtWidgets.QLabel(self)
        self.label_max_boundary = QtWidgets.QLabel(self)       
        self.label_variables = QtWidgets.QLabel(self)
        self.label_variables.setText("Variables")
        self.label_variables.setFont(self.font)

        self.setWindowTitle("DoE")
        
        self.label_steps = QtWidgets.QLabel(self)
        self.label_steps.setText("Steps")
        self.label_steps.setFont(self.font)

        self.label_duration = QtWidgets.QLabel(self)
        self.label_duration.setText("Duration")
        self.label_duration.setFont(self.font)       
            
        self.dropdown_var_num = QComboBox(self)
        self.num_var_list = ["4"]
        self.dropdown_var_num.addItems(self.num_var_list)
        
        self.line_steps = QLineEdit(self)        
        self.line_steps.move(200, 80)
        self.line_steps.resize(60, 28)
        self.line_duration = QLineEdit(self)        
        self.line_duration.move(300, 80)
        self.line_duration.resize(60, 28)

        # Arranging the instances for DoE inputs
        self.label_duration.setMaximumWidth(100)  
        self.dropdown_var_num.setMaximumWidth(100) 
        self.label_steps.setMaximumWidth(100)
        self.line_steps.setMaximumWidth(100)
        self.label_duration.setMaximumWidth(100)
        self.line_duration.setMaximumWidth(100)   
        self.init_layout.addWidget(self.label_variables, 0, 1, 1, 1)
        self.init_layout.addWidget(self.label_steps, 0, 2, 1, 1)
        self.init_layout.addWidget(self.label_duration, 0, 3, 1, 1)
        self.init_layout.addWidget(self.dropdown_var_num, 1, 1, 1, 1)
        self.init_layout.addWidget(self.line_steps, 1, 2, 1, 1)
        self.init_layout.addWidget(self.line_duration, 1, 3, 1, 1)                 

        self.button_submit = QtWidgets.QPushButton(self)
        self.button_submit.setText("Submit")
        self.button_submit.setFont(self.font)
        self.button_submit.setMaximumWidth(100) 

        self.init_layout.addWidget(self.button_submit, 1, 4, 1, 3)
        self.button_submit.setStyleSheet("background-color:white;\n"

                                      "border-width:5px;\n")       

        self.button_submit.clicked.connect(self.get_exp_info)
        self.button_submit.clicked.connect(self.set_exp_design_env)

    def update(self):
        """Updates the label size"""
        self.label.adjustSize()

    def get_exp_info(self):
        """Number of row, column and step time is taken"""
        self.num_of_row = self.line_steps.text()
        self.num_of_col = int(self.dropdown_var_num.currentText())
        self.test_step_time = self.line_duration.text()
        
        return self.num_of_row,self.test_step_time

    def lock_cells(self):
        """Enable read-only for table"""
        self.table_widget.enable_read_only(self)      

    def unlock_cells(self):
        """Enable read and write for table"""
        self.table_widget.enable_read_write(self)  

    def clear_cells(self):
        """Clear all the cells in the table"""
        self.table_widget.clear_cells(self)        

    def import_csv(self):
        """Import from csv to the table"""
        self.table_widget.import_csv(self)  

    def export_csv(self):
        """Export from table to csv"""
        self.table_widget.export_csv(self) 

    def add_column(self):
        """Add 1 column to table"""
        self.table_widget.add_column(self)

    def remove_column(self):
        """Remove 1 column from table"""
        self.table_widget.remove_column(self)

    def add_row(self):
        """Add 1 row to table"""
        self.table_widget.add_row(self)

    def remove_row(self):
        """Remove 1 row from table"""
        self.table_widget.remove_row(self)
     
    def quit_app(self):
        """Close app"""
        self.close()
        
    def set_exp_design_env(self):
        """Instances for inputs for DoE"""
        self.num_of_var=int(self.dropdown_var_num.currentText())

        self.boundaryWidget = tableManager()

        self.label_var_boundary.setText("Var:")
        self.label_var_boundary.setFont(self.font)
     
        self.label_max_boundary.setText("Min:")
        self.label_max_boundary.setFont(self.font)       

        self.label_min_boundary.setText('Max:')
        self.label_min_boundary.setFont(self.font)       
  
        self.label_model_sel=QtWidgets.QLabel(self)
        self.label_model_sel.setText('Model Selection:')
        self.label_model_sel.setFont(self.font)

        self.label_model_sel.show()
 
        self.label_ite_num = QtWidgets.QLabel(self)
        self.label_ite_num.setText('Iteration No:')
        self.label_ite_num.setFont(self.font)        

        self.label_ite_num.show()       
   
        self.line_exp_var_list = {}           

        self.dropdown_model_sel = QComboBox(self)
        self.dropdown_ite_num = QComboBox(self) 

        # list
        self.model_list = ["----", "2nd Order Taylor Series"]
        self.iteration_list=[str(x) for x in range(1,500)]

         # Adding list of items to combo box
        self.dropdown_model_sel.addItems(self.model_list)
        self.dropdown_ite_num.addItems(self.iteration_list)
        self.dropdown_model_sel.show()
        self.dropdown_ite_num.show()

        for i in range(0,int(self.num_of_var)):
            if i==0:
                self.label_var_boundary.setMaximumWidth(100)

                self.label_max_boundary.setMaximumWidth(105) 
                self.label_min_boundary.setMaximumWidth(105)  
                self.label_var_boundary.setMaximumWidth(105) 
                self.label_max_boundary.setMinimumWidth(105) 
                self.label_var_boundary.setMinimumWidth(105)
                self.label_min_boundary.setMinimumWidth(105)                 
                self.label_model_sel.setMinimumWidth(105)  
                self.label_model_sel.setMaximumWidth(105)  
                self.label_ite_num.setMinimumWidth(105)  
                self.label_ite_num.setMaximumWidth(105)

                self.init_layout.addWidget(self.label_var_boundary,2,0,1,1) 
                self.init_layout.addWidget(self.label_max_boundary,3,0,1,1)
                self.init_layout.addWidget(self.label_min_boundary,4,0,1,1)
                self.init_layout.addWidget(self.label_model_sel,5,0,1,1)
                self.init_layout.addWidget(self.label_ite_num,6,0,1,1)

            self.line_exp_var_list[i*3] = QLineEdit(self)
            self.line_exp_var_list[i*3].setMaximumWidth(100)       
            self.line_exp_var_list[i*3].show()
           
            self.line_exp_var_list[i*3+1] = QLineEdit(self)           
            self.line_exp_var_list[i*3+1].setMaximumWidth(100)
            self.line_exp_var_list[i*3+1].show()

            self.line_exp_var_list[i*3+2] = QLineEdit(self)           
            self.line_exp_var_list[i*3+2].setMaximumWidth(100) 

            self.init_layout.addWidget(self.line_exp_var_list[i*3],2,i+1,1,1)            
            self.init_layout.addWidget(self.line_exp_var_list[i*3+1],3,i+1,1,1)            
            self.init_layout.addWidget(self.line_exp_var_list[i*3+2],4,i+1,1,1)
            
            if i==1:
                self.init_layout.addWidget(self.dropdown_model_sel,5,1,1,2)
                self.init_layout.addWidget(self.dropdown_ite_num,6,1,1,1)
                self.dropdown_ite_num.setMaximumWidth(100)
                self.dropdown_model_sel.setMaximumWidth(100)   
                  

        
        self.button_generate_doe=QtWidgets.QPushButton(self)
        self.button_generate_doe.setText("Generate DoE")
        self.button_generate_doe.setFont(self.font)
        self.button_generate_doe.setStyleSheet("background-color:white;\n"

                                     "border-width:5px;\n")  
        self.init_layout.addWidget(self.button_generate_doe, 2,
                                   self.num_of_var + 1, 3, 3)

        self.button_generate_doe.show()           
        self.button_generate_doe.clicked.connect(self.generate_doe)   
        
    def generate_doe(self):
        """Generate DoE points"""
        self.variables_to_be_displayed = self.line_exp_var_list[0].text()
        self.sample_space_boundry_list={}
        
        self.selected_model = self.dropdown_model_sel.currentText()
        self.num_of_iter = int(self.dropdown_ite_num.currentText())
        for i in range (0,self.num_of_var * 3):
            self.variables_to_be_displayed = self.line_exp_var_list[i].text()
            self.sample_space_boundry_list[i] = self.line_exp_var_list[i].text()

        self.doe_point_generator = DoEPointGenerator()
        self.get_doe_labels = []
        
        self.get_doe_labels, self.det_of_testpoints, self.final_doe_points = \
        self.doe_point_generator.generate_doe_points(
            self.sample_space_boundry_list, self.num_of_row, self.num_of_col, 
            self.selected_model, self.num_of_iter)
        print(self.final_doe_points)

        if self.det_of_testpoints !=0:
            self.print_widget.print_det_results(self)
        
 
        self.sent_doe_points()#self.get_doe_labels, self.final_doe_points, \
                           #  self.test_step_time, self.num_of_row, self.num_of_col)
        self.show()        

    def skip_next_page(self):
        """Sent data to next page"""
        self.table_widget.data_to_next_page(self)

    def make_handle_button(self, button):
        """Skip to next page"""        
        def handle_button():
            if button == "engine test manager":
                self.skip_to("engine test manager")
        return handle_button
