import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import MeshPart, Part, Draft
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
        SectionGroup = FreeCAD.ActiveDocument.getObject("Group")
        Surface = FreeCAD.ActiveDocument.getObject("YY202")
        GuideLinesGroup = FreeCAD.ActiveDocument.getObject("Guide_Lines").Group
        ProjectionDirection = FreeCAD.Vector(0, 0, 1)

        Base = Surface.Mesh.Placement.Base
        CopyMesh = Surface.Mesh.copy()
        CopyMesh.Placement.Base = FreeCAD.Vector(0, 0, Base.z)

        for Wire in GuideLinesGroup:
            Wire.Placement.Base = Wire.Placement.Base.add(Base.negative())
            ProjectedWires = MeshPart.projectShapeOnMesh(Wire.Shape, CopyMesh, ProjectionDirection)
            Wire.Placement.Base = Wire.Placement.Base.add(Base)

            for ProjectedWire in ProjectedWires:
                Section = Draft.makeWire(ProjectedWire)
                Section.Placement.Base = Section.Placement.Base.add(FreeCAD.Vector(Base.x, Base.y, 0))
                SectionGroup.addObject(Section)
        FreeCAD.ActiveDocument.recompute()

FreeCADGui.addCommand('Create Guide Lines',CreateGuideLines())