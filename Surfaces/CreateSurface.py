import FreeCAD, FreeCADGui
from FreeCAD import Base
from PySide import QtCore, QtGui
import scipy.spatial
import numpy as np
import Mesh
import os

class CreateSurface:
    """
    Command to create a new surface
    """

    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap'  : Path + '/../Resources/Icons/CreateSurface.svg',
        'MenuText': "Create Surface",
        'ToolTip' : "Create surface from selected point group(s)."
    }

    def __init__(self):
        #Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/CreateSurface.ui")

        #To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateSurface)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return self.resources

    def Activated(self):
        try:
            self.Surfaces = FreeCAD.ActiveDocument.Surfaces
        except:
            self.Surfaces = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Surfaces')

        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()
        model = QtGui.QStandardItemModel()
        self.IPFui.PointGroupsLV.setModel(model)

        SG = FreeCAD.ActiveDocument.Point_Groups.Group
        OutList = FreeCAD.ActiveDocument.Point_Groups.OutList
        self.GroupList = []
        Count = 0

        for i in OutList:
            self.GroupList.append(SG[Count].Name)
            SubGroupName = SG[Count].Label
            item = QtGui.QStandardItem(SubGroupName)
            model.appendRow(item)
            Count = Count + 1

    def MaxLength(self,P1,P2,P3):
        MaxlengthLE = self.IPFui.MaxlengthLE.text()
        List = [[P1,P2],[P2,P3],[P3,P1]]
        Result = []
        for i,j in List:
            DeltaX = i[0] - j[0]
            DeltaY = i[1] - j[1]
            Length = (DeltaX**2+DeltaY**2)**0.5
            Result.append(Length)
        if Result[0] <= int(MaxlengthLE)*1000 and Result[1] <= int(MaxlengthLE)*1000 and Result[2] <= int(MaxlengthLE)*1000:
            return True
        else:
            return False

    def CreateSurface(self):
        #Import UI variables
        SurfaceNameLE = self.IPFui.SurfaceNameLE.text()
        Test = []
        GroupCounter = 0

        #Create surface
        for i in self.IPFui.PointGroupsLV.selectedIndexes():
            Selections = self.IPFui.PointGroupsLV.selectedIndexes()[GroupCounter]
            Index = int(Selections.row())
            SPG = self.GroupList[Index]
            GroupName = FreeCAD.ActiveDocument.getObject(SPG).Group
            OutList = FreeCAD.ActiveDocument.getObject(SPG).OutList
            limits = range(1,int(len(OutList)+1))
            GroupCounter = GroupCounter + 1
            Count = 0

            for i in limits:
                xx = float(GroupName[Count].X)
                yy = float(GroupName[Count].Y)
                zz = float(GroupName[Count].Z)
                Test.append([xx,yy,zz])
                Count = Count + 1

        Data = np.array(Test)
        DataOn = Data.mean(axis=0)
        Basex = FreeCAD.Vector(DataOn[0], DataOn[1], DataOn[2])
        Data -= DataOn
        tri = scipy.spatial.Delaunay(Data[:,:2])

        MeshList = []

        for i in tri.vertices:
            first = int(i[0])
            second = int(i[1])
            third = int(i[2])

            if self.MaxLength(Data[first], Data[second], Data[third]):
                MeshList.append(Data[first])
                MeshList.append(Data[second])
                MeshList.append(Data[third])

        MeshObject = Mesh.Mesh(MeshList)
        MeshObject.Placement.move(Basex)
        Surface = FreeCAD.ActiveDocument.addObject("Mesh::Feature", SurfaceNameLE)
        Surface.Mesh = MeshObject
        Surface.Label = SurfaceNameLE
        self.Surfaces.addObject(Surface)

FreeCADGui.addCommand('Create Surface',CreateSurface()) 
