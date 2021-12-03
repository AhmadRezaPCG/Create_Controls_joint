
import os
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
    
class save_file_class(QtWidgets.QDialog):
    
    VERSION_MAYA = cmds.about(version=True)
    PATH_ICON = "C:\Users\Ahmad Reza\Documents\maya\{0}\scripts\Primitive_nurbs\Icon".format(VERSION_MAYA)
    FILTER = "image (*.png ,*.svg);;PNG (*.png);;SVG (*.svg)"
    dialog_reference = None
    
    def __init__(self,parent=maya_main_window()):
        super(save_file_class,self).__init__(parent)
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.file_icon = QtGui.QIcon(":fileOpen.png")
        
        self.setWindowTitle("Save New Curve")
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
            cls.dialog_reference = save_file_class()
            cls.dialog_reference.show()
            
        
    def add_action(self):
        pass
    
    def createwidget(self):
 
        self.LE_name = QtWidgets.QLineEdit()
        self.LE_name.setMaximumWidth(500)
        
        self.LE_icon = QtWidgets.QLineEdit()
        self.LE_icon.setPlaceholderText("300px * 300px")
        self.L_icon = QtWidgets.QLabel(" Select Icon : ")
        
        self.PB_file = QtWidgets.QPushButton()
        self.PB_file.setIcon(self.file_icon)
        
        self.PB_setshape = QtWidgets.QPushButton("Set Shape")
        self.PB_cancel = QtWidgets.QPushButton("Cancel")
        self.PB_save = QtWidgets.QPushButton("Save")
   
    
    def createlayout(self):
        
        self.VL_OBJ_selected = QtWidgets.QVBoxLayout()
        self.VL_OBJ_selected.setMargin(10)
        
        FL_linename = QtWidgets.QFormLayout()
        FL_linename.addRow(" Name : " , self.LE_name)
        
        HL_icon = QtWidgets.QHBoxLayout()
        HL_icon.addWidget(self.L_icon)
        HL_icon.addWidget(self.LE_icon)
        HL_icon.addWidget(self.PB_file)
        
        HL_button = QtWidgets.QHBoxLayout()
        HL_button.addWidget(self.PB_setshape)
        HL_button.addWidget(self.PB_save)
        HL_button.addWidget(self.PB_cancel)
        
        main_window = QtWidgets.QVBoxLayout(self)
        main_window.addLayout(FL_linename)
        main_window.addLayout(HL_icon)
        main_window.addLayout(self.VL_OBJ_selected)
        main_window.addStretch()
        main_window.addLayout(HL_button)
       
    def connectsignalslot(self):
        
        self.PB_cancel.clicked.connect(self.close)
        self.PB_setshape.clicked.connect(self.set_shape)
        self.PB_save.clicked.connect(self.save_shape)
        self.PB_file.clicked.connect(self.open_dialog_getfile)        
        
    def open_dialog_getfile(self):
        
        icon_path = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                    "Select icon",
                                                     self.PATH_ICON ,
                                                     self.FILTER)[0] 
                                                     
        self.set_to_lineeditpath(icon_path)       
        
    def set_to_lineeditpath(self,icon_path):
        
        self.LE_icon.setText(icon_path)
    
    def set_shape(self):
        
        self.info_shape = []
        self.info_position = []
        self.form_shapes = []
        self.knots_shapes = []
        
        count_widget = self.VL_OBJ_selected.count()
        for index_widget in range(count_widget):
            item = self.VL_OBJ_selected.itemAt(index_widget).widget().deleteLater()
            
        
        selection_list = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection_list)
        
        if selection_list.isEmpty():
            return
            
        bool_nurbs = self.check_nurbs_bool(selection_list)
        
        if bool_nurbs:
            
            for i in range(selection_list.length()):
                dag_path = om.MDagPath()
                selection_list.getDagPath(i,dag_path)
                FN_nurbs = om.MFnNurbsCurve(dag_path)
                
                knots = om.MDoubleArray()
                FN_nurbs.getKnots(knots)
                list_knots = self.get_list_knots(knots)
                self.knots_shapes.append(list_knots)
                
                form_shape = FN_nurbs.form() 
                if form_shape == 1:
                    form_shape_str = "Open"
                else:
                    form_shape_str = "Periodic"
                    
                self.form_shapes.append(form_shape)
                degree_shape = FN_nurbs.degree()
                count_cvs_shape = FN_nurbs.numCVs()
                name_shape=FN_nurbs.name()
                
                add_label = QtWidgets.QLabel("Name = {0} , degree = {1} , count CVs = {2} , form = {3} , Count knots = {4}".format(name_shape,degree_shape,count_cvs_shape,form_shape_str,knots.length()))
                self.VL_OBJ_selected.addWidget(add_label)
                
                positions = []
                for IN_cv in range(count_cvs_shape):
                    point = cmds.xform("{0}.cv[{1}]".format(name_shape,IN_cv),t=True,q=True,os=True)
                    positions.append(point)
                self.info_shape.append((name_shape,degree_shape,count_cvs_shape))
                self.info_position.append(positions)
                
    def get_list_knots(self,knots):
        
        list_knot = []
        for knot in knots:
            list_knot.append(int(knot))
        return list_knot
                
    def create_textcreate_shape(self,name,icon_path):
        
        text_command = ""
        for index in range(len(self.info_shape)):
            if self.form_shapes[index] == 1:
                form = False
                text_command = text_command+"cmds.curve(d={0},p={1},name='{4}_{5}');".format(self.info_shape[index][1],
                                                                                        self.info_position[index],
                                                                                        self.knots_shapes[index],
                                                                                        form,
                                                                                        name,
                                                                                        index)
            else:
                form = True
                self.extend_info_position(index)
                text_command = text_command+"cmds.curve(per = {3},p={1},k={2},name='{4}_{5}');".format(self.info_shape[index][1],
                                                                                        self.info_position[index],
                                                                                        self.knots_shapes[index],
                                                                                        form,
                                                                                        name,
                                                                                        index)
            
            
        path_file = "C:\Users\Ahmad Reza\Documents\maya\{0}\scripts\Primitive_nurbs\save_file\{1}.txt".format(self.VERSION_MAYA,name)
        file_info = QtCore.QFileInfo(path_file)
        if file_info.exists():
            answer = QtWidgets.QMessageBox.question(self,"Exist File","This files name is exist.Do you want to continue?\n If you continu , your past files info were deleted.")
            if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                
                file_save = QtCore.QFile(path_file)
                file_save.open(QtCore.QIODevice.Text|QtCore.QIODevice.WriteOnly)
                
                text_stream_file = QtCore.QTextStream(file_save)
                text_stream_file << text_command + "\n" + icon_path+"\n{0}".format(len(self.info_shape))
                
                file_save.close()
                om.MGlobal.displayInfo("Youre shape has saved")
                
        else:
            
            file_save = QtCore.QFile(path_file)
            file_save.open(QtCore.QIODevice.Text|QtCore.QIODevice.WriteOnly)
            
            text_stream_file = QtCore.QTextStream(file_save)
            text_stream_file << text_command + "\n" + icon_path +"\n{0}".format(len(self.info_shape))
            
            file_save.close()
            om.MGlobal.displayInfo("Youre shape has saved")
           
    def extend_info_position(self,index):
        
        first = self.info_position[index][0]
        second = self.info_position[index][1]
        third = self.info_position[index][2]
        self.info_position[index][-1]=third
        self.info_position[index][-2]=second
        self.info_position[index][-3]=first
                
    def save_shape(self):
        
        name = self.check_exist_name()
        icon_path = self.check_exist_icon()
        info_shape = self.check_infoshape()
        if name and icon_path and info_shape:
            text_command = self.create_textcreate_shape(name,icon_path)
        
    def check_infoshape(self):
        
        try:
            if self.info_shape and len(self.info_shape)>0:
                return True
            else:
                om.MGlobal.displayError("First select your shapes and set shape")
                return False
        except:
            om.MGlobal.displayError("First select your shapes and set shape")
            return False
        
    def check_exist_name(self):
        
        name = self.LE_name.text()
        if name == "":
            om.MGlobal.displayError("Enter its name")
            return False
        try:
            check_numb = name[0]
            numb = int(check_numb)
            om.MGlobal.displayError("You cant't use numb at the first name")
            return False
        except:
            pass
        return name
        
    def check_exist_icon(self):
        
        icon_path = self.LE_icon.text()
        if icon_path == "":
            om.MGlobal.displayError("Enter its icon_path")
            return False
            
        info_file = QtCore.QFileInfo(icon_path)
        if not info_file.exists():
            om.MGlobal.displayError("Youre icon path is not exists in directory")
            return False
            
        return icon_path
                
    def check_nurbs_bool(self,selection_list):
        
        for index_selected in range(selection_list.length()):
            
            dag_path = om.MDagPath()
            selection_list.getDagPath(index_selected,dag_path)
            
            if dag_path.apiType()!=om.MFn.kNurbsCurve:
                om.MGlobal.displayError("Select nurbs shape")
                return False
        return True
        
    def showEvent(self,e):
        super(save_file_class,self).showEvent(e)
        e.accept()