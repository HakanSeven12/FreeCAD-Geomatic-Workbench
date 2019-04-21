import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import os
import Mesh

class EditSurface:
    """
    Command to edit surface
    """

    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap'  : Path + '/Resources/Icons/EditSurface.svg',
        'MenuText': "Edit Surface",
        'ToolTip' : "Delete triangles, add a triangle or swap an edge of surface."
    }

    def __init__(self):
        #Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/Resources/UI/EditSurface.ui")
        self.IPFui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #To Do List
        self.IPFui.AddTriangleB.clicked.connect(self.AddTriangle)
        self.IPFui.DeleteTriangleB.clicked.connect(self.DeleteTriangle)
        self.IPFui.SwapEdgeB.clicked.connect(self.SwapEdge)

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return self.resources

    def Activated(self):
        self.IPFui.show()
        self.IPFui.SelectSurfaceCB.clear()
        SS = FreeCAD.ActiveDocument.Surfaces.Group
        OutList = FreeCAD.ActiveDocument.Surfaces.OutList
        self.GroupList = []
        Count = 0

        for i in OutList:
            self.GroupList.append(SS[Count].Name)
            SubSurfaceName = SS[Count].Label
            self.IPFui.SelectSurfaceCB.addItem(str(SubSurfaceName))
            Count = Count + 1

    def AddTriangle(self):
        Index = self.IPFui.SelectSurfaceCB.currentIndex()
        SS = self.GroupList[Index]
        Surface = FreeCAD.ActiveDocument.getObject(SS)
        FreeCADGui.Selection.clearSelection()
        FreeCADGui.Selection.addSelection(Surface)

        FreeCADGui.runCommand("Mesh_AddFacet")

    def DeleteTriangle(self):
        '''Index = self.IPFui.SelectSurfaceCB.currentIndex()
        SS = self.GroupList[Index]
        Surface = FreeCAD.ActiveDocument.getObject(SS)'''

        FreeCADGui.runCommand("Mesh_RemoveComponents")

    def SwapEdge(self):
        Index = self.IPFui.SelectSurfaceCB.currentIndex()
        SS = self.GroupList[Index]
        Surface = FreeCAD.ActiveDocument.getObject(SS)

        print ("Swap")

FreeCADGui.addCommand('Edit Surface',EditSurface()) 
