import FreeCAD
import FreeCADGui
import Draft
import csv
import os
from PySide import QtCore, QtGui
import sys

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
        self.FilePath = QtGui.QFileDialog.getOpenFileName(None, 'Select File', "", '*.*')

        self.IPFui.BrowseLE.setText(self.FilePath[0])

   def ImportFile(self):
        #Import UI variables
        PointNameLE = self.IPFui.PointNameLE.text()
        XLE = self.IPFui.XLE.text()
        YLE = self.IPFui.YLE.text()
        ZLE = self.IPFui.ZLE.text()

        for FilePath in self.FilePath:
            File=open(FilePath, 'r')
            reader = csv.reader(File, delimiter=" ")
            for i, row in enumerate( reader ):
                if i == 0: continue # Skip column titles
                #pn, xx, yy, zz = row[0:4]
                pn = int(PointNameLE)-1
                xx = int(XLE)-1
                yy = int(YLE)-1
                zz = int(ZLE)-1
                
                Point = Draft.makePoint(X = row[xx], Y = row[yy], Z = row[zz], color = None, name = " " + str(row[pn]), point_size = 3)

FreeCADGui.addCommand('Import Point File',ImportPointFile()) 