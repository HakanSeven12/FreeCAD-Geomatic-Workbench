import FreeCAD
import FreeCADGui
import Draft
import csv
import os
from PySide import QtCore, QtGui


class ImportPointFile:
   def __init__(self):
        #Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(FreeCAD.getHomePath() + "Mod/Geomatic/Resources/UI/ImportPointFile.ui")
        
        #To Do List
        self.IPFui.BrowseB.clicked.connect(self.BrowseFile)
        self.IPFui.ImportB.clicked.connect(self.ImportFile)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

   def GetResources(self):
        return {'MenuText': 'Import Point File', 'ToolTip': 'Import point file which include survey data.'}
  
   def Activated(self):
        self.IPFui.show()
  
   def BrowseFile(self):
        self.FilePath = QtGui.QFileDialog.getOpenFileName(None, 'Select File', "", 'All Files (*.*)')
        head, tail = os.path.split(self.FilePath[0])

        self.IPFui.BrowseLE.setText(self.FilePath[0])
        self.IPFui.SubGroupNameLE.setText(tail)

   def ImportFile(self):
        #Import UI variables
        PointNameLE = self.IPFui.PointNameLE.text()
        XLE = self.IPFui.XLE.text()
        YLE = self.IPFui.YLE.text()
        ZLE = self.IPFui.ZLE.text()
        SubPoints = self.IPFui.SubGroupNameLE.text()

        #Create Group under Points
        SubGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",SubPoints)

        for FilePath in self.FilePath:
            File=open(FilePath, 'r')
            reader = csv.reader(File, delimiter=" ")
            for i, row in enumerate( reader ):
                pn = int(PointNameLE)-1
                xx = int(XLE)-1
                yy = int(YLE)-1
                zz = int(ZLE)-1
                
                Point = Draft.makePoint(X = float(row[xx])*1000, Y = float(row[yy])*1000, Z = float(row[zz])*1000, color = None, name = "Point", point_size = 3)
                Point.Label = str(row[pn])
                SubGroup.addObject(Point)
                FreeCAD.ActiveDocument.Points.addObject(SubGroup)

FreeCADGui.addCommand('Import Point File',ImportPointFile()) 
