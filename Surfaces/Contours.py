import FreeCAD, FreeCADGui
import os
import Draft

class CreateContour:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap'  : Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Create Contour",
        'ToolTip' : "Create contour on selected surface."
    }

    def __init__(self):
        print ("Add Triangle Added")

    def GetResources(self):
        #Return the command resources dictionary
        return self.resources

    def Activated(self):
        Surface = FreeCADGui.Selection.getSelection()[-1]
        Base = Surface.Mesh.Placement.Base
        CopyMesh = Surface.Mesh.copy()
        CopyMesh.Placement.Base = FreeCAD.Vector(0, 0, Base.z)
        try:
            self.Contours = FreeCAD.ActiveDocument.Contours
        except:
            self.Contours = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", 'Contours')

        self.CreateContour(CopyMesh, Base)

    def Wire(self, Name, PointList, Base, Support=None):
        Pl = FreeCAD.Placement()
        Pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        Pl.Base = FreeCAD.Vector(Base.x, Base.y, 0)

        WireObj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython", "_"+str(Name/1000))
        Draft._Wire(WireObj)
        WireObj.Points = PointList
        WireObj.Closed = False
        WireObj.Support = Support
        WireObj.MakeFace = False
        WireObj.Placement = Pl
        if FreeCADGui:
            Draft._ViewProviderWire(WireObj.ViewObject)
            Draft.formatObject(WireObj)
            Draft.select(WireObj)
            self.Contours.addObject(WireObj)
        FreeCAD.ActiveDocument.recompute()
        return WireObj

    def CreateContour(self, Mesh, Base):
        zmax = Mesh.BoundBox.ZMax
        zmin = Mesh.BoundBox.ZMin
        DeltaH = 1000

        for H in range(round(zmin), round(zmax)):
            if H % int(DeltaH) == 0:
                CrossSections = Mesh.crossSections([((0,0,H),(0,0,1))],0.000001)
                for i in CrossSections[0]:
                    Contour = self.Wire(H, i, Base)
                    Contour.Label = str(H/1000)

FreeCADGui.addCommand('Create Contour',CreateContour())
