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
        try:
            self.Contours = FreeCAD.ActiveDocument.Contours
        except:
            self.Contours = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Contours')

        self.CreateContour(Surface)

    def CreateContour(self,Surface):
        zmax = Surface.Mesh.BoundBox.ZMax
        zmin = Surface.Mesh.BoundBox.ZMin
        h = 0
        dh =1000

        while h < zmax:
            if h>zmin:
                CrossSections = Surface.Mesh.crossSections([((0,0,h),(0,0,1))],0.000001)
                for i in CrossSections[0]:
                    Contour = Draft.makeWire(i)
                    self.Contours.addObject(Contour)
                h += dh
            else:
                h += dh

FreeCADGui.addCommand('Create Contour',CreateContour())