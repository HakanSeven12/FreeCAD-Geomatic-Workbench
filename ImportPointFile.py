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
        self.IPFui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        #To Do List
        self.IPFui.AddB.clicked.connect(self.AddFile)
        self.IPFui.RemoveB.clicked.connect(self.RemoveFile)
        self.IPFui.SelectedFilesLW.itemSelectionChanged.connect(self.Preview)
        self.IPFui.CreateGroupChB.stateChanged.connect(self.CreateNewGroup)
        self.IPFui.OKB.clicked.connect(self.ImportFile)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

   def GetResources(self):
        return {'MenuText': 'Import Point File', 'ToolTip': 'Import point file which include survey data.'}
  
   def Activated(self):
        self.IPFui.show()
        self.IPFui.SubGroupListCB.clear()
        SG = FreeCAD.ActiveDocument.Point_Groups.Group
        OutList = FreeCAD.ActiveDocument.Point_Groups.OutList
        self.GroupList = []
        Count = 0

        for i in OutList:
            self.GroupList.append(SG[Count].Name)
            SubGroupName = SG[Count].Label
            self.IPFui.SubGroupListCB.addItem(str(SubGroupName))
            Count = Count + 1

   def AddFile(self):
        self.FileList = QtGui.QFileDialog.getOpenFileNames(None, "Select one or more files to open", os.getenv("HOME"),'All Files (*.*)')
        self.IPFui.SelectedFilesLW.addItems(self.FileList[0])

   def RemoveFile(self):
        listItems=self.IPFui.SelectedFilesLW.selectedItems() 
        for item in listItems:
           self.IPFui.SelectedFilesLW.takeItem(self.IPFui.SelectedFilesLW.row(item))

   def Preview(self):
        listItems=self.IPFui.SelectedFilesLW.selectedItems() 
        head, tail = os.path.split(listItems[0].text())
        self.IPFui.FileNameL.setText(tail)
        #self.IPFui.PreviewLW.clear()
        self.IPFui.PreviewLW.setRowCount(0)

        PointName = self.IPFui.PointNameLE.text()
        Northing = self.IPFui.NorthingLE.text()
        Easting = self.IPFui.EastingLE.text()
        Elevation = self.IPFui.ElevationLE.text()
        Description = self.IPFui.DescriptionLE.text()

        File=open(listItems[0].text(), 'r')
        reader = csv.reader(File, delimiter=" ")
        for i, row in enumerate( reader ):
            PN = int(PointName)-1
            N = int(Northing)-1
            E = int(Easting)-1
            Z = int(Elevation)-1
            D = int(Description)-1

            numRows = self.IPFui.PreviewLW.rowCount()
            self.IPFui.PreviewLW.insertRow(numRows)

            self.IPFui.PreviewLW.setItem(numRows, 0, QtGui.QTableWidgetItem(row[PN]))
            self.IPFui.PreviewLW.setItem(numRows, 1, QtGui.QTableWidgetItem(row[N]))
            self.IPFui.PreviewLW.setItem(numRows, 2, QtGui.QTableWidgetItem(row[E]))
            self.IPFui.PreviewLW.setItem(numRows, 3, QtGui.QTableWidgetItem(row[Z]))
            self.IPFui.PreviewLW.setItem(numRows, 4, QtGui.QTableWidgetItem(row[D]))

   def CreateNewGroup(self):
        if self.IPFui.CreateGroupChB.isChecked():
            self.IPFui.SubGroupListCB.setEditable(True)
        else:
            self.IPFui.SubGroupListCB.setEditable(False)

   def ImportFile(self):
        #Import UI variables
        PointName = self.IPFui.PointNameLE.text()
        Northing = self.IPFui.NorthingLE.text()
        Easting = self.IPFui.EastingLE.text()
        Elevation = self.IPFui.ElevationLE.text()
        Description = self.IPFui.DescriptionLE.text()
        Index = self.IPFui.SubGroupListCB.currentIndex()
        CNG = self.IPFui.SubGroupListCB.currentText()
        SPG = self.GroupList[Index]

        #Create Group under Points
        if self.IPFui.CreateGroupChB.isChecked():
            SubGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",CNG)
            FreeCAD.ActiveDocument.Point_Groups.addObject(SubGroup)
        else:
            SubGroup = FreeCAD.ActiveDocument.getObject(SPG)
			
        #Read Points from file
        Items = []
        for i in range(self.IPFui.SelectedFilesLW.count()):
            Items.append(self.IPFui.SelectedFilesLW.item(i))
        Labels = [i.text() for i in Items]
        for FilePath in Labels:
            File=open(FilePath, 'r')
            reader = csv.reader(File, delimiter=" ")
            for i, row in enumerate( reader ):
                PN = int(PointName)-1
                N = int(Northing)-1
                E = int(Easting)-1
                Z = int(Elevation)-1

                Point = Draft.makePoint(X = float(row[N])*1000, Y = float(row[E])*1000, Z = float(row[Z])*1000, color = (0.37,0.69,0.22) , name = "Point", point_size = 3)
                Point.Label = str(row[PN])
                SubGroup.addObject(Point)
        FreeCADGui.SendMsgToActiveView("ViewFit")

FreeCADGui.addCommand('Import Point File',ImportPointFile()) 
