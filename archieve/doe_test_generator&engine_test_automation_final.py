# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 12:11:33 2021

@author: akas
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QSpinBox, QMainWindow, QMenu, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QHBoxLayout, QWIDGETSIZE_MAX, QWidget, QPushButton,QLabel,QLineEdit, QComboBox, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtWidgets import QFileDialog, QMessageBox,QStackedWidget,QFormLayout,QRadioButton,QCheckBox,QListWidget,QGroupBox, QGridLayout,QSpacerItem
from PyQt5 import Qt
import csv
import pandas as pd
import sys
import random
import numpy as np
from traceback import print_exception
from win32com.client import Dispatch
import os 
import win32api
import time


class PageManager(QWidget):

    gotoSignal = QtCore.pyqtSignal(str)
    clearCellSignal = QtCore.pyqtSignal(str)
    importCSVSignal= QtCore.pyqtSignal(str)
    exportCSVSignal= QtCore.pyqtSignal(str)
    lockCellSignal= QtCore.pyqtSignal(str)
    unlockCellSignal= QtCore.pyqtSignal(str)
    addColumnSignal= QtCore.pyqtSignal(str)
    removeColumnSignal= QtCore.pyqtSignal(str)
    addRowSignal= QtCore.pyqtSignal(str)
    removeRowSignal= QtCore.pyqtSignal(str)
    doeTransferSignal=QtCore.pyqtSignal(list,list,str,str,int)
        # self.tabloWidget.arrangeTable(self.receiveDoeLabels,self.expActMatrix,self.tDuration, self.nRow, self.nColumn)

    def goto(self, name):
        self.gotoSignal.emit(name)

    def doeMaster(self,receiveDoeLabel,expActMatrix,tDuration, nRow, nColumn):
        print("Doe Transfer PM")
        print(self.receiveDoeLabels)
        #.receiveDoeLabels,self.expActMatrix,self.tDuration, self.nRow, self.nColumn  ,A,B,C,D,E
        self.doeTransferSignal.emit(self.receiveDoeLabels,self.expActMatrix,self.tDuration, self.nRow, self.nColumn)
        
class MasterWindow(QMainWindow):
    # dataReceivedSignal = QtCore.pyqtSignal(list)   
    def __init__(self):
        super(MasterWindow,self).__init__()
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}
        
        self.register(MainWindow(), "main")
        self.register(SecondWindow(), "search")    
        # self.tabloWidget = tableManager()
        # self.returnedtabloWidget = self.tabloWidget.makeTable(self)
        self.sinifdeneme=PageManager()
        self.setGeometry(100, 100, 600, 600)
        
#Initializing signal register
        self.goto("main")      
        self.clearCellsMaster() 
        self.importCsvMaster()
        self.exportCsvMaster()        
        self.lockCellsMaster()
        self.unlockCellsMaster()
        self.addColumnMaster()
        self.removeColumnMaster()
        self.addRowMaster()
        self.removeRowMaster()        
        self.doeTransferMaster()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 900)
        self.setWindowTitle("DoE Point Generator")


########tablo görünümü oluşturuluyor       
        
#####tuşlar oluşturuluyor

        self.Font = QFont()
        self.Font.setBold(True) 
      
##################################################################
     
        # self.b2.clicked.connect(self.arrangeCells)        
        # self.b2.clicked.connect(self.arrangeBoundary)         
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('File')
        self.editMenu = menubar.addMenu('Edit')        
        self.viewMenu = menubar.addMenu('View')
        self.toolMenu = menubar.addMenu('Tools')
        self.helpMenu = menubar.addMenu('Help')
          
########################################
#Menü ve altmenüler oluşturuluyor        
        newAct = QAction('New',self)        
        openAct = QAction('Open',self)        
        saveAct = QAction('Save',self)
        impMenu=QMenu('Import',self)
        

        importAct=QAction('Import to CSV',self)

        impMenu.addAction(importAct)
        quitAct=QAction('Quit',self)
        
        optMenu=QMenu('Options',self)
        optAct=QAction('LAN Settings',self)
        optMenu.addAction(optAct)
        
        aboutMenu=QAction('About',self) 
### etkileşimleri bağla
        importAct.triggered.connect(self.importCsv)
        self.printWidget=printManager()        
        aboutMenu.triggered.connect(self.aboutMethod)
        

        
        self.fileMenu.addAction(newAct)
        self.fileMenu.addAction(openAct)
        self.fileMenu.addAction(saveAct)                   
        self.fileMenu.addMenu(impMenu)
        self.fileMenu.addAction(quitAct)
        
        self.toolMenu.addMenu(optMenu)
        
        self.helpMenu.addAction(aboutMenu)
        quitAct.triggered.connect(self.quitApp) 
      
     
###########################################################
   
    def update(self):
        self.label.adjustSize()
    def aboutMethod(self):
        self.printWidget.aboutInfo(self)
    def arrangeCells(self):
        self.nRow=self.line10.text()
        self.nColumn=self.comboVar.text()
        self.tDuration=self.line11.text()
        self.tabloWidget.dynamicRownColumn(self)
        
        return self.nRow,self.tDuration 
    

    def lockCells(self):
        self.tabloWidget.enableReadOnly(self)

    def unlockCells(self):
        self.tabloWidget.enableReadWrite(self) 
        
        
    def clearCells(self):
        self.tabloWidget.clearCells(self)
    def importCsv(self): 
        self.tabloWidget.importCsv(self)
    def exportCsv(self): 
        self.tabloWidget.exportCsv(self) 
    def addColumn(self):
        self.tabloWidget.addColumn(self)
    def removeColumn(self):
        self.tabloWidget.removeColumn(self)
    def addRow(self):
        self.tabloWidget.addRow(self)
    def removeRow(self):
        self.tabloWidget.removeRow(self)        
    def quitApp(self):
        self.close()

        
 ####################
    def triggerAutoTest(self):
       # self.nStep,self.nVar,self.doeActExpFinal=self.tabloWidget.extraxtData(self)

        self.apiObject=testAutomationAPI()
        self.apiObject.automateTest(self)#self.nStep,self.nVar,self.doeActExpFinal
#### Skipping pages        
    def register(self, widget, name):
        self.m_pages[name] = widget
        # print(self.m_pages)
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageManager):
            widget.gotoSignal.connect(self.goto)
            # print(widget)
            # print(MainWindow())
    @QtCore.pyqtSlot(str)
    def goto(self, name):
        # if name == "search":
        #     print("-")
            # self.m_pages['main'].dataNextPage()
            # self.tabloWidget.dataNextPage(self)
            # self.m_pages["search"].secondPageWidgetInit()
            # self.dataReceivedSignal.emit(self.dataReceived)
        if name in self.m_pages:
            widget = self.m_pages[name]
            if name == "search":
                widget.arrangeVar()
                widget.secondPageWidgetInit()                
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())
            print("Çalışan slot")
##Clear cells signal-slot            
    def clearCellsMaster(self):

        Class=self.m_pages['main']
        Class.clearCellSignal.connect(self.clearCellsSlot)
    @QtCore.pyqtSlot(str)
    def clearCellsSlot(self,isim):
        print("İnşAllah oldu")   
        self.tabloWidget.clearCells(self)
##Import Csv signal-slot            
    def importCsvMaster(self):

        Class=self.m_pages['main']
        Class.importCSVSignal.connect(self.importCsvSlot)
    @QtCore.pyqtSlot(str)
    def importCsvSlot(self,isim):
        print("Import Csv")   
        self.tabloWidget.importCsv(self)   
 
##Export Csv signal-slot            
    def exportCsvMaster(self):

        Class=self.m_pages['main']
        Class.exportCSVSignal.connect(self.exportCsvSlot)
    @QtCore.pyqtSlot(str)
    def exportCsvSlot(self,isim):
  
        self.tabloWidget.exportCsv(self)    
##Lock cells signal-slot            
    def lockCellsMaster(self):

        Class=self.m_pages['main']
        Class.lockCellSignal.connect(self.lockCellsSlot)
    @QtCore.pyqtSlot(str)
    def lockCellsSlot(self,isim):
        print("İnşAllah oldu")   
        self.tabloWidget.enableReadOnly(self)  
##Unlock cells signal-slot            
    def unlockCellsMaster(self):

        Class=self.m_pages['main']
        Class.unlockCellSignal.connect(self.unlockCellsSlot)
    @QtCore.pyqtSlot(str)
    def unlockCellsSlot(self,isim):
        print("İnşAllah oldu")   
        self.tabloWidget.enableReadWrite(self)          
##Add column signal-slot            
    def addColumnMaster(self):

        Class=self.m_pages['main']
        Class.addColumnSignal.connect(self.addColumnSlot)
    @QtCore.pyqtSlot(str)
    def addColumnSlot(self,isim):
        print("İnşAllah oldu")   
        self.tabloWidget.addColumn(self) 
##Remove column signal-slot            
    def removeColumnMaster(self):

        Class=self.m_pages['main']
        Class.removeColumnSignal.connect(self.removeColumnSlot)
    @QtCore.pyqtSlot(str)
    def removeColumnSlot(self,isim):
        print("İnşAllah oldu")   
        self.tabloWidget.removeColumn(self)
##Add row signal-slot            
    def addRowMaster(self):

        Class=self.m_pages['main']
        Class.addRowSignal.connect(self.addRowSlot)
    @QtCore.pyqtSlot(str)
    def addRowSlot(self,isim):
        print("İnşAllah oldu")   
        self.tabloWidget.addRow(self) 
##Remove row signal-slot            
    def removeRowMaster(self):

        Class=self.m_pages['main']
        Class.removeRowSignal.connect(self.removeRowSlot)
    @QtCore.pyqtSlot(str)
    def removeRowSlot(self,isim):
        print("İnşAllah oldu")   
        self.tabloWidget.removeRow(self)
##Doe Transfer signal-slot            
    def doeTransferMaster(self):

        Class=self.m_pages['main']
        Class.doeTransferSignal.connect(self.doeTransferSlot)
    @QtCore.pyqtSlot(list,list,str,str,int)
    def doeTransferSlot(self,a,b,c,d,e):
        Class=self.m_pages['main']
        self.d=d
        self.e=e
        print("Doe transfer")   
        # self.tabloWidget.arrangeTable(self.receiveDoeLabels,self.expActMatrix,self.tDuration, self.nRow, self.nColumn)
        Class.tabloWidget.dynamicRownColumn(self)
        Class.tabloWidget.arrangeTable(a,b,c,d,e)
        # self.tabloWidget.arrangeTable(A,B,C,D,E)        
        print("array transferi gerçekleşti")
        print(b)
class MainWindow(PageManager):    ####

    def __init__(self):
        super().__init__()
      
        self.initUI()
    
    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.Font = QFont()

        self.Font.setBold(True)       

##########Form görünümü oluşturuluyor

        self.formGroupBox = QGroupBox("Project")
        self.initLayout = QGridLayout()
        self.formGroupBox.setLayout(self.initLayout)

##########Variables box layout

        self.innerGroupBox = QGroupBox("Variables")
        self.varboxlayout = QGridLayout()

##########Variables box layout
        self.expGroupBox = QGroupBox("Design")
        self.expboxlayout = QVBoxLayout()  
        self.buttonH1Layout=QHBoxLayout()
        self.buttonH2Layout=QHBoxLayout()
    

        self.expGroupBox.setLayout(self.expboxlayout)
        self.innerGroupBox.setLayout(self.varboxlayout)
        # self.formGroupBox.setLayout(self.initLayout)       
        
########### Ana kutu görünümüne ekleniyor

        self.mainLayout = QVBoxLayout()

        # self.mainLayout.addStretch(16)

        self.mainLayout.addWidget(self.formGroupBox)
        self.mainLayout.addWidget(self.innerGroupBox)
        self.mainLayout.addWidget(self.expGroupBox)       
        self.setLayout(self.mainLayout)
                       

#####tuşlar oluşturuluyor
        self.tabloWidget = tableManager()
        self.returnedtabloWidget = self.tabloWidget.makeTable(self)
        self.btnMaker = buttonManager()
        self.btnMaker.makeTestBtn(self)
        self.printWidget=printManager()
        self.Font = QFont()
        self.Font.setBold(True)

             

##################################################################

#####Sınır koşulları tanımlanıyor
    
#######################################################################
        self.boundaryVar = QtWidgets.QLabel(self)
        self.boundaryMin = QtWidgets.QLabel(self)       
        self.boundaryMax = QtWidgets.QLabel(self)       
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Variables")
        self.label.setFont(self.Font)

        self.setWindowTitle("MainWindow")
        
        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("Steps")
        self.label2.setFont(self.Font)

        self.label3 = QtWidgets.QLabel(self)
        self.label3.setText("Duration")
        self.label3.setFont(self.Font)       
            
        self.comboVar=QComboBox(self)
        self.nVarList=["4"]
        self.comboVar.addItems(self.nVarList)
        
        self.line10 = QLineEdit(self)        
        self.line10.move(200,80)
        self.line10.resize(60, 28)
        self.line11 = QLineEdit(self)        
        self.line11.move(300,80)
        self.line11.resize(60, 28)

        ######### Arranging 1. page, project inputs

        self.label.setMaximumWidth(100)  
        self.comboVar.setMaximumWidth(100) 
        self.label2.setMaximumWidth(100)
        self.line10.setMaximumWidth(100)
        self.label3.setMaximumWidth(100)
        self.line11.setMaximumWidth(100)   
        self.initLayout.addWidget(self.label,0,1,1,1)
        self.initLayout.addWidget(self.label2,0,2,1,1)
        self.initLayout.addWidget(self.label3,0,3,1,1)
        self.initLayout.addWidget(self.comboVar,1,1,1,1)
        self.initLayout.addWidget(self.line10,1,2,1,1)
        self.initLayout.addWidget(self.line11,1,3,1,1)                 

        # self.formlayout.addLayout(self.labelHorizontal)

        self.b2 = QtWidgets.QPushButton(self)

        self.b2.setText("Submit")

        self.b2.setFont(self.Font)
        self.b2.setMaximumWidth(100) 
        # self.b2.move(400,80)
        self.initLayout.addWidget(self.b2,1,4,1,3)
        self.b2.setStyleSheet("background-color:white;\n"

                                      "border-width:5px;\n")       
        # self.labelHorizontal.addStretch()
        # self.labelHorizontal.insertSpacing(10, 150)
        # self.labelHorizontal.insertStretch(-1000, 1) 
        # self.labelHorizontal.setAlignment(QtCore.Qt.AlignTop)

        self.b2.clicked.connect(self.arrangeCells)       

        self.b2.clicked.connect(self.arrangeBoundary)     
        # self.searchButton = QtWidgets.QPushButton("Ara", self)

        # self.searchButton.clicked.connect(self.make_handleButton("searchButton")) 

    def update(self):

        self.label.adjustSize()

    def aboutMethod(self):

        self.printWidget.aboutInfo(self)

    def arrangeCells(self):

        self.nRow=self.line10.text()
        self.nColumn=int(self.comboVar.currentText())
        self.tDuration=self.line11.text()
        # self.tabloWidget.dynamicRownColumn(self)      
        return self.nRow,self.tDuration

    def lockCells(self):
        self.tabloWidget.enableReadOnly(self)      
        # self.lockCellSignal.emit("Lock cells")
    def unlockCells(self):
        self.tabloWidget.enableReadWrite(self)
        # self.unlockCellSignal.emit("Unlock cells")      

    def clearCells(self):

        self.tabloWidget.clearCells(self)        
        # self.clearCellSignal.emit("clearall")
        print("clear celldeyiz")
      #  self.tabloWidget.clearCells(self)
    def importCsv(self):
        self.tabloWidget.importCsv(self)  
        # self.importCSVSignal.emit("import csv")
        print("MW import csv")
    def exportCsv(self):
        self.tabloWidget.exportCsv(self) 
        # self.exportCSVSignal.emit("export csv")
    def addColumn(self):
        self.tabloWidget.addColumn(self)
        # self.addColumnSignal.emit("Add col")
    def removeColumn(self):
        self.tabloWidget.removeColumn(self)
        # self.removeColumnSignal.emit("Remove col")
    def addRow(self):
        self.tabloWidget.addRow(self)
        # self.addRowSignal.emit("Add row")
    def removeRow(self):
        self.tabloWidget.removeRow(self)
        # self.removeRowSignal.emit("Remove row")      
    def quitApp(self):

        self.close()
    def arrangeBoundary(self):
        # self.Font = QFont()
        # self.Font.setBold(True)

        self.lineHorizontal=QHBoxLayout()
        self.nVariable=int(self.comboVar.currentText())

        self.boundaryWidget = tableManager()
        # self.returnedBoundaryWidget = self.boundaryWidget.makeTable(self)  


        self.boundaryVar.setText("Var:")
        self.boundaryVar.setFont(self.Font)

     
        self.boundaryMax.setText("Min:")
        self.boundaryMax.setFont(self.Font)       

 
        self.boundaryMin.setText('Max:')
        self.boundaryMin.setFont(self.Font)       

       
        self.modelSelection=QtWidgets.QLabel(self)
        self.modelSelection.setText('Model Selection:')
        self.modelSelection.setFont(self.Font)

        self.modelSelection.show()
 
        self.iterationNo=QtWidgets.QLabel(self)
        self.iterationNo.setText('Iteration No:')
        self.iterationNo.setFont(self.Font)        

        self.iterationNo.show()       
   
        self.varList={}           
        self.lineVertical={}
                # creating a combo box widget

        self.combo_box = QComboBox(self)
        self.iterationBox = QComboBox(self) 

        # list

        self.modelList = ["----", "2nd Order Taylor Series"]
        self.iterationList=list(range(1,50))
        self.iterationList=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17",

                            "18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34",

                            "35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","60","70","80","90","100",
                            "110","120","130","140","150","160","170","180","190","200","210","220","230","240","250","260","270","280","290","300",
                            "310","320","330","340","350","360","370","380","390","400","410","420","430","440","450","460","470","480","490","500"]

         # adding list of items to combo box
        self.combo_box.addItems(self.modelList)
        self.iterationBox.addItems(self.iterationList)
        self.combo_box.show()
        self.iterationBox.show()
##İstenen değişken sayısı kadar modelin min ve max noktaları isteniyor
        # self.formlayout.addStretch()
        for i in range(0,int(self.nVariable)):
            if i==0:
                self.boundaryVar.setMaximumWidth(100)

                self.boundaryMax.setMaximumWidth(105) 
                self.boundaryMin.setMaximumWidth(105)  
                self.boundaryVar.setMaximumWidth(105) 
                self.boundaryMax.setMinimumWidth(105) 
                self.boundaryVar.setMinimumWidth(105)
                self.boundaryMin.setMinimumWidth(105)                 
                self.modelSelection.setMinimumWidth(105)  
                self.modelSelection.setMaximumWidth(105)  
                self.iterationNo.setMinimumWidth(105)  
                self.iterationNo.setMaximumWidth(105)  
               

                self.initLayout.addWidget(self.boundaryVar,2,0,1,1) 
                self.initLayout.addWidget(self.boundaryMax,3,0,1,1)
                self.initLayout.addWidget(self.boundaryMin,4,0,1,1)
                self.initLayout.addWidget(self.modelSelection,5,0,1,1)
                self.initLayout.addWidget(self.iterationNo,6,0,1,1)                
                # self.lineVertical[i].setAlignment(QtCore.Qt.AlignTop)
                # self.lineHorizontal.addStretch()

                
            print("sınır koşulları giriliyor")


            self.varList[i*3]=QLineEdit(self)
            self.varList[i*3].setMaximumWidth(100)       
            self.varList[i*3].show()
           
            self.varList[i*3+1]=QLineEdit(self)           
            self.varList[i*3+1].setMaximumWidth(100)
            self.varList[i*3+1].show()

           

            self.varList[i*3+2]=QLineEdit(self)           
            self.varList[i*3+2].setMaximumWidth(100) 

            self.initLayout.addWidget(self.varList[i*3],2,i+1,1,1)            
            self.initLayout.addWidget(self.varList[i*3+1],3,i+1,1,1)            
            self.initLayout.addWidget(self.varList[i*3+2],4,i+1,1,1)
            
            if i==1:
                self.initLayout.addWidget(self.combo_box,5,1,1,2)
                self.initLayout.addWidget(self.iterationBox,6,1,1,1)
                self.iterationBox.setMaximumWidth(100)
                self.combo_box.setMaximumWidth(100)   
                  

        
        self.submitBoundary=QtWidgets.QPushButton(self)
        self.submitBoundary.setText("Generate DoE")
        self.submitBoundary.setFont(self.Font)
        self.submitBoundary.setStyleSheet("background-color:white;\n"

                                     "border-width:5px;\n")  
        self.initLayout.addWidget(self.submitBoundary,2,self.nVariable+1,3,3)
        # self.lineVertical[self.nVariable+1].setAlignment(QtCore.Qt.AlignTop)

        # self.formlayout.addStretch()   
        
        self.submitBoundary.show()           
        self.submitBoundary.clicked.connect(self.sbmitBoundary)   
        
    def sbmitBoundary(self,deneme):
        self.Display=self.varList[0].text()
        # print(self.tDuration)
        self.boundryList={}
        
        self.modelExperiment=self.combo_box.currentText()
        self.iterationNumber=int(self.iterationBox.currentText())
        for i in range (0,self.nVariable*3):
            self.Display=self.varList[i].text()
            self.boundryList[i]=self.varList[i].text()
            print(self.Display)

        self.boundaryExport=doePointGenerator()
        self.receiveDoeLabels = []
    #    self.m=0


        
        self.receiveDoeLabels,self.receiveDoePoints, self.detVal, self.expActMatrix = self.boundaryExport.boundaryImport(self.boundryList,self.nRow,self.nColumn,self.modelExperiment,self.iterationNumber)
        print(self.expActMatrix)

        if self.detVal !=0:
            print("DoePointGenerator, tableManager ve MyWindow'sırayla dönüldü")

            self.printWidget.toBePrinted(self)
        
        # self.tabloWidget.arrangeTable(self.receiveDoeLabels,self.expActMatrix,self.tDuration, self.nRow, self.nColumn)
        self.doeMaster(self.receiveDoeLabels,self.expActMatrix,self.tDuration, self.nRow, self.nColumn)
        # self.searchButton.setGeometry(150, 150, 100, 20)
        self.show()        
        print()
    def skipNextPage(self):
        self.tabloWidget.dataNextPage(self)

    def make_handleButton(self, button):
        
        def handleButton():
            if button == "searchButton":
                self.goto("search")
        return handleButton


class SecondWindow(PageManager):
    pauseThread=Qt.pyqtSignal(str)        
    def __init__(self):
        super().__init__()
        SecondWindow.ProjectName=True
        SecondWindow.pause=False
        SecondWindow.abort=False
        self.autoTest=testAutomationAPI()
        print("print")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Test Automation")
        self.Font = QFont()
        self.Font.setBold(True)        
##########Form görünümü oluşturuluyor
        self.formGroupBox = QGroupBox("Project")
        self.formlayout = QVBoxLayout()
        self.formGroupBox.setLayout(self.formlayout)
##########Variables box layout
        self.innerGroupBox = QGroupBox("Variables")
        self.varboxlayout = QGridLayout()
##########Variables box layout
        self.expGroupBox = QGroupBox("Experiment")
        self.exprunlayout = QGridLayout()   
        
        self.expGroupBox.setLayout(self.exprunlayout)
        self.innerGroupBox.setLayout(self.varboxlayout)
        self.formGroupBox.setLayout(self.formlayout)        
########### Ana kutu görünümüne ekleniyor
        self.mainLayout = QVBoxLayout()
        # self.mainLayout.addStretch(16)
        self.mainLayout.addWidget(self.formGroupBox)
        self.mainLayout.addWidget(self.innerGroupBox)
        self.mainLayout.addWidget(self.expGroupBox)        
        self.setLayout(self.mainLayout)



        self.finalView=QHBoxLayout(self)
        self.apiSW = QHBoxLayout(self)
        
        
        atiView=QRadioButton("ATI")
        atiView.setCheckable(True) 
   
        atiView.setFont(self.Font)
       
        self.apiSW.addWidget(atiView)
        incaView=QRadioButton("Inca")
        incaView.setCheckable(False)
        incaView.setFont(self.Font)         
        self.apiSW.addWidget(incaView)

        
        
        self.vText=QVBoxLayout()
        
        appView=QLabel("App:    ")
        appView.setFont(self.Font)
        self.vText.addWidget(appView)

        textView=QLabel("Project:    ")
        textView.setFont(self.Font)       
        self.vText.addWidget(textView)



        self.qpushbutton=QPushButton("Get Path")
        self.qpushbutton.setFont(self.Font)         
       
        self.projectVertical=QVBoxLayout() 
        self.projectVertical.addLayout(self.apiSW) 
        
        self.projectButton=QHBoxLayout()
        self.projectPath=QLineEdit()
        self.projectButton.addWidget(self.projectPath)
     
        self.projectButton.addWidget(self.qpushbutton)  
        
        self.projectVertical.addLayout(self.projectButton)

          

        self.importedProject=self.qpushbutton.clicked.connect(self.getPath)
        
        self.finalView.addLayout(self.vText) 
        self.finalView.addLayout(self.projectVertical)
        
        self.formlayout.addLayout(self.finalView)
        # self.exprunlayout.addStretch()        
        self.varText={}
        self.varCombo={}
        self.varButton={}
        self.varButtonComboHorizontal=QHBoxLayout()
        self.varRowtoRowVer=QVBoxLayout()
        self.finalVerticalLayout=QVBoxLayout()
        self.backButton = QtWidgets.QPushButton("Prev", self)        
        self.runButton = QPushButton("Run",self)
        self.pauseButton = QPushButton("Pause",self)
        self.recordButton = QPushButton("Record",self)
        self.stopButton = QPushButton("Stop",self) 
        self.tableWidget=QTableWidget(self)
        self.exprunlayout.addWidget(self.tableWidget,0,0,1,5)           
        self.exprunlayout.addWidget(self.backButton,1,0)
        self.exprunlayout.addWidget(self.runButton,1,1)        
        self.exprunlayout.addWidget(self.pauseButton,1,2)       
        self.exprunlayout.addWidget(self.recordButton,1,3)
        self.exprunlayout.addWidget(self.stopButton,1,4)        
      
        self.qpushbutton.setFont(self.Font)        
        self.qpushbutton.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
        self.backButton.setFont(self.Font)        
        self.backButton.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")  
        self.runButton.setFont(self.Font)        
        self.runButton.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
        self.pauseButton.setFont(self.Font)        
        self.pauseButton.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
        self.recordButton.setFont(self.Font)        
        self.recordButton.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
        self.stopButton.setFont(self.Font)        
        self.stopButton.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")         
        # self.importedProject=1
        self.runButton.clicked.connect(self.exportProject)
        self.stopButton.clicked.connect(self.abortTest)
        self.pauseButton.clicked.connect(self.pauseTest)
        self.autoTest.threadApiSignal.connect(self.changeColour)
        self.autoTest.threadRestartTest.connect(self.changeColourBeforeRun)
        self.show()
        self.UiComponents()     
        
    @QtCore.pyqtSlot(int)
    def changeColour(self,i):
        for k in range(len(SecondWindow.dataTransfer[0])):
            self.tableWidget.item(i+1,k).setBackground(QColor(50,205,50))
    @QtCore.pyqtSlot(str)        
    def changeColourBeforeRun(self):
        for x in range(len(SecondWindow.dataTransfer)-1):
            for y in range(len(SecondWindow.dataTransfer[0])):
                self.tableWidget.item(x+1,y).setBackground(QColor(255,255,255))
            
    def getPath(self):
        
        SecondWindow.ProjectName, NotUsed = QFileDialog.getOpenFileNames()
        self.projectPath.setText(SecondWindow.ProjectName[0])
    def pauseTest(self):
        
        print("pause kısmı aktif")
        
        if self.pauseButton.text() == "Pause":
            self.pauseButton.setText("Resume")
            SecondWindow.pause= True
        else:
            self.pauseButton.setText("Pause")
            SecondWindow.pause= False
        
        # self.pauseThread.emit("dur")
    def exportProject(self):
        
        if SecondWindow.ProjectName==None:
            print("Proje dosyası seçilmek zorunda \nBunun için yukardaki tuşu kullanın")
        else:
            print("Başlıyor")
            self.autoTest.start()
    def arrangeVar(self):
        print("arrangeVar içindeyiz")
        # print(SecondWindow.dataTransfer) 
        self.varHorLayout={}

        
        for i in range(len(SecondWindow.dataTransfer[0])):

            self.varButton[i]=QPushButton(str(str(i+1)+") "+SecondWindow.dataTransfer[0][i]))
            self.varButton[i].setStyleSheet("background-color:rgb(255,200,100);\n""Text-align:left;\n");
            # self.varButton[i].setBackGround(QColor(120,0,0))
            # self.backButton.setStyleSheet("background-color:red")            
            self.varButton[i].setMaximumWidth(350)
            self.varButton[i].setMinimumWidth(100)            
            self.varboxlayout.addWidget(self.varButton[i], i%4,i//4)

        self.varboxlayout.setColumnStretch(50,1)
 


    # def printem(self):
    #     print("qpushbutton deneme")
    def goToMain(self):

        # print(SecondWindow.dataTransfer)
        for i in range(len(SecondWindow.dataTransfer[0])): 
            # self.varText[i].deleteLater()
            # self.varCombo[i].deleteLater()
            self.varButton[i].deleteLater()        
        self.goto("main")

    def UiComponents(self):
        
        print("2. pencere")          

         
        # self.backButton.setGeometry(QtCore.QRect(100, 700, 100, 20))
        self.backButton.clicked.connect(self.secondPageWidgetEraser)
        self.backButton.clicked.connect(self.goToMain)            
    def secondPageWidgetEraser(self):
        print("widget silme, 2. sayfa *****")

        MainWindow().tabloWidget.tableMaker.deleteLater()
    def secondPageWidgetInit(self):
        # print("2. sayfanın içinde ----",SecondWindow.dataTransfer)
        self.tableWidget.setRowCount(len(SecondWindow.dataTransfer))
        
        self.tableWidget.setColumnCount(len(SecondWindow.dataTransfer[0]))
      
        # MainWindow().tabloWidget.tableMaker.setItem(0,0, QTableWidgetItem(str(10)))
        for i in range(len(SecondWindow.dataTransfer)):
            # print("data matrisi",len(SecondWindow.dataTransfer))
            for j in range(len(SecondWindow.dataTransfer[0])):
                self.tableWidget.setItem(i,j, QTableWidgetItem(str(SecondWindow.dataTransfer[i][j])))
                self.tableWidget.item(i,j).setBackground(QColor(255,255,255))

        
                          
    def abortTest(self):
        print("Abort testteyiz")
        if self.stopButton.text() == "Stop":
            self.stopButton.setText("Aborted")
            SecondWindow.abort=True
            print("True-abort test")
            print(SecondWindow.abort)
        else:
            self.stopButton.setText("Stop")
            SecondWindow.abort =False

                 

        
        
class testAutomationAPI(QThread):
   
    threadApiSignal=Qt.pyqtSignal(int)
    threadRestartTest=Qt.pyqtSignal(str)
    def __init__(self):
        super().__init__()        
        self.wShell = Dispatch("WScript.Shell")
      

    def importProject(self,parent):

        # self.ProjectName, NotUsed = QFileDialog.getOpenFileNames()

        # with open(ProjectName[0], "rt")as f:         

            # data = csv.reader(f)
        print("Proje import ekranında")        
#Create a windows shell object
        self.wShell = Dispatch("WScript.Shell")
          
        self.ret =self.wShell.Popup("This script can run with the VISION GUI visible, or can run with VISION running invisible in the background. If you want to see the VISION GUI, then be sure VISION is launched before clicking OK to run this script. Otherwise, just click OK to run it. \n \n To exit this script, click Cancel.",0,"AddScreenControls",65)
        if self.ret==2:
            exit()          

#Launch the XCP simulator from the VISION install folder (used for demo purposes)
# VisionApp = Dispatch("Vision.ApplicationInterface")
        print("vision app giriş ",parent.ProjectName)

# os.startfile(VisionApp.Path + "\XcpIpSim.exe")
# VisionApp = None


        
        return self.ProjectName
    
    def run(self):
        self.runAutoTest(self)
    @pyqtSlot(str)    
    def runAutoTest(self,parent):#,nStep,nVar  
        import time
#Create the project object
        # time.sleep(2)



        if SecondWindow.ProjectName== None:
            print("You must select project file",SecondWindow.ProjectName)

        else:
            print("Proje dosyası taşındı",SecondWindow.ProjectName)
        self.Project = Dispatch("Vision.ProjectInterface") 

        

        # self.recorder=Dispatch("Vision.RecorderFile")
        # self.recObject=Dispatch("VisionProjectComponent")

        # self.recorder= Dispatch("Vision.DeviceInterface")
       

#Open the virtual XCP project (relative to the script location)

        ################################################################3
        # Project.Open (r"C:\Users\akas\Documents\TTZAM1,5\ApiDeneme.vpj")
        # self.Project.Open(r"C:\Users\akas\Documents\TTZAM1,5\ApiDeneme.vpj")
        #####################################################################3
        
#Go Online
        self.Project.Online = True

        
#Create an interface to device "PCM"
        Device = self.Project.FindDevice("PCM")
        
        # for i in range(10):
        #     print(Device.Strategies.Item(i)) 
  
        print("strateji")
        # time.sleep(10)
        # print(Device.ActiveStrategy)
        # print("downloaded")
        # time.sleep(10000)
        # self.screenU=self.Project.Screens
        
        # for i in range(10):
        # time.sleep(10)    
        # print(str(self.screenU.Item(1)))
        # print(self.screenU.Count)        
        # # print(self.screenU[1])
        # print(len(self.screenU))
        # self.Screen=self.Project.ScreenOpen(self.screenU.Item(1))
        # self.Recorder=self.Screen.FindControl("Recorder")
        # print(self.Screen)
        # print(self.Recorder)
        # self.Recorder.Start()        
        # time.sleep(10000)
        # print(Device)
        # print(Screens)
        # Screens.Start()        
#Download active strategy to the ecu
        # time.sleep(10)
############# Downloading the active strategy is not activated due to lack of info      
        # Device.DownloadActiveStrategy()
#############        
        # time.sleep(100)
        # time.sleep(10000)
        # recorder=Device.start()
#Trigger the recording object        

#An option for adding labels is trying step by step approach. In each step related label is added as map and checked, if object is none
#then process goes on till being added as scalar.  
        
        self.getCalProperties={}
        self.getLabelType=[]
        p=0
        eRow=0
        if p==0:
            for i in range(len(SecondWindow.dataTransfer[0])-1):
                if i==0 and SecondWindow.dataTransfer[0][0]=="Step":
                    print("Step eklenmiş")
                    eRow=1
                else:
                    print((SecondWindow.dataTransfer[0][i]))
                    self.getCalProperties[i-eRow]=Device.FindTable3D(SecondWindow.dataTransfer[0][i])
                    if self.getCalProperties[i-eRow]==None:
                        print("Doğru yol")                        
                        self.getCalProperties[i-eRow]=Device.FindTable2D(SecondWindow.dataTransfer[0][i])
                        if self.getCalProperties[i-eRow]==None:
                            self.getCalProperties[i-eRow]=Device.FindScalar(SecondWindow.dataTransfer[0][i])
                            print("skalar eklendi")
                            if self.getCalProperties[i-eRow]==None:
                                print("You have entered a wrong label")
                                self.getLabelType.append("None")
                            else: 
                                print(self.getCalProperties[i-eRow].Type)
                                self.getLabelType.append("Calibratable")
                        else:
                            self.getLabelType.append("Curve")
                            print(self.getCalProperties[i-eRow].Type)
                    else:
                        self.getLabelType.append("Map")
                        print(self.getCalProperties[i-eRow].Type)
                        
 
#Another option is adding labels according to label name. For Liebherr and Bosch suffix "_C" means calibratable, "_CUR" means curve and "_MAP" means map.       
                         
        elif p==1:
            for i in range(len(SecondWindow.dataTransfer[0])):
                print(len(SecondWindow.dataTransfer[0][i]))
            for i in range(len(SecondWindow.dataTransfer[0])-1):
                if i==0 and SecondWindow.dataTransfer[0][0]=="Step":
                    print("Ctrl+Alt+Del")
                    eRow=1
                else:
                    print(len(SecondWindow.dataTransfer[0][0]))
                    if SecondWindow.dataTransfer[0][i][len(SecondWindow.dataTransfer[0][i])-1]=="C":
                        self.getCalProperties[i-eRow]=Device.FindScalar(SecondWindow.dataTransfer[0][i])
                        print(i,". scalar değişken eklendi")
                    elif SecondWindow.dataTransfer[0][i][len(SecondWindow.dataTransfer[0][i])-1]=="R":
                        print(i,". curve değişken eklendi")
                        self.getCalProperties[i-eRow]=Device.FindTable2D(SecondWindow.dataTransfer[0][i])
                    elif SecondWindow.dataTransfer[0][i][len(SecondWindow.dataTransfer[0][i])-1]=="P":
                        print(i,". map değişken eklendi")
                        self.getCalProperties[i-eRow]=Device.FindTable3D(SecondWindow.dataTransfer[0][i])                    
                 

     

#Test starts here. 
        
        self.threadRestartTest.emit("change colour")
        for i in range(len(SecondWindow.dataTransfer)-1):
            if SecondWindow.abort==True:
                break
                print(SecondWindow.abort,"test iptali, pause") 
            for j in range(len(self.getCalProperties)):
                if self.getLabelType[j]=="Calibratable":
                    self.getCalProperties[j].TargetValue=float(SecondWindow.dataTransfer[i+1][j+eRow])
                elif self.getLabelType[j]=="Curve":
                    curve=[]
                    for d in range(len(self.getCalProperties[j].YaxisActualValues)):
                        curve.append(float(SecondWindow.dataTransfer[i+1][j+eRow]))
                    self.getCalProperties[j].YAxisTargetValues=curve
                    curve=0
                elif self.getLabelType[j]=="Map":
                    dummyMap=[]
                    for m in range(len(self.getCalProperties[j].ZaxisActualValues)):
                        dummyMap.append([])
                        for n in range(len(self.getCalProperties[j].ZaxisActualValues[0])):
                            dummyMap[m].append(float(SecondWindow.dataTransfer[i+1][j+eRow]))
                    print(dummyMap)        
                    self.getCalProperties[j].ZAxisTargetValues=dummyMap
                    dummyMap=0
                    
            print(SecondWindow.dataTransfer[i+1][len(SecondWindow.dataTransfer[0])-1])
            self.threadApiSignal.emit(i)
            # time.sleep(1)
            t=0

            while t<float(SecondWindow.dataTransfer[i+1][len(SecondWindow.dataTransfer[0])-1]):
                time.sleep(0.2)
                print(t)
                if SecondWindow.abort==True:
                    break
                    print(SecondWindow.abort,"test iptali, pause") 
                while SecondWindow.pause==True:
                    time.sleep(1)
                    print(SecondWindow.abort)
                    
                    if SecondWindow.abort==True:
                        break
                        print(SecondWindow.abort,"test iptali, pause")                     
                    print("duruyor")
                t+=0.2                    
            

        SecondWindow.pause= False
#Release the objects
        print("test bitirildi")
        Device = None

        Calibration = None
        Project = None    


#####################
        
class buttonManager(QWidget):
    def __init__(self):
        super().__init__()

    def makeTestBtn(self, parent):
        self.Font = QFont()
        self.Font.setBold(True)
        # self.layOutVer=Qt.QVBoxLayout(parent)
        self.testBtn01 = QPushButton("Import CSV", parent)
        self.testBtn02 = Qt.QPushButton("Export CSV", parent)
        self.testBtn03 = Qt.QPushButton("Lock Cells", parent)
        self.testBtn04 = Qt.QPushButton("Unlock Cells", parent)
        self.testBtn05 = Qt.QPushButton("Clear Cells", parent)
        self.testBtn06 = Qt.QPushButton("Add Col", parent)
        self.testBtn07 = QPushButton("Remove Col", parent)
        self.testBtn08 = QPushButton("Add Row", parent)
        self.testBtn09 = QPushButton("Remove Row", parent)
        

        self.testBtn01.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.testBtn02.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.testBtn03.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.testBtn04.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.testBtn05.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")  
        self.testBtn06.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.testBtn07.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.testBtn08.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")
        self.testBtn09.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n")        
        self.testBtn01.setFont(self.Font) 
        self.testBtn02.setFont(self.Font)  
        self.testBtn03.setFont(self.Font)  
        self.testBtn04.setFont(self.Font)
        self.testBtn05.setFont(self.Font)
        self.testBtn06.setFont(self.Font) 
        self.testBtn07.setFont(self.Font)  
        self.testBtn08.setFont(self.Font)  
        self.testBtn09.setFont(self.Font)

######Reset düğmesi        
        self.b1 = QtWidgets.QPushButton(parent)
        self.b1.setText("Next")

        parent.buttonH1Layout.addWidget(self.testBtn01)        
        parent.buttonH1Layout.addWidget(self.testBtn02)
        parent.buttonH1Layout.addWidget(self.testBtn03)
        parent.buttonH1Layout.addWidget(self.testBtn04)
        parent.buttonH1Layout.addWidget(self.testBtn05) 
        parent.buttonH2Layout.addWidget(self.testBtn06)        
        parent.buttonH2Layout.addWidget(self.testBtn07)
        parent.buttonH2Layout.addWidget(self.testBtn08)
        parent.buttonH2Layout.addWidget(self.testBtn09)
        parent.buttonH2Layout.addWidget(self.b1)  
        parent.expboxlayout.addLayout(parent.buttonH1Layout)
        parent.expboxlayout.addLayout(parent.buttonH2Layout)
        # self.b1.move(580,800)
        # self.b1.clicked.connect(parent.clearCells)
        self.b1.setFont(self.Font)
        self.b1.setStyleSheet("background-color:white;\n"
                                     "border-width:5px;\n") 
   

         
        self.testBtn01.clicked.connect(parent.importCsv) 
        self.testBtn02.clicked.connect(parent.exportCsv) 
        self.testBtn03.clicked.connect(parent.lockCells)
        self.testBtn04.clicked.connect(parent.unlockCells)        
        self.testBtn05.clicked.connect(parent.clearCells)
        self.testBtn06.clicked.connect(parent.addColumn)
        self.testBtn07.clicked.connect(parent.removeColumn)           
        self.testBtn08.clicked.connect(parent.addRow)
        self.testBtn09.clicked.connect(parent.removeRow)
        self.b1.clicked.connect(parent.skipNextPage)
        
        self.b1.clicked.connect(parent.make_handleButton("searchButton")) 
##############################################################################        
        
class tableManager(QWidget):
    
    def __init__(self):

        super().__init__() 

    def secondPageWidgetEraser(self,parent):
        print("")
        # print("explayout kaç elemana sahip",parent.exprunlayout.count())
        # # parent.exprunlayout.removeWidget()   
        # MainWindow().tabloWidget.tableMaker.setParent(None)
    def secondPageWidget(self,parent):

        print("explayout kaç elemana sahip",parent.exprunlayout.count())  
        print(" ---- secondPageWidget ------",len(SecondWindow.dataTransfer))
        for i in range(len(SecondWindow.dataTransfer)):

            for j in range(len(SecondWindow.dataTransfer[0])):
                MainWindow().tabloWidget.tableMaker.setItem(i,j, QTableWidgetItem(str("asv")))


    
        parent.exprunlayout.setAlignment(QtCore.Qt.AlignTop)
    def makeTable(self, parent):
        self.tableMaker = QTableWidget(parent)
        self.tableMaker.setRowCount(21)
        self.tableMaker.setColumnCount(7)
        # self.tableMaker.setColumnWidth(0, 50)
    
        self.doeimport=doePointGenerator()
        self.doeLabelImport=doePointGenerator()
        self.doeLabel=self.doeLabelImport.doeLabelTransferGUI(self)
        self.doeTestNoktasi=self.doeimport.doeTransferGUI()

        for j in range(0,len(self.doeLabel)):
            if j==0:
                self.tableMaker.setItem(0,0, QTableWidgetItem("Step"))    
            self.tableMaker.setItem(0,j+1, QTableWidgetItem(str(self.doeLabel[j])))            


        parent.varboxlayout.addWidget(self.tableMaker,0,0,1,2)
        self.tableMaker.setMaximumHeight(500)
        return self.tableMaker
    def dynamicRownColumn(self,parent):
        self.tableMaker.setRowCount(int(parent.d)+1)
        self.tableMaker.setColumnCount(int(parent.e)+2)
        return self.tableMaker
    def arrangeTable(self,doeLabelFinal,doePointFinal,duration,Row, Column):


#### Adım sayısı, süre, sinyaller ve test noktalarının bütünleşik matrisi oluşturulur        
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
                self.tableMaker.setItem(i,j, QTableWidgetItem(str(self.doeActMatrixFinal[i][j])))
        return self.tableMaker
    def enableReadOnly(self,parent):
        print("okuma modu")

        self.tableMaker.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers) 
    def enableReadWrite(self,parent):     

        self.tableMaker.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)       
        print("yazma fonk")
     #   self.tableMaker.setEnabled(1)
    def clearCells(self,parent):
        nVar=self.tableMaker.columnCount()
        nStep=self.tableMaker.rowCount()
        for i in range(nStep): 
            for j in range(int(nVar)):
                self.tableMaker.setItem(i,j, QTableWidgetItem(str(''))) 
                
    def addColumn(self,parent):
        nCol=self.tableMaker.columnCount()
        self.tableMaker.setColumnCount(nCol+1)
    def removeColumn(self,parent):
        nCol=self.tableMaker.columnCount()
        self.tableMaker.setColumnCount(nCol-1)
    def addRow(self,parent):
        nRow=self.tableMaker.rowCount()
        self.tableMaker.setRowCount(nRow+1)
    def removeRow(self,parent):
        nRow=self.tableMaker.rowCount()
        self.tableMaker.setRowCount(nRow-1)
            
    def importCsv(self,parent):
      
        FileData, NotUsed = QFileDialog.getOpenFileNames(self)

        with open(FileData[0], "rt")as f:         

            data = csv.reader(f)
 
            nVar=0
            nStep=0
            self.importedCsv=[]
            for row in data:
                nStep+=1
                self.importedCsv.append([])
                for j in range(len(row)):
                    self.importedCsv[nStep-1].append(row[j])

                 
            nVar=len(row)
            # print(nStep)
            # print(nVar)
            # print(self.importedCsv)
            self.tableMaker.setRowCount(nStep)
            self.tableMaker.setColumnCount(nVar)            
           
            for i in range(nStep): 
                for j in range(nVar):
                    self.tableMaker.setItem(i,j, QTableWidgetItem(str(self.importedCsv[i][j])))            
    def exportCsv(self,parent):
        column=self.tableMaker.columnCount()
        row=self.tableMaker.rowCount()
        exportCsv=[]
        print(row,column)
        for i in range(row): 
            exportCsv.append([])
            for j in range(column):
                a=self.tableMaker.item(i,j)
                if a==None:
                    a=0
                else:
                    a=self.tableMaker.item(i,j).text()
                exportCsv[i].append(a)
        # print(exportCsv)
        export=QFileDialog.getSaveFileName()
        with open(str(export[0]+".csv"), mode='w',newline='') as experiment_list:            
            experimentList = csv.writer(experiment_list, delimiter=',', quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
            experimentList.writerows(exportCsv)             
    def dataNextPage(self,parent):
        SecondWindow.dataTransfer=[]           
        column=self.tableMaker.columnCount()
        row=self.tableMaker.rowCount()

        # SecondWindow.dataTransfer=[]
        # print(row,column)

        subCol=0
        subRow=0
        for i in range(row):

            for j in range(column):
                a=self.tableMaker.item(i,j)
                if a==None and i==0:
                    subCol+=1
                elif a==None and j==0:
                    subRow+=1
        column=column-subCol
        row=row-subRow            
        for i in range(row):

            SecondWindow.dataTransfer.append([])
            for j in range(column):
                a=self.tableMaker.item(i,j)
                if a==None:
                    a=0
                else:
                    a=self.tableMaker.item(i,j).text()
                SecondWindow.dataTransfer[i].append(a)
        
        return SecondWindow.dataTransfer            
#######################################################################################################################

class printManager(QWidget):
    def __init__(self):
        super().__init__()
    def toBePrinted(self,parent):
        self.detOutput = QTextEdit(parent)
        self.detPrnt=int(len(parent.detVal))/2
        toPrint=[]
        for i in range(parent.iterationNumber):
            printVal=str(i+1)+". iteration determinant value is "+str(round(parent.detVal[2*i+1],3))
            # self.detOutput.append(str(i+1))
            # self.detOutput.append(". denemenin determinantı")
            # self.detOutput.append(str(parent.detVal[2*i+1])))
          

            self.detOutput.append(printVal)
    
        max_value=max(parent.detVal)
        maxIndex=parent.detVal.index(max_value)
        self.detOutput.append("")         
        strPrint=str(round(((maxIndex-1)/2)+1))+". iteration selected"
        
        # for i in range(10):
        #     hataAyiklama=parent.detVal[maxIndex]-parent.detVal[2*i+1]
        #     print(hataAyiklama)
        self.detOutput.append(strPrint)
        # self.detOutPut.setMaximumHeight(250)    
        parent.varboxlayout.addWidget(self.detOutput,1,0,1,1)

        # self.detOutput.setGeometry(750,75,400,750)
        self.detOutput.show()
        # print(parent.detVal)    
    def aboutInfo(self,parent):
        msg=QMessageBox(parent)
        msg.setWindowTitle("Tutorial on PyQt5")
        msg.setText("This is the main text!")
        msg.setIcon(QMessageBox.Question)
    #    msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Retry|QMessageBox.Ignore|)
        msg.setDefaultButton(QMessageBox.Retry)
        msg.setInformativeText("This application has two main abilities. DoE (Design of Experiment) point generation and test automation."
                                "\n\nDoE point generation is based on D-Optimal experiment design. Application will provide local d-optimal "
                                "but not global d-optimal. "
                                "Right now application is able to generate"
                                " experiments only for 4 variables. Not more, not less.\n\n"
                                "Test automation is based on API. It is designed to use with Vision ATI which have API tool."
                                " There isn't any restriction on the variable number. One could easily use test automation part " 
                                "without touching the DoE part")

        msg.setDetailedText("details")
        print("print managerdayız")
        msg.show()

    def testProg(self,parent,i):
        msg=QMessageBox(self)
        msg.setWindowTitle("Tutorial on PyQt5")
        msg.setText("This is the main text!")
        msg.setIcon(QMessageBox.Question)
        msg.setDefaultButton(QMessageBox.Retry)
        msg.setInformativeText(str(i+1)+". Step \n" + " \n \n Test is in progress: \n")

        msg.setDetailedText("details")

        msg.show()
                   
class doePointGenerator():
    def __init__(self):
        super().__init__()
    def doeTransferGUI(self):

        self.doepoint=[2,3,4,5,6,7,8,9,0,1,2,3,9,8,7,6,13,26,45,92]
        return self.doepoint     
    def doeLabelTransferGUI(self,parent):

        self.doeLabelTransfered=["TqCnvnToFu_MaskOfMap2ForFuMDmdSp_C","FuVcvCtrl1_PreCtrlOfVcv1_CUR","TqCnvnToFu_MaskOfMap4ForFuMDmdSp_C","TqCnvnToFu_MaskOfMap5ForFuMDmdSp_C","FuInjMCalcn_MapStrtForMaiInj_MAP","Time"]        
        return self.doeLabelTransfered
    def boundaryImport(self,dctnry,nStep,nVariable,modelExperiment,iterationNumber):
        print("Allah'a hamd olsun")
  #      print(dict)
  #      print(nRow)
        self.deneme=400
        self.doeLabelDeneme=[]
        self.doepoint=[]
        
#Model için sınır değişkeni isimleri ve mak. min değerleri alınır 
       
        for i in range(len(dctnry)//3):

            self.doeLabelDeneme.append(dctnry[i*3])
            self.doepoint.append(dctnry[(i*3)+1])
            self.doepoint.append(dctnry[(3*i)+2])
            
        self.DoePointDeneme=[]
        # for i in range(0,int(nRow)*4):
        #     self.DoePointDeneme.append(round(int(self.doepoint[2*(i%4)])+((i//4)*((int(self.doepoint[2*(i%4)+1])-int(self.doepoint[2*(i%4)]))/int(nRow)))))
        # print(self.DoePointDeneme)
        print("Doe noktaları basılıyor")
        # print(self.doepoint)
        
#Sınır değerleri olarak -1,1 atanır

        self.doeScaledPoint=[]
        for i in range(len(self.doepoint)//2):
            self.doeScaledPoint.append(-1)
            self.doeScaledPoint.append(1)
            
#Tam faktöryel noktaları oluşturulur
        # print(self.doeScaledPoint)    
        self.V=[]
        self.nV=[]
        for j in range(0,int(nVariable)):

            for i in range(0,21**int(nVariable)):
            
  #              self.V[i].append((int(self.doepoint[j])+((int(self.doepoint[j+1])-int(self.doepoint[j]))/20)*((i//(20**(int(self.nColumn)-(j+1))))%20)))
  #              self.V[i]=(round(int(self.doepoint[j*2])+((int(self.doepoint[2*j+1])-int(self.doepoint[2*j]))/20)*((i//(20**(int(nColumn)-(j+1))))%20)))
                self.V.append((round(float(self.doeScaledPoint[j*2])+((float(self.doeScaledPoint[2*j+1])-float(self.doeScaledPoint[2*j]))/20)*((i//(21**(int(nVariable)-(j+1))))%21),2)))

           # self.nV.append(self.V)
           # print(self.V)
        print(len(self.V))

# Creates a list containing 5 lists, each of 8 items, all set to 0
        self.nV = [[0 for x in range(int(nVariable))] for y in range(21**int(nVariable))]

        for i in range(0,(21**int(nVariable))*int(nVariable)):
 #       for i in range(0,2):            
            self.nV[i//int(nVariable)][(i)%int(nVariable)]=self.V[(i%int(nVariable))*(21**int(nVariable))+(i//int(nVariable))]
#        print(self.nV)
        
        

  ### Bu noktada deney uzayının uç noktalarını bulmak amacıyla liste içinde liste tanımlanacak      

        infoMatrix=[]
        for i in range(0,int(nVariable)+1):
            infoMatrix.append([])
        
        for i in range(0,21**int(nVariable)):
            counter=0
            for j in range(0,int(nVariable)):
                if (self.nV[i][j]==-1 or self.nV[i][j]==1):
                    counter+=1
            infoMatrix[counter].append(i+1)
   

#Bu noktada deney uzayının belli gruplara (köşe, kenar, yüzey vb.) ayrılmış hallerinden kaç elemanın
#seçileceği belirleniyor. Burdaki yüzdeler başka d-optimal testlerinin tersine mühendislik incelemeleri sonucu bulunmuştur. En iyi
#sonucu 4 değişken olduğu durumda vermesi beklenmektedir. 

        verticePointNo=[]
        edgePointNo=[]
        facePointNo=[]
        volumePointNo=[]
        midPointNo=[]           
        stepNumber=int(nStep)
        for i in range(0,iterationNumber):  #iterasyon sayısı
            verticeRand=random.randint(3,14)
            stepNumberRem=stepNumber
            verticeNumber=round((verticeRand*stepNumber)/100)
        
            if verticeNumber>=stepNumberRem:
                verticeNumber=stepNumberRem
                stepNumberRem=0
            stepNumberRem=stepNumberRem-verticeNumber
            edgeNumber=round(random.randint(36,50)*stepNumber/100)
            if edgeNumber>=stepNumberRem:
                edgeNumber=stepNumberRem
           
            stepNumberRem=stepNumberRem-edgeNumber
            volumeNumber=round(random.randint(8,16)*stepNumber/100)
            if volumeNumber>=stepNumberRem:
                volumeNumber=stepNumberRem
           
            stepNumberRem=stepNumberRem-volumeNumber             
            faceNumber=round(random.randint(18,50)*stepNumber/100)
            if faceNumber>=stepNumberRem:
                faceNumber=stepNumberRem
           
            stepNumberRem=stepNumberRem-faceNumber   


            midNumber=round(random.randint(0,6)*stepNumber/100)
            if midNumber>=stepNumberRem:
                midNumber=stepNumberRem
           
            stepNumberRem=stepNumberRem-midNumber
       
            while stepNumberRem>0:

                
                if stepNumberRem>0:
                    verticeNumber+=1
                    stepNumberRem-=1
                if verticeNumber>round((stepNumber*14)/100):
                    verticeNumber-=1
                    stepNumberRem+=1 
                if stepNumberRem>0:                    
                    edgeNumber+=1
                    stepNumberRem-=1                
                if edgeNumber>round((stepNumber*50)/100):
                    edgeNumber-=1                    
                    stepNumberRem+=1
                if stepNumberRem>0:                    
                    faceNumber+=1
                    stepNumberRem-=1                 
                if faceNumber>round((stepNumber*50)/100):
                    faceNumber-=1                    
                    stepNumberRem+=1 
                if stepNumberRem>0:                    
                    volumeNumber+=1
                    stepNumberRem-=1 
                if volumeNumber>round((stepNumber*16)/100):
                    volumeNumber-=1
                    stepNumberRem+=1
                if stepNumberRem>0:                    
                    midNumber+=1
                    stepNumberRem-=1 
                if midNumber>round((stepNumber*6)/100):
                    midNumber-=1            
                    stepNumberRem+=1             

            verticePointNo.append(verticeNumber)
            edgePointNo.append(edgeNumber)
            facePointNo.append(faceNumber)
            volumePointNo.append(volumeNumber)
            midPointNo.append(midNumber)

        if modelExperiment=="2nd Order Taylor Series":
            verticeRndmzList=[]
            edgeRndmzList=[]
            faceRndmzList=[]
            volumeRndmzList=[]
            midRndmzList=[]            

            infoRandomizedList=[]
            for j in range(0,len(infoMatrix)):
                infoRandomizedList.append([])

            for i in range(0,iterationNumber):     #iterasyon sayısı
                infoRandomizedList[4].append(random.sample(range(0, len(infoMatrix[4])), verticePointNo[i]))
                infoRandomizedList[3].append(random.sample(range(0, len(infoMatrix[3])), edgePointNo[i]))
                infoRandomizedList[2].append(random.sample(range(0, len(infoMatrix[2])), facePointNo[i]))
                infoRandomizedList[1].append(random.sample(range(0, len(infoMatrix[1])), volumePointNo[i]))
                infoRandomizedList[0].append(random.sample(range(0, len(infoMatrix[0])), midPointNo[i]))                
            
            print(infoRandomizedList[4])

            print(len(infoMatrix[4]))
            expMatrix=[]            
            for k in range(0,len(infoMatrix)):
                for i in range(0,iterationNumber):  #iterasyon sayısı
                    expMatrix.append([])
                    for j in range(0,len(infoRandomizedList[k][i])):
                        expMatrix[i].append(infoMatrix[k][infoRandomizedList[k][i][j]])
                        
            expFinalMatrix=[]
            
### Seçilen noktalar aday noktalar listesinden eşleştirilir             
            for i in range(0,iterationNumber):     #iterasyon sayısı
                expFinalMatrix.append([])
                for j in range(0,len(expMatrix[i])):
                    expFinalMatrix[i].append(self.nV[expMatrix[i][j]-1])
                     

####### Seçilen deney noktaları gerçek sınırlara göre ölçeklenir



############### Rastgele seçilen deney noktaları için 2nci dereceden
############### Taylor serisine göre bilgi matrisi oluşturulacak
            infoModelMatrix=[]
            for i in range(0,iterationNumber):    #iterasyon sayısı
                infoModelMatrix.append([])
                for j in range(0,len(expFinalMatrix[i])):
                    infoModelMatrix[i].append([])
                    for k in range(0,int(nVariable)):
                        if k<=0:
                            infoModelMatrix[i][j].append(1)
                            for m in range(0,int(nVariable)):                            
                                infoModelMatrix[i][j].append(expFinalMatrix[i][j][m])
                        for n in range(0,int(nVariable)-k):
                            infoModelMatrix[i][j].append(round(expFinalMatrix[i][j][k]*expFinalMatrix[i][j][k+n],3))

########### X'X matrisinin istenen deneme sayısı kadar seçilen noktalar ile determinantı bulunur
########### Bu deneme sayılarının en yüksek determinanta sahip olan deney seçilir 
            print("Genişletilmiş model matrisi")
            infoTransposeMtrx=[]
            dotInfoMatrix=[]
            self.detValueMatrix=[]
            for i in range(0,iterationNumber): # iterasyon sayısı kadar yapılacak
                infoTransposeMtrx.append([])
                dotInfoMatrix.append([])
                infoTransposeMtrx[i]=np.transpose(infoModelMatrix[i])
                dotInfoMatrix[i]=np.dot(infoTransposeMtrx[i],infoModelMatrix[i])
                detValue=np.linalg.det(dotInfoMatrix[i])
                self.detValueMatrix.append(i)
                self.detValueMatrix.append(detValue)
                print(i,". denemenin determinantı",detValue)

############# X'X matrisinin en büyük determinanta sahip elemanı seçilir
            max_value=max(self.detValueMatrix)
            maxIndex=self.detValueMatrix.index(max_value)
            detIndexHi=round(((maxIndex-1)/2)+1)
            # self.detOutput.append("")         
            # strPrint=str(round(((maxIndex-1)/2)+1))+". deneme seçildi"
            
############### Seçilen indise göre matris gerçek boyutlarına ölçeklenir            

            
            for i in range(0,int(nVariable)):   #değişken sayısı
                print(self.doepoint[2*i])      #doepoint ismi değiştirilebilir
                print(self.doepoint[2*i+1])

      #      expActMatrix=expFinalMatrix
            expActMatrix=[]
               
            for j in range(0,int(nStep)):      #test noktası kadar yapılacak
                expActMatrix.append([])
                    
            # print("-1 ve 1 arasında ölçeklenmiş noktalar")                        

            for j in range(0,int(nStep)): #60 nVar
                for k in range(0,int(nVariable)):
                # for k in range(0,4):
                    expActMatrix[j].append(round((expFinalMatrix[detIndexHi-1][j][k]*(float(self.doepoint[2*k+1])-float(self.doepoint[2*k]))+float(self.doepoint[2*k+1])+float(self.doepoint[2*k]))/2,1))
                        # expActMatrix[i][j].append(10)#(float(self.doepoint[2*k+1]))#-float(self.doepoint[2*k]))
       #     print(expActMatrix)           
#### Eşleştirilen noktalar csv dosyasına yazılır
           
  #          for i in range(0,expActMatrix[i]):

                # expActFinalMatrix[i//int(nColumn)][(i)%int(nColumn)]=expActMatrix[(i%int(nColumn))*(21**int(nColumn))+(i//int(nColumn))]
        with open('experiment_list_scaled.csv', mode='w',newline='') as experiment_list_scaled:
            experimentListScaled = csv.writer(experiment_list_scaled, delimiter=',', quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
            experimentListScaled.writerows(expActMatrix)

 ###Aday noktaları csv dosyasına yazılıyor. Bu seçilen deney noktalarının csvye aktarılmısı için kullanılabilir                
        with open('candidate_list.csv', mode='w',newline='') as candidate_list:
            candidateList = csv.writer(candidate_list, delimiter=',', quotechar='"')
            

            # outfile.close()
            candidateList.writerows(self.nV)
            
        

        return self.doeLabelDeneme,self.DoePointDeneme, self.detValueMatrix, expActMatrix
def window():

    app = QApplication(sys.argv)

    win = MasterWindow()
    win.show()
    sys.exit(app.exec_())

window()
print("windowun dışına çıkmadı")
