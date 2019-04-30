import FreeCAD
import FreeCADGui
import os

class NewProject:
    """
    Command to creatae a new project
    """
    resources = {
        'Pixmap'  : os.path.dirname(__file__) + '/Resources/Icons/NewProject.svg',
        'MenuText': "New Project",
        'ToolTip' : "Create new project."
    }

    def GetResources(self):
        """
        Return the command resources dictionary
        """
        return self.resources

    def Activated(self):
        #Create Point Groups

        try:
            FreeCAD.ActiveDocument.Point_Groups
        except:
            PointGroups = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Point_Groups')
            PointGroups.Label = "Point Groups"

        try:
            FreeCAD.ActiveDocument.Points
        except:
            Points = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Points')
            PointGroups.addObject(Points)

        #Create Surfaces Group
        try:
            FreeCAD.ActiveDocument.Surfaces
        except:
            FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Surfaces')

        return

FreeCADGui.addCommand('New Project',NewProject())
