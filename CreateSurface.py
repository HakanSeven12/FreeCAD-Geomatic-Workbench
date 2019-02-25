import FreeCAD
import FreeCADGui
import Points
import Mesh
import ReverseEngineering as Reen

class CreateSurface:
   def __init__(self):
        self.planarMesh = []
        #Import *.ui file(s)
        #self.IPFui = FreeCADGui.PySideUic.loadUi(FreeCAD.getHomePath() + "Mod/Geomatic/Resources/UI/ImportPointFile.ui")
        
        #To Do List

   def GetResources(self):
        return {'MenuText': 'Create Surface', 'ToolTip': 'Create surface from selected point group.'}
  
   def Activated(self):
        GroupName = FreeCAD.ActiveDocument.All_Points.Group
        OutList = FreeCAD.ActiveDocument.All_Points.OutList
        limits = range(1,364)
        Count = 0

        for i in limits:
            xx = float(GroupName[Count].X)
            yy = float(GroupName[Count].Y)
            zz = float(GroupName[Count].Z)
            self.planarMesh.append( (xx,yy,zz) ) 
            Count = Count + 1

        Points.show(Points.Points(self.planarMesh))
        PointCloud = FreeCAD.ActiveDocument.Points001.Points
        planarMeshObject=Reen.triangulate(PointCloud, 30000, 1000)
        #planarMeshObject=Reen.triangulate(PointCloud, 10000, 3.5)
        Mesh.show(planarMeshObject)

FreeCADGui.addCommand('Create Surface',CreateSurface()) 