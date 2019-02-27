import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import Points
import Mesh
import numpy as np
import scipy.spatial
from scipy.spatial import Delaunay
import pylab

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
        #Create surface
        GroupName = FreeCAD.ActiveDocument.All_Points.Group
        OutList = FreeCAD.ActiveDocument.All_Points.OutList
        limits = range(1,int(len(OutList)))
        Count = 0
        data = np.empty((0,3), float)

        for i in limits:
            xx = int(GroupName[Count].X)
            yy = int(GroupName[Count].Y)
            zz = int(GroupName[Count].Z)
            np.append(data, np.array([[xx,yy,zz]]),axis = 0)
            Count = Count + 1

        print (data)
  
        tri = scipy.spatial.Delaunay( data[:,:2] )

        pylab.triplot( data[:,0], data[:,1], tri.simplices.copy() )
        pylab.plot( data[:,0], data[:,1], 'ro' ) ;

        planarMesh = []

        for i in tri.simplices:

           first = int(i[0:1])
           second = int(i[1:2])
           third = int(i[2:3])

           planarMesh.append(data[first])
           planarMesh.append(data[second])
           planarMesh.append(data[third])

        planarMeshObject = Mesh.Mesh(planarMesh)
        Mesh.show(planarMeshObject)

FreeCADGui.addCommand('Create Surface',CreateSurface()) 
