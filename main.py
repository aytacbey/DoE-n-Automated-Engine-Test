# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 12:11:33 2021

@author: kasimoglu
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5.QtGui import QFont
import sys
from page_manager import PageManager
from doe_manager import DoEManager
from engine_test_manager import EngineTestManager
from print_manager import PrintManager


class MasterWindow(QMainWindow):
    """Main class_inst for tool.
    
    Tool should be executed from this module.
    """
    def __init__(self):
        super(MasterWindow, self).__init__()
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.m_pages = {}
        self.register(DoEManager(), "doe manager")
        self.register(EngineTestManager(), "engine test manager")

        self.setGeometry(100, 100, 600, 600)

        # Initializing signal register
        self.go_to("doe manager")
        # self.clear_cells_master()
        # self.import_csv_master()
        # self.export_csv_master()
        # self.lock_cells_master()
        # self.unlock_cells_master()
        # self.add_column_master()
        # self.remove_column_master()
        # self.add_row_master()
        # self.remove_row_master()
        self.doe_points_trnsfr_master()
        self.init_UI()

    def init_UI(self):
        """Initialization of UI"""
        self.setGeometry(100, 100, 800, 900)
        self.setWindowTitle("DoE Point Generator")

        # Table is generated
        self.font = QFont()
        self.font.setBold(True)

        menubar = self.menuBar()
        self.file_menu = menubar.addMenu('File')
        self.edit_menu = menubar.addMenu('Edit')
        self.view_menu = menubar.addMenu('View')
        self.tool_menu = menubar.addMenu('Tools')
        self.help_menu = menubar.addMenu('Help')

        # Menus and submenus are generated
        menu_new_action = QAction('New', self)
        menu_open_action = QAction('Open', self)
        menu_save_action = QAction('Save', self)
        menu_import_action = QMenu('Import', self)
        menu_import_to_csv_action = QAction('Import to csv', self)
        menu_import_action.addAction(menu_import_to_csv_action)
        menu_export_action = QMenu('Export', self)
        menu_export_csv_action = QAction('Export csv', self)
        menu_export_action.addAction(menu_export_csv_action)
        menu_quit_action = QAction('Quit', self)

        options_menu = QMenu('Options', self)
        options_test_settings = QAction('Test Settings', self)
        options_menu.addAction(options_test_settings)

        menu_about_action = QAction('About', self)

        # Menu and functions are connected
        menu_import_to_csv_action.triggered.connect(self.import_csv_master)
        menu_export_csv_action.triggered.connect(self.export_csv_master)
        self.print_widget = PrintManager()
        menu_about_action.triggered.connect(self.about_method)

        self.file_menu.addAction(menu_new_action)
        self.file_menu.addAction(menu_open_action)
        self.file_menu.addAction(menu_save_action)
        self.file_menu.addMenu(menu_import_action)
        self.file_menu.addMenu(menu_export_action)
        self.file_menu.addAction(menu_quit_action)
        self.tool_menu.addMenu(options_menu)
        self.help_menu.addAction(menu_about_action)
        menu_quit_action.triggered.connect(self.quit_app)

    def about_method(self):
        """Information about tool"""
        self.print_widget.info_about_program(self)

    # Import csv func from menu
    def import_csv_master(self):
        """Import from csv func which is triggered from menu"""
        # Import Csv function's signal-slot
        class_inst = self.m_pages['doe manager']
        class_inst.import_csv_func_sgnl.connect(self.import_csv_func_slot)
        class_inst.import_csv_from_master()
        
    @QtCore.pyqtSlot(str)
    def import_csv_func_slot(self, isim):
        """Import from csv func which is triggered from menu"""
        self.m_pages['doe manager'].table_widget.import_csv(self)

    # Export csv func from menu
    def export_csv_master(self):
        """Export to csv func which is triggered from menu"""
        # Export csv signal-slot
        class_inst = self.m_pages['doe manager']
        class_inst.export_csv_func_sgnl.connect(self.export_csv_func_slot)
        class_inst.export_csv_from_master()
        
    @QtCore.pyqtSlot(str)
    def export_csv_func_slot(self, isim):
        """Export to csv func which is triggered from menu"""
        self.m_pages['doe manager'].table_widget.export_csv(self)

    def quit_app(self):
        """Quits the app"""
        self.close()

    # Skip between doe point generation and test automation.
    def register(self, widget, name):
        """Register the instances of DoE Manager and Engine Test Manager 
        class
        """
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageManager):
            widget.go_to_func_sgnl.connect(self.go_to)

    @QtCore.pyqtSlot(str)
    def go_to(self, name):
        """Switches between pages"""
        if name == "engine test manager":
            pass
            # widget = self.m_pages[name]
        if name in self.m_pages:
            widget = self.m_pages[name]
            if name == "engine test manager":
                widget.exprmnt_var_display()
                widget.exprmnt_page_init()
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())
            
    # Another alternative to manipulate table, right now it is obsolete.
    # def clear_cells_master(self):
    #     # Clear cells signal-slot
    #     class_inst = self.m_pages['doe manager']
    #     class_inst.clear_cells_func_sgnl.connect(self.clear_cells_func_slot)

    # @QtCore.pyqtSlot(str)
    # def clear_cells_func_slot(self, isim):
    #     print("İnşAllah oldu")
    #     self.table_widget.clearCells(self)

    # def import_csv_master(self):
    #     # Import Csv function's signal-slot
    #     class_inst = self.m_pages['doe manager']
    #     class_inst.import_csv_func_sgnl.connect(self.import_csv_func_slot)

    # @QtCore.pyqtSlot(str)
    # def import_csv_func_slot(self, isim):
    #     print("Import Csv")
    #     self.table_widget.importCsv(self)

    # def export_csv_master(self):
    #     # Export csv signal-slot
    #     class_inst = self.m_pages['doe manager']
    #     class_inst.export_csv_func_sgnl.connect(self.export_csv_func_slot)

    # @QtCore.pyqtSlot(str)
    # def export_csv_func_slot(self, isim):
    #     self.table_widget.exportCsv(self)

    # def lock_cells_master(self):
    #     # Lock cells signal-slot
    #     class_inst = self.m_pages['doe manager']
    #     class_inst.lock_cells_func_sgnl.connect(self.lock_cells_func_slot)

    # @QtCore.pyqtSlot(str)
    # def lock_cells_func_slot(self, isim):
    #     print("İnşAllah oldu")
    #     self.table_widget.enableReadOnly(self)

    # def unlock_cells_master(self):
    #     # Unlock cells signal-slot
    #     class_inst = self.m_pages['doe manager']
    #     class_inst.unlock_cells_func_sgnl.connect(self.unlock_cells_func_slot)

    # @QtCore.pyqtSlot(str)
    # def unlock_cells_func_slot(self, isim):
    #     print("İnşAllah oldu")
    #     self.table_widget.enableReadWrite(self)

    # def add_column_master(self):
    #     # Add column signal-slot
    #     class_inst = self.m_pages['doe manager']
    #     class_inst.add_column_func_sgnl.connect(self.add_column_func_slot)

    # @QtCore.pyqtSlot(str)
    # def add_column_func_slot(self, isim):
    #     print("İnşAllah oldu")
    #     self.table_widget.addColumn(self)

    # def remove_column_master(self):
    #     # Remove column signal-slot
    #     class_inst = self.m_pages['doe manager']
    #     class_inst.remove_column_func_sgnl.connect(self.remove_column_slot)

    # @QtCore.pyqtSlot(str)
    # def remove_column_slot(self, isim):
    #     print("İnşAllah oldu")
    #     self.table_widget.removeColumn(self)

    # def add_row_master(self):
    #     # Add row signal-slot
    #     class_inst = self.m_pages['doe manager']
    #     class_inst.add_row_func_sgnl.connect(self.add_row_func_slot)

    # @QtCore.pyqtSlot(str)
    # def add_row_func_slot(self, isim):
    #     print("İnşAllah oldu")
    #     self.table_widget.addRow(self)

    # def remove_row_master(self):
    #     # Remove row signal-slot
    #     class_inst = self.m_pages['doe manager']
    #     class_inst.remove_row_func_sgnl.connect(self.remove_row_func_slot)

    # @QtCore.pyqtSlot(str)
    # def remove_row_func_slot(self, isim):
    #     print("İnşAllah oldu")
    #     self.table_widget.removeRow(self)

    def doe_points_trnsfr_master(self):
        """DoE test points are carried to table"""
        # Doe Transfer signal-slot
        class_inst = self.m_pages['doe manager']
        class_inst.doe_points_trnsfr_func_sgnl.connect(
                    self.doe_points_trnsfr_func_slot)

    @QtCore.pyqtSlot(list, list, str, str, int)
    def doe_points_trnsfr_func_slot(self, doe_labels, doe_points,
                                    step_time, row_num, col_num):
        """DoE test points are carried to table"""
        class_inst = self.m_pages['doe manager']
        self.row_num = row_num
        self.col_num = col_num
        class_inst.table_widget.adapt_row_n_column(self)
        class_inst.table_widget.doe_points_to_table(doe_labels, doe_points,
                                               step_time, row_num, col_num)


def window():
    app = QApplication(sys.argv)
    win = MasterWindow()
    win.show()
    sys.exit(app.exec_())


window()
