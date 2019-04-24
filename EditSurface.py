import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import os
import Mesh
from pivy import coin

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

    def mouseClick(self,cb):
        event = cb.getEvent()
        if event.getButton() == coin.SoMouseButtonEvent.BUTTON2 and event.getState() == coin.SoMouseButtonEvent.DOWN:
            FreeCADGui.ActiveDocument.ActiveView.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.MC)
        if event.getButton() == coin.SoMouseButtonEvent.BUTTON1 and event.getState() == coin.SoMouseButtonEvent.DOWN:
            pp = cb.getPickedPoint()
            if not pp is None:
                detail = pp.getDetail()
                if detail.isOfType(coin.SoFaceDetail.getClassTypeId()):
                    face_detail = coin.cast(detail, str(detail.getTypeId().getName()))
                    index = face_detail.getFaceIndex()
                    self.list_of_indexes.append(index)
                    if len(self.list_of_indexes) == 2:
                        Index = self.IPFui.SelectSurfaceCB.currentIndex()
                        SS = self.GroupList[Index]
                        Surface = FreeCADGui.ActiveDocument.getObject(SS)
                        MeshObj = Surface.Object
                        CopyMesh = MeshObj.Mesh.copy()
                        CopyMesh.swapEdge(self.list_of_indexes[0],self.list_of_indexes[1])
                        MeshObj.Mesh = CopyMesh
                        self.list_of_indexes.clear()

    def SwapEdge(self):
        self.list_of_indexes = []
        self.MC = FreeCADGui.ActiveDocument.ActiveView.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.mouseClick)

FreeCADGui.addCommand('Edit Surface',EditSurface()) 
