import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import csv, os
import Draft

class ImportPointFile:
    #Command to import point file which include survey data.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap'  : Path + '/../Resources/Icons/ImportPointFile.svg',
        'MenuText': "Import Point File",
        'ToolTip' : "Import point file which include survey data."
    }

    def __init__(self):
        #Import *.ui file(s).
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/ImportPointFile.ui")
        self.CPGui = FreeCADGui.PySideUic.loadUi(self.Path + "/CreatePointGroup.ui")

        #To Do List.
        self.IPFui.AddB.clicked.connect(self.AddFile)
        self.IPFui.RemoveB.clicked.connect(self.RemoveFile)
        self.IPFui.SelectedFilesLW.itemSelectionChanged.connect(self.Preview)
        self.IPFui.PointGroupChB.stateChanged.connect(self.ActivatePointGroups)
        self.IPFui.CreateGroupB.clicked.connect(self.LoadCPGui)
        self.IPFui.OKB.clicked.connect(self.ImportFile)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)
        self.CPGui.OkB.clicked.connect(self.CreatePointGroup)
        self.CPGui.CancelB.clicked.connect(self.CPGui.close)

    def GetResources(self):
        #Return the command resources dictionary.
        return self.Resources

    def Activated(self):
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

        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()
        self.IPFui.FileNameL.setText("")
        self.IPFui.SubGroupListCB.clear()
        self.IPFui.SelectedFilesLW.clear()
        self.IPFui.PreviewTW.setRowCount(0)
        self.IPFui.PointGroupChB.setChecked(False)
        PointGroups = FreeCAD.ActiveDocument.Point_Groups.Group
        self.GroupList = []

        for PointGroup in PointGroups:
            self.GroupList.append(PointGroup.Name)
            SubGroupName = PointGroup.Label
            self.IPFui.SubGroupListCB.addItem(str(SubGroupName))

    def AddFile(self):
        #Add point files to the list.
        self.FileList = QtGui.QFileDialog.getOpenFileNames(None, "Select one or more files to open", os.getenv("HOME"),'All Files (*.*)')
        self.IPFui.SelectedFilesLW.addItems(self.FileList[0])

    def RemoveFile(self):
        #Remove point files from list.
        for item in self.IPFui.SelectedFilesLW.selectedItems():
           self.IPFui.SelectedFilesLW.takeItem(self.IPFui.SelectedFilesLW.row(item))

    def Preview(self):
        #Import UI variables.
        listItems=self.IPFui.SelectedFilesLW.selectedItems()
        if listItems:
            head, tail = os.path.split(listItems[0].text())
            self.IPFui.FileNameL.setText(tail)
            self.IPFui.PreviewTW.setRowCount(0)

            PointName = self.IPFui.PointNameLE.text()
            Northing = self.IPFui.NorthingLE.text()
            Easting = self.IPFui.EastingLE.text()
            Elevation = self.IPFui.ElevationLE.text()
            Description = self.IPFui.DescriptionLE.text()

            #Show selected file preview.
            File=open(listItems[0].text(), 'r')
            if self.IPFui.DelimiterCB.currentText() == "Space":
                reader = csv.reader(File, delimiter = ' ')
            elif self.IPFui.DelimiterCB.currentText() == "Comma":
                reader = csv.reader(File, delimiter=',')
            for i, row in enumerate( reader ):
                PN = int(PointName)-1
                N = int(Northing)-1
                E = int(Easting)-1
                Z = int(Elevation)-1
                D = int(Description)-1

                numRows = self.IPFui.PreviewTW.rowCount()
                self.IPFui.PreviewTW.insertRow(numRows)

                self.IPFui.PreviewTW.setItem(numRows, 0, QtGui.QTableWidgetItem(row[PN]))
                self.IPFui.PreviewTW.setItem(numRows, 1, QtGui.QTableWidgetItem(row[N]))
                self.IPFui.PreviewTW.setItem(numRows, 2, QtGui.QTableWidgetItem(row[E]))
                self.IPFui.PreviewTW.setItem(numRows, 3, QtGui.QTableWidgetItem(row[Z]))
                try:
                    self.IPFui.PreviewTW.setItem(numRows, 4, QtGui.QTableWidgetItem(row[D]))
                except:
                    pass

    def ActivatePointGroups(self):
        #When QCheckBox status changed do fallowing options.
        if self.IPFui.PointGroupChB.isChecked():
            self.IPFui.SubGroupListCB.setEnabled(True)
            self.IPFui.CreateGroupB.setEnabled(True)
        else:
            self.IPFui.SubGroupListCB.setEnabled(False)
            self.IPFui.CreateGroupB.setEnabled(False)

    def LoadCPGui(self):
        #Load Create Point Group UI.
        self.CPGui.setParent(self.IPFui)
        self.CPGui.setWindowFlags(QtCore.Qt.Window)
        self.CPGui.show()

    def CreatePointGroup(self):
        #Create new point group.
        NewGroupName = self.CPGui.PointGroupNameLE.text()
        NewGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",NewGroupName)
        FreeCAD.ActiveDocument.Point_Groups.addObject(NewGroup)
        self.IPFui.SubGroupListCB.addItem(NewGroupName)
        self.GroupList.append(NewGroup.Name)
        NewGroup.Label = NewGroupName
        self.CPGui.close()

    def ImportFile(self):
        #Import UI variables.
        PointName = self.IPFui.PointNameLE.text()
        Northing = self.IPFui.NorthingLE.text()
        Easting = self.IPFui.EastingLE.text()
        Elevation = self.IPFui.ElevationLE.text()
        Description = self.IPFui.DescriptionLE.text()
        Index = self.IPFui.SubGroupListCB.currentIndex()

        if self.IPFui.PointGroupChB.isChecked():
            SPG = self.GroupList[Index]
            SubGroup = FreeCAD.ActiveDocument.getObject(SPG)
        else:
            SubGroup = FreeCAD.ActiveDocument.Points

        #Read Points from file.
        Items = []
        for i in range(self.IPFui.SelectedFilesLW.count()):
            Items.append(self.IPFui.SelectedFilesLW.item(i))
        Labels = [i.text() for i in Items]
        for FilePath in Labels:
            File=open(FilePath, 'r')
            if self.IPFui.DelimiterCB.currentText() == "Space":
                reader = csv.reader(File, delimiter = ' ')
            elif self.IPFui.DelimiterCB.currentText() == "Comma":
                reader = csv.reader(File, delimiter=',')
            for i, row in enumerate( reader ):
                PN = int(PointName)-1
                N = int(Northing)-1
                E = int(Easting)-1
                Z = int(Elevation)-1

                Point = Draft.makePoint(X = float(row[E])*1000, Y = float(row[N])*1000, Z = float(row[Z])*1000, color = (0.37,0.69,0.22) , name = "Point", point_size = 3)
                Point.Label = str(row[PN])
                SubGroup.addObject(Point)
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        self.IPFui.close()

FreeCADGui.addCommand('Import Point File',ImportPointFile()) 
