import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import MeshPart, Part, Draft
import os


class CreateGuideLines:
    # Command to create sections for every selected surfaces.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap': Path + '/../Resources/Icons/create_sections.svg',
        'MenuText': "Export Points",
        'ToolTip': "Export points to point file."
    }

    def __init__(self):
        # Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/create_sections.ui")

        # todo :
        self.IPFui.CreateB.clicked.connect(self.create_sections)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

    def get_resources(self):
        #Return the command resources dictionary
        return self.Resources

    def activated(self):
        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()

    @staticmethod  # i added staticmethod wrapper due to not using any instance attr
    def create_sections():
        section_group = FreeCAD.ActiveDocument.getObject("Group")
        surface = FreeCAD.ActiveDocument.getObject("YY202")
        guide_lines_group = FreeCAD.ActiveDocument.getObject("Guide_Lines").Group
        projection_direction = FreeCAD.Vector(0, 0, 1)

        base = surface.Mesh.Placement.Base
        copy_mesh = surface.Mesh.copy()
        copy_mesh.Placement.Base = FreeCAD.Vector(0, 0, base.z)

        for Wire in guide_lines_group:
            Wire.Placement.Base = Wire.Placement.Base.add(base.negative())
            projected_wires = MeshPart.projectShapeOnMesh(Wire.Shape, copy_mesh, projection_direction)
            Wire.Placement.Base = Wire.Placement.Base.add(base)

            for ProjectedWire in projected_wires:
                section = Draft.makeWire(ProjectedWire)
                section.Placement.Base = section.Placement.Base.add(FreeCAD.Vector(base.x, base.y, 0))
                section_group.addObject(section)
        FreeCAD.ActiveDocument.recompute()


FreeCADGui.addCommand('Create Guide Lines',CreateGuideLines())