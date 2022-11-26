# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 11:23:42 2022

@author: kasimoglu
"""

from PyQt5 import Qt
from PyQt5.QtWidgets import QWidget
import sys
import random
from win32com.client import Dispatch
import os 
import win32api
import time


# Initially it was designed with QThread but later on it's changed
class EngineTestAutomation(QWidget):  
    """Engine test automation using API of ATI Vision.
    
    Runs auto test based on the given points
    """   
    eng_tst_chnge_color_sgnl = Qt.pyqtSignal(int)
    eng_tst_reset_color_sgnl = Qt.pyqtSignal(str)
    def __init__(self, EngineTestManager):
        super().__init__()    
        self.w_shell = Dispatch("WScript.Shell")
      
    def import_project(self, parent):
        """Virtual test environment, right now it's not used"""
        # self.project_name, NotUsed = QFileDialog.getOpenFileNames()
        # with open(project_name[0], "rt")as f:
    
        # Create a windows shell object
        self.w_shell = Dispatch("WScript.Shell")
          
        self.ret = self.w_shell.Popup(
            "This script can run with the VISION GUI visible, or can run with \
            VISION running invisible in the background. If you want to see \
            the VISION GUI, then be sure VISION is launched before clicking \
            OK to run this script. Otherwise, just click OK to run it. \n \n \
            To exit this script, click Cancel.", 0, "AddScreenControls", 65)
        if self.ret==2:
            exit()          

        # Launch the XCP simulator from the VISION install folder (used for demo purposes)
        # VisionApp = Dispatch("Vision.ApplicationInterface")
        print("vision app giriş ",parent.project_name)

        # os.startfile(VisionApp.Path + "\XcpIpSim.exe")
        # VisionApp = None
        
        return self.project_name
    
    def run(self, parent):
        """Initial step for auto test"""
        self.run_auto_test(parent)
        
#    @pyqtSlot(str)    
    def run_auto_test(self, parent):  
        """Runs the engine auto test based on the given points"""
        # Create the project object
        # time.sleep(2)
        print("parent to ", parent.test_pnts_from_doe_page)        
        print("engine test manager object", parent.test_pnts_from_doe_page)

        if parent.project_name== None:
            print("You must select project file",parent.project_name)

        else:
            print("***Proje dosyası taşındı", parent.project_name)
        self.ATI_project_generator = Dispatch("Vision.ProjectInterface") 

        # self.recorder=Dispatch("Vision.RecorderFile")
        # self.recObject=Dispatch("VisionProjectComponent")
        # self.recorder= Dispatch("Vision.DeviceInterface")
       
        #Open the virtual XCP project (relative to the script location)
        # Go Online
        self.ATI_project_generator.Online = True
        
        # Create an interface to device "PCM"
        device = self.ATI_project_generator.FindDevice("PCM")

        # Trigger the recording object        

        # An option for adding labels is trying step by step approach. 
        # In each step related label is added as map and checked, \
        # if object is none then process goes on till being added as scalar.  
        option_fr_add_var = 0
        eRow = 0        
        self.var_added_to_test = {}
        self.get_var_type = []
        test_pnts = parent.test_pnts_from_doe_page
        if option_fr_add_var == 0:
            for i in range(len(test_pnts[0]) - 1):
                if i == 0 and test_pnts[0][0] == "Step":
                    print("Step eklenmiş")
                    eRow = 1
                else:
                    print((test_pnts[0][i]))
                    self.var_added_to_test[i-eRow] = device.FindTable3D(
                        test_pnts[0][i])
                    if self.var_added_to_test[i-eRow] == None:
                        print("Doğru yol")                        
                        self.var_added_to_test[i-eRow]                  \
                            = device.FindTable2D(test_pnts[0][i])
                        if self.var_added_to_test[i-eRow] == None:
                            self.var_added_to_test[i-eRow]      \
                                = device.FindScalar(test_pnts[0][i])

                            if self.var_added_to_test[i-eRow] == None:
                                self.get_var_type.append("None")
                            else: 
                                print(self.var_added_to_test[i-eRow].Type)
                                self.get_var_type.append("Calibratable")
                        else:
                            self.get_var_type.append("Curve")
                            print(self.var_added_to_test[i-eRow].Type)
                    else:
                        self.get_var_type.append("Map")
                        print(self.var_added_to_test[i-eRow].Type)
                        
        # Another option is adding labels according to label name. 
        # For Liebherr and Bosch suffix "_C" means calibratable, 
        # "_CUR" means curve and "_MAP" means map.       
                         
        elif option_fr_add_var == 1:
            for i in range(len(test_pnts[0])):
                print(len(test_pnts[0][i]))
            for i in range(len(test_pnts[0])-1):
                if i==0 and test_pnts[0][0]=="Step":
                    print("Ctrl+Alt+Del")
                    eRow=1
                else:
                    print(len(test_pnts[0][0]))
                    if test_pnts[0][i][len(test_pnts[0][i])-1] == "C":
                        self.var_added_to_test[i-eRow]    \
                            = device.FindScalar(test_pnts[0][i])
                        print(i,". scalar variable is added")
                    elif test_pnts[0][i][len(test_pnts[0][i])-1]=="R":
                        print(i,". curve variable is added")
                        self.var_added_to_test[i-eRow]      \
                            = device.FindTable2D(test_pnts[0][i])
                    elif test_pnts[0][i][len(test_pnts[0][i])-1]=="P":
                        print(i,". map variable is added")
                        self.var_added_to_test[i-eRow]    \
                            = device.FindTable3D(test_pnts[0][i])                    
                     
        #Test starts here.        
        self.eng_tst_reset_color_sgnl.emit("change colour")
        for i in range(len(test_pnts)-1):
            if parent.abort==True:
                break
                print(parent.abort,"test aborted, pause") 
            for j in range(len(self.var_added_to_test)):
                if self.get_var_type[j]=="Calibratable":
                    self.var_added_to_test[j].TargetValue = \
                        float(test_pnts[i + 1][j + eRow])
                elif self.get_var_type[j]=="Curve":
                    curve=[]
                    for d in range(
                            len(self.var_added_to_test[j].YaxisActualValues)):
                        curve.append(
                            float(test_pnts[i + 1][j + eRow]))
                    self.var_added_to_test[j].YAxisTargetValues = curve
                    curve = 0
                elif self.get_var_type[j] == "Map":
                    dummy_map=[]
                    for m in range(
                            len(self.var_added_to_test[j].ZaxisActualValues)):
                        dummy_map.append([])
                        ttl_pt = self.var_added_to_test[j].ZaxisActualValues[0]
                        for n in range(len(ttl_pt)):
                            dummy_map[m].append(float(test_pnts[i+1][j+eRow]))
                    print(dummy_map)        
                    self.var_added_to_test[j].ZAxisTargetValues = dummy_map
                    dummy_map = 0
                    
            print(test_pnts[i+1][len(test_pnts[0])-1])
            self.eng_tst_chnge_color_sgnl.emit(i)
            # time.sleep(1)
            t=0

            while t<float(test_pnts[i+1][len(test_pnts[0])-1]):
                time.sleep(0.2)
                print(t)
                if parent.abort==True:
                    break
                    print(parent.abort,"Test is aborted, pause") 
                while parent.pause==True:
                    time.sleep(1)
                    print(parent.abort)
                    
                    if parent.abort==True:
                        break
                        print(parent.abort,"Test is paused, pause")                     
                t+=0.2                    
            

        parent.pause= False
        # Release the objects
        device = None
        calibration = None
        project = None   