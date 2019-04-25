import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import Draft
import csv, os

class ImportPointFile:
    #Command to import point file which include survey data.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap'  : Path + '/Resources/Icons/ImportPointFile.svg',
        'MenuText': "Import Point File",
        'ToolTip' : "Import point file which include survey data."
    }

    def __init__(self):
        #Import *.ui file(s).
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/Resources/UI/ImportPointFile.ui")
        self.CPGui = FreeCADGui.PySideUic.loadUi(self.Path + "/Resources/UI/CreatePointGroup.ui")

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
        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()
        self.IPFui.FileNameL.setText("")
        self.IPFui.SubGroupListCB.clear()
        self.IPFui.SelectedFilesLW.clear()
        self.IPFui.PreviewTW.setRowCount(0)
        self.IPFui.PointGroupChB.setChecked(False)
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
        #Add point files to the list.
        self.FileList = QtGui.QFileDialog.getOpenFileNames(None, "Select one or more files to open", os.getenv("HOME"),'All Files (*.*)')
        self.IPFui.SelectedFilesLW.addItems(self.FileList[0])

    def RemoveFile(self):
        #Remove point files from list.
        listItems=self.IPFui.SelectedFilesLW.selectedItems() 
        for item in listItems:
           self.IPFui.SelectedFilesLW.takeItem(self.IPFui.SelectedFilesLW.row(item))

    def Preview(self):
        #Import UI variables.
        listItems=self.IPFui.SelectedFilesLW.selectedItems() 
        try:
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
        CNG = self.CPGui.PointGroupNameLE.text()
        SubGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",CNG)
        FreeCAD.ActiveDocument.Point_Groups.addObject(SubGroup)
        SubGroup.Label = self.CPGui.PointGroupNameLE.text()
        self.GroupList.append(SubGroup.Name)
        SubGroupName = SubGroup.Label
        self.IPFui.SubGroupListCB.addItem(str(SubGroupName))
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
        FreeCADGui.SendMsgToActiveView("ViewFit")

FreeCADGui.addCommand('Import Point File',ImportPointFile()) 
