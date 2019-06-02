import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import csv, os
import Draft


class ImportPointFile:
    # Command to import point file which includes survey data.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap': Path + '/../Resources/Icons/ImportPointFile.svg',
        'MenuText': "Import Point File",
        'ToolTip': "Import point file which includes survey data."
    }

    def __init__(self):
        # Import *.ui file(s).
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/ImportPointFile.ui")
        self.CPGui = FreeCADGui.PySideUic.loadUi(self.Path + "/create_point_group.ui")

        # todo :
        self.IPFui.AddB.clicked.connect(self.add_file)
        self.IPFui.RemoveB.clicked.connect(self.remove_file)
        self.IPFui.SelectedFilesLW.itemSelectionChanged.connect(self.preview)
        self.IPFui.PointGroupChB.stateChanged.connect(self.activate_points_groups)
        self.IPFui.CreateGroupB.clicked.connect(self.load_cp_gui)
        self.IPFui.OKB.clicked.connect(self.import_file)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)
        self.CPGui.OkB.clicked.connect(self.create_point_group)
        self.CPGui.CancelB.clicked.connect(self.CPGui.close)

    def get_resources(self):
        # Return the command resources dictionary.
        return self.Resources

    def activated(self):
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

    def add_file(self):
        # Add point files to the list.
        self.FileList = QtGui.QFileDialog.getOpenFileNames(None, "Select one or more files to open", os.getenv("HOME"), 'All Files (*.*)')
        self.IPFui.SelectedFilesLW.addItems(self.FileList[0])

    def remove_file(self):
        # Remove point files from list.
        for item in self.IPFui.SelectedFilesLW.selectedItems():
           self.IPFui.SelectedFilesLW.takeItem(self.IPFui.SelectedFilesLW.row(item))

    def preview(self):
        # Import UI variables.
        list_items = self.IPFui.SelectedFilesLW.selectedItems()
        if list_items:
            head, tail = os.path.split(list_items[0].text())
            self.IPFui.FileNameL.setText(tail)
            self.IPFui.PreviewTW.setRowCount(0)

            point_name = self.IPFui.PointNameLE.text()
            northing = self.IPFui.NorthingLE.text()
            easting = self.IPFui.EastingLE.text()
            elevation = self.IPFui.ElevationLE.text()
            description = self.IPFui.DescriptionLE.text()

            # Show selected file preview.
            file = open(list_items[0].text(), 'r')

            if self.IPFui.DelimiterCB.currentText() == "Space":
                reader = csv.reader(file, delimiter=' ')
            elif self.IPFui.DelimiterCB.currentText() == "Comma":
                reader = csv.reader(file, delimiter=',')

            for i, row in enumerate(reader):
                pn = int(point_name)-1
                n = int(northing)-1
                e = int(easting)-1
                z = int(elevation)-1
                d = int(description)-1

                num_rows = self.IPFui.PreviewTW.rowCount()
                self.IPFui.PreviewTW.insertRow(num_rows)

                self.IPFui.PreviewTW.setItem(num_rows, 0, QtGui.QTableWidgetItem(row[pn]))
                self.IPFui.PreviewTW.setItem(num_rows, 1, QtGui.QTableWidgetItem(row[n]))
                self.IPFui.PreviewTW.setItem(num_rows, 2, QtGui.QTableWidgetItem(row[e]))
                self.IPFui.PreviewTW.setItem(num_rows, 3, QtGui.QTableWidgetItem(row[z]))
                try:
                    self.IPFui.PreviewTW.setItem(num_rows, 4, QtGui.QTableWidgetItem(row[d]))
                except:
                    pass

    def activate_points_groups(self):
        # When QCheckBox status changed do the following options.
        if self.IPFui.PointGroupChB.isChecked():
            self.IPFui.SubGroupListCB.setEnabled(True)
            self.IPFui.CreateGroupB.setEnabled(True)
        else:
            self.IPFui.SubGroupListCB.setEnabled(False)
            self.IPFui.CreateGroupB.setEnabled(False)

    def load_cp_gui(self):
        # Load Create Point Group UI.
        self.CPGui.setParent(self.IPFui)
        self.CPGui.setWindowFlags(QtCore.Qt.Window)
        self.CPGui.show()

    def create_point_group(self):
        # Create new point group.
        new_group_name = self.CPGui.PointGroupNameLE.text()
        new_group = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",new_group_name)
        FreeCAD.ActiveDocument.Point_Groups.addObject(new_group)
        self.IPFui.SubGroupListCB.addItem(new_group_name)
        self.GroupList.append(new_group.Name)
        new_group.Label = new_group_name
        self.CPGui.close()

    def import_file(self):
        # Import UI variables.
        point_name = self.IPFui.PointNameLE.text()
        northing = self.IPFui.NorthingLE.text()
        easting = self.IPFui.EastingLE.text()
        elevation = self.IPFui.ElevationLE.text()
        # description = self.IPFui.DescriptionLE.text()  # is not used
        index = self.IPFui.SubGroupListCB.currentIndex()

        if self.IPFui.PointGroupChB.isChecked():
            spg = self.GroupList[index]
            sub_group = FreeCAD.ActiveDocument.getObject(spg)
        else:
            sub_group = FreeCAD.ActiveDocument.Points

        # Read Points from file.
        items_ = []
        for i in range(self.IPFui.SelectedFilesLW.count()):
            items_.append(self.IPFui.SelectedFilesLW.item(i))
        labels = [i.text() for i in items_]
        for FilePath in labels:
            file = open(FilePath, 'r')
            if self.IPFui.DelimiterCB.currentText() == "Space":
                reader = csv.reader(file, delimiter=' ')
            elif self.IPFui.DelimiterCB.currentText() == "Comma":
                reader = csv.reader(file, delimiter=',')
            for i, row in enumerate(reader):
                pn = int(point_name)-1
                n = int(northing)-1
                e = int(easting)-1
                z = int(elevation)-1

                point = Draft.makePoint(X=float(row[e])*1000, Y=float(row[n])*1000, Z=float(row[z])*1000,
                                        color=(0.37, 0.69, 0.22), name="Point", point_size=3)
                point.Label = str(row[pn])
                sub_group.addObject(point)
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        self.IPFui.close()

FreeCADGui.addCommand('Import Point File',ImportPointFile())
