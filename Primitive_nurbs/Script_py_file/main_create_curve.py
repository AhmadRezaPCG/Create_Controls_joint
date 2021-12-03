###############################################################################
# Name: 
#   Create Controls joint
#
# Description: 
#     I have created this script for save and create nurbs easily . 
#     You can save your custome nurbs and later use that.
#     It allows you to create multi controller for different joint .
#       
#   
#
# Author: 
#   Ahmadreza Rezaei
#
# Copyright (C) 2022 Ahmadreza Rezaei. All rights reserved.
###############################################################################

from functools import partial
from .save_file import save_file_class
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

def maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window),QtWidgets.QWidget)
    
class main_primitivenurbs_class(QtWidgets.QDialog):
    
    FILTER = "Text (*.txt)"
    VERSION_MAYA = cmds.about(version=True)
    PATH_SAVE_FILE = "C:\Users\Ahmad Reza\Documents\maya\{0}\scripts\Primitive_nurbs\save_file".format(VERSION_MAYA)
    dialog_reference = None
    
    def __init__(self,parent=maya_main_window()):
        super(main_primitivenurbs_class,self).__init__(parent)
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.setMinimumSize(700,500)
        self.setMaximumWidth(700)
        self.setWindowTitle("Nurbs primitive")
        self.add_action()
        self.createwidget()
        self.createlayout()
        self.connectsignalslot()
        
    @classmethod
    def show_dialog(cls):
        
        if cls.dialog_reference:
                
            if cls.dialog_reference.isHidden():
                cls.dialog_reference.show()
            else:
                cls.dialog_reference.raise_()
                cls.dialog_reference.activateWindow()
        else:
            cls.dialog_reference = main_primitivenurbs_class()
            cls.dialog_reference.show()    
    
    def add_action(self):
        
        self.A_delete = QtWidgets.QAction()
        self.A_delete.setText("Delete item")
        
        self.A_save = QtWidgets.QAction()
        self.A_save.setText("Save new")
            
    def createwidget(self):
        
        self.W_create = QtWidgets.QWidget()
        self.W_option = QtWidgets.QWidget()
        
        self.TW_main = QtWidgets.QTabWidget(self)
        self.TW_main.addTab(self.W_create,"Create Nurbs")
        self.TW_main.addTab(self.W_option,"Parent Option")
        
        self.SI_horizontal = QtWidgets.QSpacerItem(50,50,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        
        self.MB_edit = QtWidgets.QMenuBar()
        menu_edit = self.MB_edit.addMenu("Edit")
        menu_edit.addAction(self.A_save)
        menu_edit.addSeparator()
        menu_edit.addAction(self.A_delete)
        
        self.PB_refresh = QtWidgets.QPushButton("Refresh")
        self.PB_cancel = QtWidgets.QPushButton("Cancel")
        
        
        # ___________________________________________________________
        
        self.CB_enableoption = QtWidgets.QCheckBox("Enable option")
        self.CB_enableoption.setChecked(False)
        
        self.L_name = QtWidgets.QLineEdit()
        
        self.La_axis = QtWidgets.QLabel("Nornal axis : ")
        self.RB_x = QtWidgets.QRadioButton("X")
        self.RB_x.setChecked(True)
        self.RB_y = QtWidgets.QRadioButton("Y")
        self.RB_z = QtWidgets.QRadioButton("Z")
        
        self.SD_scale = QtWidgets.QDoubleSpinBox()
        self.SD_scale.setValue(1.00)
        
        self.CB_constraint = QtWidgets.QCheckBox("Constraint")
        self.CB_constraint.setChecked(False)
        self.La_constraint = QtWidgets.QLabel("Constraint : ")
        self.RB_parent = QtWidgets.QRadioButton("Parent")
        self.RB_parent.setChecked(True)
        self.RB_orient = QtWidgets.QRadioButton("Orient")
        self.RB_point = QtWidgets.QRadioButton("Point")
        
        self.CB_individual = QtWidgets.QCheckBox("Individual")
        
        
    
    def createlayout(self):
        
        
        SA_GrL = QtWidgets.QScrollArea()
        SA_GrL.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        SA_GrL.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        SA_GrL.setWidgetResizable(True)
        
        self.GrL_item = QtWidgets.QGridLayout()
        self.GrL_item.addItem(self.SI_horizontal,500,500)
        
        W_GrL = QtWidgets.QWidget()
        W_GrL.setLayout(self.GrL_item)
        
        SA_GrL.setWidget(W_GrL)
        
        HL_button = QtWidgets.QHBoxLayout()
        HL_button.addStretch()
        HL_button.addWidget(self.PB_refresh)
        HL_button.addWidget(self.PB_cancel)    
        
        VL_W_create = QtWidgets.QVBoxLayout()
        VL_W_create.addWidget(SA_GrL)
        VL_W_create.addLayout(HL_button)
        
        self.W_create.setLayout(VL_W_create)
        
        # _______________________________________________________
        
        
        self.W_nameandaxis = QtWidgets.QWidget()
        self.W_nameandaxis.setEnabled(False)
        self.W_constraint = QtWidgets.QWidget()
        self.W_constraint.setEnabled(False)
        
        FL_name = QtWidgets.QFormLayout()
        FL_name.addRow("name : " ,self.L_name)
        
        HL_axis = QtWidgets.QHBoxLayout()
        HL_axis.addWidget(self.La_axis)
        HL_axis.addWidget(self.RB_x)
        HL_axis.addWidget(self.RB_y)
        HL_axis.addWidget(self.RB_z)
        HL_axis.addStretch()
        
        FL_spinbox = QtWidgets.QFormLayout()
        FL_spinbox.addRow("Scale : ",self.SD_scale)
        
        VLM_name = QtWidgets.QVBoxLayout()
        VLM_name.addLayout(FL_name)
        VLM_name.addLayout(HL_axis)
        VLM_name.addLayout(FL_spinbox)
        
        self.W_nameandaxis.setLayout(VLM_name)
        
        HL_constraint = QtWidgets.QHBoxLayout()
        HL_constraint.addWidget(self.La_constraint)
        HL_constraint.addWidget(self.RB_parent)
        HL_constraint.addWidget(self.RB_orient)
        HL_constraint.addWidget(self.RB_point)
        HL_constraint.addStretch()
        
        VLM_constraint = QtWidgets.QVBoxLayout()
        VLM_constraint.addLayout(HL_constraint)
        VLM_constraint.addWidget(self.CB_individual)
        
        self.W_constraint.setLayout(VLM_constraint)
        
        Frame_1 = QtWidgets.QFrame()
        Frame_1.setFrameShape(QtWidgets.QFrame.HLine)
        Frame_2 = QtWidgets.QFrame()
        Frame_2.setFrameShape(QtWidgets.QFrame.HLine)
        Frame_3 = QtWidgets.QFrame()
        Frame_3.setFrameShape(QtWidgets.QFrame.HLine)
        
        VL_parent_tab = QtWidgets.QVBoxLayout()
        VL_parent_tab.addWidget(self.CB_enableoption)
        VL_parent_tab.addWidget(Frame_1)
        VL_parent_tab.addWidget(self.W_nameandaxis)
        VL_parent_tab.addWidget(Frame_2)
        VL_parent_tab.addWidget(self.CB_constraint)
        VL_parent_tab.addWidget(Frame_3)
        VL_parent_tab.addWidget(self.W_constraint)
        
        VL_parent_tab.addStretch()
        
        self.W_option.setLayout(VL_parent_tab)
        
        # __________________________________________________________
        
        
        main_window = QtWidgets.QVBoxLayout(self)
        main_window.addWidget(self.TW_main)
        main_window.setMenuBar(self.MB_edit)
        
        
        
    def connectsignalslot(self):
        
        self.A_delete.triggered.connect(self.delete_item)
        self.PB_refresh.clicked.connect(self.update_show_curve)
        self.PB_cancel.clicked.connect(self.close)
        self.A_save.triggered.connect(self.open_save_dialog)
        self.CB_enableoption.toggled.connect(self.on_off_option)
        self.CB_constraint.toggled.connect(self.on_off_constraint)

    def delete_item(self):
        
        filepath_fordelete = QtWidgets.QFileDialog.getOpenFileNames(self, 
                                                    "Choose for delete",
                                                     self.PATH_SAVE_FILE ,
                                                     self.FILTER)[0] 
        if len(filepath_fordelete)>0:
            answer = QtWidgets.QMessageBox.question(self,"About deleting","Are you sure that you want to delete? ")
            if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                self.delete_text_file(filepath_fordelete)
            
            
    def delete_text_file(self,filepath_fordelete):
        
        for file_text_path in filepath_fordelete:
            file_text = QtCore.QFile(file_text_path)
            file_text.remove()
        
        self.update_show_curve()
        
    def open_save_dialog(self):
    
        save_file_class.show_dialog()
    
    def update_show_curve(self):
        
        self.delete_GrL()
        
        dir_save_file = QtCore.QDir(self.PATH_SAVE_FILE)
        files_saved = dir_save_file.entryList("*.txt",QtCore.QDir.NoDotAndDotDot|QtCore.QDir.Files)
        if len(files_saved)==0:
            return
            
        self.get_icon_command(files_saved)
        
    def delete_GrL(self):
        
        count_widget = self.GrL_item.count()
        for index in range(1,count_widget):
            HL_layout = self.GrL_item.itemAt(index).layout()
            count_VL = HL_layout.count()
            for VL_widg in range(count_VL):
                widg = HL_layout.itemAt(VL_widg).widget()
                widg.deleteLater()
            HL_layout.deleteLater()
            
    def get_icon_command(self,files_saved):
        
        index_file = 1
        for file_saved_name in files_saved:
            
            file_saved = QtCore.QFile(self.PATH_SAVE_FILE+"\\"+file_saved_name)
            file_saved.open(QtCore.QIODevice.Text|QtCore.QIODevice.ReadOnly)
            all_text_file = QtCore.QTextStream(file_saved)
            
            name_file = self.get_correctedname(file_saved_name)
            command_create_curve = all_text_file.readLine()
            path_icon = all_text_file.readLine()
            count_shape = int(all_text_file.readLine())
            
            file_saved.close()
            
            self.create_buttonicon(name_file,command_create_curve,path_icon,index_file,count_shape)
            
            index_file+=1
            
    def get_correctedname(self,file_saved_name):
        
        return (file_saved_name.split(".")[0])
            
    def create_buttonicon(self,name_file,command_create_curve,path_icon,index_file,count_shape):
        index_file_column = index_file
        index_file_row = 1
        if index_file > 3:
            index_file_row_divide = (index_file-1)/3
            index_file_row+=index_file_row_divide
            index_file_column = index_file -(3*index_file_row_divide)
        
        icon = QtGui.QPixmap(path_icon)
        
        VL_command_curve = QtWidgets.QVBoxLayout()
        
        PB_command_icon = QtWidgets.QPushButton(name_file)
        create = partial(self.create_shape,command_create_curve,name_file,count_shape)
        PB_command_icon.clicked.connect(create)
        PB_command_icon.setMaximumWidth(200)
        font = QtGui.QFont()
        font.setPointSize(6)
        PB_command_icon.setFont(font)
        
        L_command_icon = QtWidgets.QLabel()
        L_command_icon.setPixmap(icon.scaled(200,200))
        
        VL_command_curve.addWidget(L_command_icon)
        VL_command_curve.addWidget(PB_command_icon)        
        
        self.GrL_item.addLayout(VL_command_curve,index_file_row,index_file_column,QtCore.Qt.AlignTop^QtCore.Qt.AlignmentFlag)
       
    def create_shape(self,command_create_curve,name_file,count_shape):
    
        list_selected = cmds.ls(sl=True)
    
        node_name = cmds.createNode("transform",n=name_file+"_TRANSFORM")
        exec command_create_curve
        
        for numb_shape in range(count_shape):
            shape = cmds.listRelatives("{0}_{1}".format(name_file,numb_shape),shapes=True)
            cmds.parent(shape,node_name,r=True,shape=True)
            cmds.delete("{0}_{1}".format(name_file,numb_shape))
        
        self.deleteHistory(node_name)
        
        if self.CB_enableoption.checkState():
            actual_name = self.go_to_option(node_name)
        else:
            actual_name = None
            
        if self.CB_constraint.checkState():
            if actual_name:
                self.go_to_constraint(actual_name,list_selected)
            else:
                self.go_to_constraint(node_name,list_selected)
            
    def on_off_option(self,bool_option):
        self.W_nameandaxis.setEnabled(bool_option)
        
    def on_off_constraint(self,bool_constraint):
        self.W_constraint.setEnabled(bool_constraint)
    
    def go_to_option(self,node_name):
        
        new_name = self.get_newname(node_name)
        actual_name = self.change_name(new_name,node_name)
        if not actual_name:
            return
        self.change_axis(actual_name)
        self.change_scale(actual_name)
        return actual_name
        
    
    def get_newname(self,node_name):
        
        new_name = self.L_name.text()
        if new_name == "":
            return node_name
        return new_name
    
    
    def change_name(self,new_name,node_name):
        
        try:
            actual_name = cmds.rename(node_name,new_name)
            return actual_name
        except:
            om.MGlobal.displayError("Your new name is not correct")
            return False
            
            
    def change_axis(self,actual_name):
        
        if self.RB_x.isChecked():
            return
        elif self.RB_y.isChecked():
            cmds.setAttr(actual_name+".rz",90)
            self.freeze_mesh(actual_name)
            self.deleteHistory(actual_name)
        else:
            cmds.setAttr(actual_name+".ry",90)
            self.freeze_mesh(actual_name)
            self.deleteHistory(actual_name)
        
    def change_scale(self,actual_name):
        
        value_scale = float(self.SD_scale.value())
        cmds.setAttr(actual_name+".s",value_scale,value_scale,value_scale)
        self.freeze_mesh(actual_name)
        self.deleteHistory(actual_name)
        
    def go_to_constraint(self,node_name,list_selected):
        
        self.constraint_node(node_name,list_selected)
    
    def constraint_node(self,node_name,list_selected):
        
        bool_individual = self.CB_individual.isChecked()
        if self.RB_parent.isChecked():
            self.create_const(list_selected,node_name,bool_individual,"parent")
        elif self.RB_orient.isChecked():
            self.create_const(list_selected,node_name,bool_individual,"orient")
        else:
            self.create_const(list_selected,node_name,bool_individual,"point")
                
        
    
    def create_const(self,list_selected,node_name,bool_individual,type_const):
        
        
        
        if type_const == "parent":
            if bool_individual:
                for name_driver in list_selected:
                    actual_name_driver = name_driver.split("|")
                    new_namenode = cmds.duplicate(node_name,name = "{0}_{1}".format(node_name,actual_name_driver[-1]))[0]
                    parent_newname = self.create_parent_offset(new_namenode)
                    const = cmds.parentConstraint(name_driver,parent_newname,mo=False)[0]
                    cmds.delete(const)
                    cmds.parentConstraint(new_namenode,name_driver,mo=True)
                    
                cmds.delete(node_name)
                
            else:
                offset_namenode = self.create_parent_offset(node_name)
                const = cmds.parentConstraint(list_selected,offset_namenode,mo=False)[0]
                cmds.delete(const)
                for name_selected in list_selected:
                    cmds.parentConstraint(node_name,name_selected,mo=True)
    
        elif type_const == "orient":
            if bool_individual:
                for name_driver in list_selected:
                    
                    new_namenode = cmds.duplicate(node_name,name = "{0}_{1}".format(node_name,name_driver),rr=True)[0]
                    parent_newname = self.create_parent_offset(new_namenode)
                    const = cmds.parentConstraint(name_driver,parent_newname,mo=False)[0]
                    cmds.delete(const)
                    cmds.orientConstraint(new_namenode,name_driver,mo=True)
                    
                cmds.delete(node_name)
                
            else:
                offset_namenode = self.create_parent_offset(node_name)
                const = cmds.parentConstraint(list_selected,offset_namenode,mo=False)[0]
                cmds.delete(const)
                for name_selected in list_selected:
                    cmds.orientConstraint(node_name,name_selected,mo=True)
                
        else:
            if bool_individual:
                for name_driver in list_selected:
                    
                    new_namenode = cmds.duplicate(node_name,name = "{0}_{1}".format(node_name,name_driver),rr=True)[0]
                    parent_newname = self.create_parent_offset(new_namenode)
                    const = cmds.parentConstraint(name_driver,parent_newname,mo=False)[0]
                    cmds.delete(const)
                    cmds.pointConstraint(new_namenode,name_driver,mo=True)
                    
                cmds.delete(node_name)
                
            else:
                offset_namenode = self.create_parent_offset(node_name)
                const = cmds.parentConstraint(list_selected,offset_namenode,mo=False)[0]
                cmds.delete(const)
                for name_selected in list_selected:
                    cmds.pointConstraint(node_name,name_selected,mo=True)
    
    def create_parent_offset(self,new_namenode):
        
        parent_nodemesh = cmds.listRelatives(new_namenode,parent=True)
        offset_node = cmds.createNode("transform",name = new_namenode+"_OFFSET")
        
        parent_const_name = cmds.parentConstraint(new_namenode,offset_node,mo=False)[0]
        cmds.delete(parent_const_name)
        
        if parent_nodemesh:
            cmds.parent(offset_node,parent_nodemesh)
        cmds.parent(new_namenode,offset_node)
        return offset_node
    
    def freeze_mesh(self,actual_name):
        
        cmds.makeIdentity(actual_name,apply  = True ,t=1,r=1,s=1,n=0,pn = 1)
    
    def deleteHistory(self,node_name):
        
        cmds.select(cl=True)
        all_shape = cmds.listRelatives(node_name,shapes=True)    
        cmds.select(all_shape)
        cmds.select(node_name,add=True)
        cmds.DeleteHistory()
        cmds.select(cl=True)
    
    def showEvent(self,e):
        super(main_primitivenurbs_class,self).showEvent(e)
        e.accept()
        self.update_show_curve()

