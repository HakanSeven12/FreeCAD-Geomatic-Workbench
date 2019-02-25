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
        self.IPFui.CreateGroupChB.stateChanged.connect(self.CreateNewGroup)

   def GetResources(self):
        return {'MenuText': 'Import Point File', 'ToolTip': 'Import point file which include survey data.'}
  
   def Activated(self):
        self.IPFui.show()
        self.IPFui.SubGroupListCB.clear()
        SG = FreeCAD.ActiveDocument.Points.Group
        OutList = FreeCAD.ActiveDocument.Points.OutList
        self.GroupList = []
        Count = 0

        for i in OutList:
            self.GroupList.append(SG[Count].Name)
            SubGroupName = SG[Count].Label
            self.IPFui.SubGroupListCB.addItem(str(SubGroupName))
            Count = Count + 1

   def CreateNewGroup(self):
        if self.IPFui.CreateGroupChB.isChecked():
            self.IPFui.SubGroupListCB.setEditable(True)
        else:
            self.IPFui.SubGroupListCB.setEditable(False)

   def BrowseFile(self):
        self.FilePath = QtGui.QFileDialog.getOpenFileName(None, 'Select File', "", 'All Files (*.*)')
        self.head, self.tail = os.path.split(self.FilePath[0])
        self.IPFui.BrowseLE.setText(self.FilePath[0])

   def ImportFile(self):
        #Import UI variables
        PointNameLE = self.IPFui.PointNameLE.text()
        XLE = self.IPFui.XLE.text()
        YLE = self.IPFui.YLE.text()
        ZLE = self.IPFui.ZLE.text()
        Index = self.IPFui.SubGroupListCB.currentIndex()
        CNG = self.IPFui.SubGroupListCB.currentText()
        SPG = self.GroupList[Index]

        #Create Group under Points
        if self.IPFui.CreateGroupChB.isChecked():
            SubGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",CNG)
            FreeCAD.ActiveDocument.Points.addObject(SubGroup)
        else:
            SubGroup = FreeCAD.ActiveDocument.getObject(SPG)
			
        #Read Points from file
        File=open(self.head +"/"+ self.tail, 'r')
        reader = csv.reader(File, delimiter=" ")
        for i, row in enumerate( reader ):
            pn = int(PointNameLE)-1
            xx = int(XLE)-1
            yy = int(YLE)-1
            zz = int(ZLE)-1
                
            Point = Draft.makePoint(X = float(row[xx])*1000, Y = float(row[yy])*1000, Z = float(row[zz])*1000, color = (0.37,0.69,0.22) , name = "Point", point_size = 3)
            Point.Label = str(row[pn])
            SubGroup.addObject(Point)
        FreeCADGui.SendMsgToActiveView("ViewFit")

FreeCADGui.addCommand('Import Point File',ImportPointFile()) 
