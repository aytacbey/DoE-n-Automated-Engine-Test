# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 10:24:49 2022

@author: kasimoglu
"""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem,  QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QFileDialog, QRadioButton
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QColor

from page_manager import PageManager
from engine_test_automation import EngineTestAutomation


class EngineTestManager(PageManager):
    """All the processes for automated engine test is controlled from here"""
    def __init__(self):
        super().__init__()
        self.project_name = True
        self.pause = False
        self.abort = False
        self.engine_test_object = EngineTestAutomation(EngineTestManager)
        self.init_UI()

    def init_UI(self):
        """Initialize UI"""
        self.setWindowTitle("Test Automation")
        self.font = QFont()
        self.font.setBold(True)    
        # Project info display
        self.project_group_box = QGroupBox("Project")
        self.project_layout = QVBoxLayout()

        # Variable info layout
        self.var_group_box = QGroupBox("Variables")
        self.variable_box_layout = QGridLayout()
        # Experiment layout
        self.exprmnt_group_box = QGroupBox("Experiment")
        self.exprmnt_layout = QGridLayout()   
        
        self.exprmnt_group_box.setLayout(self.exprmnt_layout)
        self.var_group_box.setLayout(self.variable_box_layout)
        self.project_group_box.setLayout(self.project_layout)        
        # Main layout
        self.main_layout = QVBoxLayout()
        # self.main_layout.addStretch(16)
        self.main_layout.addWidget(self.project_group_box)
        self.main_layout.addWidget(self.var_group_box)
        self.main_layout.addWidget(self.exprmnt_group_box)        
        self.setLayout(self.main_layout)


        self.all_project_component = QHBoxLayout(self)
        self.app_sel_layout = QHBoxLayout(self)
        
        
        radio_bttn_ATI = QRadioButton("ATI")
        radio_bttn_ATI.setCheckable(True)    
        radio_bttn_ATI.setFont(self.font)       
        self.app_sel_layout.addWidget(radio_bttn_ATI)
        
        radio_bttn_Inca = QRadioButton("Inca")
        radio_bttn_Inca.setCheckable(False)
        radio_bttn_Inca.setFont(self.font)         
        self.app_sel_layout.addWidget(radio_bttn_Inca)

        self.labels_for_project_info = QVBoxLayout()
        label_app = QLabel("App:    ")
        label_app.setFont(self.font)
        self.labels_for_project_info.addWidget(label_app)

        label_project = QLabel("Project:    ")
        label_project.setFont(self.font)
        self.labels_for_project_info.addWidget(label_project)

        self.get_path_button = QPushButton("Get Path")
        self.get_path_button.setFont(self.font)         

        self.path_n_app_layout = QVBoxLayout() 
        self.path_n_app_layout.addLayout(self.app_sel_layout) 
        
        self.horz_path_layout = QHBoxLayout()
        self.project_path_line = QLineEdit()
        self.horz_path_layout.addWidget(self.project_path_line)
     
        self.horz_path_layout.addWidget(self.get_path_button)
        self.path_n_app_layout.addLayout(self.horz_path_layout)

        
        self.project_path = self.get_path_button.clicked.connect(self.get_path)
        
        self.all_project_component.addLayout(self.labels_for_project_info) 
        self.all_project_component.addLayout(self.path_n_app_layout)
        
        self.project_layout.addLayout(self.all_project_component)

        self.var_on_button = {}

        self.back_button = QtWidgets.QPushButton("Prev", self)        
        self.run_button = QPushButton("Run",self)
        self.pause_button = QPushButton("Pause",self)
        self.record_button = QPushButton("Record",self)
        self.stop_button = QPushButton("Stop",self) 
        self.table_widget_exp = QTableWidget(self)
        self.exprmnt_layout.addWidget(self.table_widget_exp, 0, 0, 1, 5)           
        self.exprmnt_layout.addWidget(self.back_button, 1, 0)
        self.exprmnt_layout.addWidget(self.run_button, 1, 1)        
        self.exprmnt_layout.addWidget(self.pause_button, 1, 2)       
        self.exprmnt_layout.addWidget(self.record_button, 1, 3)
        self.exprmnt_layout.addWidget(self.stop_button, 1, 4)        
      
        self.get_path_button.setFont(self.font)        
        self.get_path_button.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
        self.back_button.setFont(self.font)        
        self.back_button.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")  
        self.run_button.setFont(self.font)        
        self.run_button.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
        self.pause_button.setFont(self.font)        
        self.pause_button.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
        self.record_button.setFont(self.font)        
        self.record_button.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
        self.stop_button.setFont(self.font)        
        self.stop_button.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")         
        
        self.run_button.clicked.connect(self.run_test)
        self.stop_button.clicked.connect(self.abort_test)
        self.pause_button.clicked.connect(self.pause_test)
        self.engine_test_object.eng_tst_chnge_color_sgnl.connect(
            self.change_colour_each_step)
        self.engine_test_object.eng_tst_reset_color_sgnl.connect(
            self.change_colour_before_run)
        self.show()
        self.UI_components()     
        
    @QtCore.pyqtSlot(int)
    def change_colour_each_step(self,i):
        """Change the colour of the respective cell"""
        for k in range(len(EngineTestManager.data_transfer[0])):
            self.table_widget_exp.item(i+1, k).setBackground(
                QColor(50, 205, 50))
    @QtCore.pyqtSlot(str)        
    def change_colour_before_run(self):
        """Turn colour of all cells to white before start"""
        for x in range(len(EngineTestManager.data_transfer)-1):
            for y in range(len(EngineTestManager.data_transfer[0])):
                self.table_widget_exp.item(x+1, y).setBackground(
                    QColor(255, 255, 255))
            
    def get_path(self):
        """Get path of the project file for ATI Vision"""
        self.project_name, not_used = QFileDialog.getOpenFileNames()
        self.project_path_line.setText(self.project_name[0])
        
    def pause_test(self):
        """Resume or pause the test"""
        if self.pause_button.text() == "Pause":
            self.pause_button.setText("Resume")
            self.pause = True
        else:
            self.pause_button.setText("Pause")
            self.pause = False

    def run_test(self):
        """Run the test"""
        if self.project_name == None:
            print("Project file should be selected i.e A2L and Hex \n \
                  For this use get path button")
        else:
            print("It started")
            self.project_name = True
            self.engine_test_object.run(self) #start(self)
    def exprmnt_var_display(self):
        """Display experiment variables"""
        self.test_pnts_from_doe_page = EngineTestManager.data_transfer
        for i in range(len(EngineTestManager.data_transfer[0])):

            self.var_on_button[i] = QPushButton(
                str(str(i+1) + ") " + EngineTestManager.data_transfer[0][i]))
            self.var_on_button[i].setStyleSheet(
                "background-color:rgb(255,200,100);\n""Text-align:left;\n");
            # self.var_on_button[i].setBackGround(QColor(120,0,0))
            # self.back_button.setStyleSheet("background-color:red")            
            self.var_on_button[i].setMaximumWidth(350)
            self.var_on_button[i].setMinimumWidth(100)            
            self.variable_box_layout.addWidget(
                self.var_on_button[i], i%4 , i//4)

        self.variable_box_layout.setColumnStretch(50, 1)

    def go_to_doe_manager(self):
        """Switch to DoE Manager page"""
        for i in range(len(EngineTestManager.data_transfer[0])):
            self.var_on_button[i].deleteLater()        
        self.skip_to("doe manager")

    def UI_components(self):
        """Switch to DoE Manager page"""
        self.back_button.clicked.connect(self.engine_test_pg_wdgt_eraser)
        self.back_button.clicked.connect(self.go_to_doe_manager)    

    def engine_test_pg_wdgt_eraser(self, parent):
        """Removal of widgets in the first page, right now it's obsolete"""
        DoEManager().table_widget.tableMaker.deleteLater()
        #print(parent.delete)
        # parent.m_pages["doe manager"].table_widget.tableMaker.deleteLater()      
    def exprmnt_page_init(self):
        """Row and column structure are copied from the table in doe manager 
        page.
        """
        test_pnts = EngineTestManager.data_transfer
        self.table_widget_exp.setRowCount(len(test_pnts))        
        self.table_widget_exp.setColumnCount(len(test_pnts[0]))

        for i in range(len(test_pnts)):
            for j in range(len(test_pnts[0])):
                self.table_widget_exp.setItem(
                    i, j, QTableWidgetItem(str(test_pnts[i][j])))
                self.table_widget_exp.item(i,j).setBackground(
                    QColor(255, 255, 255))

    def abort_test(self):
        """Abort or pause the test"""
        if self.stop_button.text() == "Stop":
            self.stop_button.setText("Aborted")
            self.abort = True
            print(self.abort)
        else:
            self.stop_button.setText("Stop")
            self.abort = False