import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import Draft
import os

class CreateGuideLines:
    #Command to create sections for every selected surfaces.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap'  : Path + '/../Resources/Icons/CreateSections.svg',
        'MenuText': "Export Points",
        'ToolTip' : "Export points to point file."
    }

    def __init__(self):
        #Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/CreateSections.ui")

        #To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateSections)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

    def GetResources(self):
        #Return the command resources dictionary
        return self.Resources

    def Activated(self):
        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()

    def CreateSections(self):

        FreeCAD.ActiveDocument.recompute()

FreeCADGui.addCommand('Create Guide Lines',CreateGuideLines())