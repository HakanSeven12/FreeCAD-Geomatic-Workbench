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
        trp = []

        for i in limits:
            xx = float(GroupName[Count].X)
            yy = float(GroupName[Count].Y)
            zz = float(GroupName[Count].Z)
            trp.append([xx,yy,zz])
            Count = Count + 1

        data = np.array(trp)
        test = np.array(trp)
        data -= data.mean(axis=0)
        tri = scipy.spatial.Delaunay( data[:,:2]) # qhull_options = "Q3"

        #pylab.triplot( data[:,0], data[:,1], tri.simplices.copy() )
        #pylab.plot( data[:,0], data[:,1], 'ro' ) ;

        planarMesh = []

        for i in tri.vertices:

           first = int(i[0:1])
           second = int(i[1:2])
           third = int(i[2:3])

           planarMesh.append(test[first])
           planarMesh.append(test[second])
           planarMesh.append(test[third])

        planarMeshObject = Mesh.Mesh(planarMesh)
        Mesh.show(planarMeshObject)

FreeCADGui.addCommand('Create Surface',CreateSurface()) 
