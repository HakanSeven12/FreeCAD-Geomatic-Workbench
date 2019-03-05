import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import Mesh

class EditSurface:
   def __init__(self):
        #Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(FreeCAD.getHomePath() + "Mod/Geomatic/Resources/UI/EditSurface.ui")
        self.IPFui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #To Do List
        self.IPFui.AddTriangleB.clicked.connect(self.AddTriangle)
        self.IPFui.DeleteTriangleB.clicked.connect(self.DeleteTriangle)
        self.IPFui.SwapEdgeB.clicked.connect(self.SwapEdge)

   def GetResources(self):
        return {'MenuText': 'Edit Surface', 'ToolTip': 'Delete a triangle, add a triangle or swap an edge of surface.'}

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

        print ("Add")

   def DeleteTriangle(self):
        '''Index = self.IPFui.SelectSurfaceCB.currentIndex()
        SS = self.GroupList[Index]
        Surface = FreeCAD.ActiveDocument.getObject(SS)'''

        FreeCADGui.runCommand("Mesh_RemoveComponents")

        print ("Delete")

   def SwapEdge(self):
        Index = self.IPFui.SelectSurfaceCB.currentIndex()
        SS = self.GroupList[Index]
        Surface = FreeCAD.ActiveDocument.getObject(SS)

        FreeCADGui.runCommand("Mesh_SwapEdge")

        print ("Swap")

FreeCADGui.addCommand('Edit Surface',EditSurface()) 
