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

    def max_length(self, P1, P2, P3):
        maxlength_le = self.IPFui.MaxlengthLE.text()
        list_ = [[P1,P2],[P2,P3],[P3,P1]]
        result = []
        for i,j in list_:
            delta_x = i[0] - j[0]
            delta_y = i[1] - j[1]
            length = (delta_x**2+delta_y**2)**0.5
            result.append(length)
        if result[0] <= int(maxlength_le) * 1000 and \
                result[1] <= int(maxlength_le) * 1000 and result[2] <= int(maxlength_le) * 1000:
            return True
        else:
            return False

    def create_surface(self):
        import scipy.spatial

        test_ = []

        # Create surface
        for SelectedIndex in self.IPFui.PointGroupsLV.selectedIndexes():
            index_ = self.group_list[SelectedIndex.row()]
            point_group = FreeCAD.ActiveDocument.getObject(index_).Group

            for Point in point_group:
                xx = float(Point.X)
                yy = float(Point.Y)
                zz = float(Point.Z)
                test_.append([xx, yy, zz])

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

            if self.max_length(data[first], data[second], data[third]):
                mesh_list.append(data[first])
                mesh_list.append(data[second])
                mesh_list.append(data[third])

        mesh_object = Mesh.Mesh(mesh_list)
        mesh_object.Placement.move(basex)
        surface_name_le = self.IPFui.SurfaceNameLE.text()
        surface = FreeCAD.ActiveDocument.addObject("Mesh::Feature", surface_name_le)
        surface.Mesh = mesh_object
        surface.Label = surface_name_le
        self.Surfaces.addObject(surface)


FreeCADGui.addCommand('Create Surface',CreateSurface()) 
