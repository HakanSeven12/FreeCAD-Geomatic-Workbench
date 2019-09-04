import FreeCAD, FreeCADGui
import os
import Draft


class CreateContour:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap': Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Create Contour",
        'ToolTip': "Create contour on selected surface."
    }

    def __init__(self):
        # todo : does not make sense
        print("Add Triangle Added")

    def get_resources(self):
        # Return the command resources dictionary
        return self.resources

    def is_active(self):
        if FreeCADGui.Selection.getSelection() is not None:
            selection = FreeCADGui.Selection.getSelection()[-1]
            if selection.TypeId == 'Mesh::Feature':
                return True
        return False

    def activated(self):
        surface = FreeCADGui.Selection.getSelection()[-1]
        base = surface.Mesh.Placement.Base
        copy_mesh = surface.Mesh.copy()
        copy_mesh.Placement.Base = FreeCAD.Vector(0, 0, base.z)
        # todo : try - except part should be changed
        try:
            self.contours = FreeCAD.ActiveDocument.Contours
        except:
            self.contours = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", 'contours')

        self.create_contour(copy_mesh, base)

    def wire(self, name, point_list, base, support=None):
        Pl = FreeCAD.Placement()
        Pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        Pl.Base = FreeCAD.Vector(base.x, base.y, 0)

        wire_obj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython", "_" + str(name / 1000))
        Draft._Wire(wire_obj)  # it seems Wire is a protected member of Draft. Are you really sure?
        wire_obj.Points = point_list
        wire_obj.Closed = False
        wire_obj.Support = support
        wire_obj.MakeFace = False
        wire_obj.Placement = Pl
        if FreeCADGui:
            Draft._ViewProviderWire(wire_obj.ViewObject)  # protected member again
            Draft.formatObject(wire_obj)
            Draft.select(wire_obj)
            self.contours.addObject(wire_obj)
        FreeCAD.ActiveDocument.recompute()
        return wire_obj

    def create_contour(self, Mesh, Base):
        zmax = Mesh.BoundBox.ZMax
        zmin = Mesh.BoundBox.ZMin
        delta_h = 1000

        for H in range(round(zmin), round(zmax)):
            if H % int(delta_h) == 0:
                cross_sections = Mesh.crossSections([((0,0,H),(0,0,1))],0.000001)
                for i in cross_sections[0]:
                    contour = self.wire(H, i, Base)
                    contour.Label = str(H/1000)


FreeCADGui.addCommand('Create Contour',CreateContour())
