import FreeCAD, FreeCADGui
from FreeCAD import Base
from PySide import QtCore, QtGui
import numpy as np
import Mesh
import os


class CreateSurface:
    """
    Command to create a new surface
    """

    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap': Path + '/../Resources/Icons/create_surface.svg',
        'MenuText': "Create Surface",
        'ToolTip': "Create surface from selected point group(s)."
    }

    def __init__(self):
        # Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/create_surface.ui")

        # todo :
        self.IPFui.CreateB.clicked.connect(self.create_surface)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

    def get_resources(self):
        """
        Return the command resources dictionary
        """
        return self.resources

    def activated(self):
        try:
            self.Surfaces = FreeCAD.ActiveDocument.Surfaces
        except:
            self.Surfaces = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", 'Surfaces')

        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()
        model = QtGui.QStandardItemModel()
        self.IPFui.PointGroupsLV.setModel(model)

        point_groups = FreeCAD.ActiveDocument.Point_Groups.Group
        self.group_list = []

        for PointGroup in point_groups:
            self.group_list.append(PointGroup.Name)
            sub_group_name = PointGroup.Label
            item = QtGui.QStandardItem(sub_group_name)
            model.appendRow(item)


    def MaxLength(self,P1,P2,P3):
        MaxlengthLE = self.IPFui.MaxlengthLE.text()
        List = [[P1, P2], [P2, P3], [P3, P1]]
        Result = []
        for i, j in List:
            DeltaX = i[0] - j[0]
            DeltaY = i[1] - j[1]
            Length = (DeltaX**2+DeltaY**2)**0.5
            Result.append(Length)
        if Result[0] <= int(MaxlengthLE)*1000 and Result[1] <= int(MaxlengthLE)*1000 and Result[2] <= int(MaxlengthLE)*1000:
            return True
        else:
            return False

    def MaxAngle(self, P1, P2, P3):
        import math
        MaxAngleLE = self.IPFui.MaxAngleLE.text()
        List = [[P1, P2], [P2, P3], [P3, P1]]
        Result = []
        for i, j in List:
            Radian = FreeCAD.Vector(i).getAngle(FreeCAD.Vector(j))
            Angle = math.degrees(Radian)
            Result.append(Angle)
            print(Angle)
        if Result[0] <= int(MaxAngleLE)*1000 and Result[1] <= int(MaxAngleLE)*1000 and Result[2] <= int(MaxAngleLE)*1000:
            return True
        else:
            return False

    def CreateSurface(self):
        import scipy.spatial

        test_ = []

        # Create surface
        for SelectedIndex in self.IPFui.PointGroupsLV.selectedIndexes():
            Index = self.GroupList[SelectedIndex.row()]
            PointGroup = FreeCAD.ActiveDocument.getObject(Index)

            for Point in PointGroup.Points.Points:
                xx = float(Point.x)
                yy = float(Point.y)
                zz = float(Point.z)
                Test.append([xx,yy,zz])

        data = np.array(test_)
        data_on = data.mean(axis=0)
        basex = FreeCAD.Vector(data_on[0], data_on[1], data_on[2])
        data -= data_on
        tri = scipy.spatial.Delaunay(data[:, :2])

        mesh_list = []

        for i in tri.vertices:
            first = int(i[0])
            second = int(i[1])
            third = int(i[2])

            if self.MaxLength(Data[first], Data[second], Data[third])\
            and self.MaxAngle(Data[first], Data[second], Data[third]):
                MeshList.append(Data[first])
                MeshList.append(Data[second])
                MeshList.append(Data[third])

        MeshObject = Mesh.Mesh(MeshList)
        MeshObject.Placement.move(Basex)
        SurfaceNameLE = self.IPFui.SurfaceNameLE.text()
        Surface = FreeCAD.ActiveDocument.addObject("Mesh::Feature", SurfaceNameLE)
        Surface.Mesh = MeshObject
        Surface.Label = SurfaceNameLE
        self.Surfaces.addObject(Surface)

FreeCADGui.addCommand('Create Surface',CreateSurface()) 
