import FreeCAD
import FreeCADGui
import Points
import Mesh
import ReverseEngineering as Reen
from PySide import QtCore, QtGui

class CreateSurface:
   def __init__(self):
        #Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(FreeCAD.getHomePath() + "Mod/Geomatic/Resources/UI/CreateSurface.ui")
        
        #To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateSurface)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

   def GetResources(self):
        return {'MenuText': 'Create Surface', 'ToolTip': 'Create surface from selected point group(s).'}

   def Activated(self):
        self.IPFui.show()
        self.planarMesh = []

   def CreateSurface(self):
        #Import UI variables
        SurfaceNameLE = self.IPFui.SurfaceNameLE.text()
        TLenghLE = float(self.IPFui.TLenghLE.text())*1000
        OVLE = float(self.IPFui.OVLE.text())
        #Create surface
        GroupName = FreeCAD.ActiveDocument.All_Points.Group
        OutList = FreeCAD.ActiveDocument.All_Points.OutList
        limits = range(1,int(len(OutList)))
        Count = 0

        for i in limits:
            xx = float(GroupName[Count].X)
            yy = float(GroupName[Count].Y)
            zz = float(GroupName[Count].Z)
            self.planarMesh.append( (xx,yy,zz) ) 
            Count = Count + 1

        Points.show(Points.Points(self.planarMesh))
        PointCloud = FreeCAD.ActiveDocument.Points001.Points
        planarMeshObject=Reen.triangulate(PointCloud, TLenghLE, OVLE)
        Mesh.show(planarMeshObject)

FreeCADGui.addCommand('Create Surface',CreateSurface()) 
