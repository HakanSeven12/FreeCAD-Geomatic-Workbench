import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import os

class ExportPoints:
    """
    Command to export points to point file.
    """

    def __init__(self):
        """
        Constructor
        """

        # Get file path.
        self.Path = os.path.dirname(__file__)

        # Get *.ui files.
        self.EP = FreeCADGui.PySideUic.loadUi(self.Path + "/ExportPoints.ui")

        # Set icon,  menu text and tooltip.
        self.Resources = {
            'Pixmap': self.Path + '/../Resources/Icons/ExportPoints.svg',
            'MenuText': "Export Points",
            'ToolTip': "Export points to point file."
        }

        # To do.
        UI = self.EP
        UI.BrowseB.clicked.connect(self.FileDestination)
        UI.ExportB.clicked.connect(self.ExportPointsToFile)
        UI.CancelB.clicked.connect(UI.close)

        # Create empty point group names list.
        self.GroupList = []

    def GetResources(self):
        """
        Return the command resources dictionary.
        """

        return self.Resources

    def Activated(self):
        """
        Command activation method
        """

        # Show UI.
        UI = self.EP
        UI.setParent(FreeCADGui.getMainWindow())
        UI.setWindowFlags(QtCore.Qt.Window)
        UI.show()

        # Clear previous operation.
        UI.FileDestinationLE.clear()
        UI.PointGroupsLW.clear()
        PointGroups = FreeCAD.ActiveDocument.Point_Groups.Group

        for PointGroup in PointGroups:
            self.GroupList.append(PointGroup.Name)
            SubGroupName = PointGroup.Label
            UI.PointGroupsLW.addItem(SubGroupName)

    def FileDestination(self):
        """
        Get file destination.
        """

        UI = self.EP
        fileName = QtGui.QFileDialog.getSaveFileName(None, 'Save File', os.getenv("HOME"), Filter='*.txt')
        UI.FileDestinationLE.setText(fileName[0]+".txt")

    def ExportPointsToFile(self):
        """
        Export selected point group(s).
        """

        #Get UI variables.
        UI = self.EP
        PointName = UI.PointNameLE.text()
        Northing = UI.NorthingLE.text()
        Easting = UI.EastingLE.text()
        Elevation = UI.ElevationLE.text()
        Description = UI.DescriptionLE.text()
        Format = ["","","","",""]
        FileDestinationLE = UI.FileDestinationLE.text()

        #Set delimiter.
        if UI.DelimiterCB.currentText() == "Space":
            Delimiter = ' '
        elif UI.DelimiterCB.currentText() == "Comma":
            Delimiter=','

        #Create point file.
        File = open(FileDestinationLE, 'w')
        Counter = 1

        for SelectedIndex in UI.PointGroupsLW.selectedIndexes():
            Index = self.GroupList[SelectedIndex.row()]
            PointGroup = FreeCAD.ActiveDocument.getObject(Index)

            for Item in PointGroup.Points.Points:
                pn = str(Counter)
                xx = str(round(float(Item.x)/1000,3))
                yy = str(round(float(Item.y)/1000,3))
                zz = str(round(float(Item.z)/1000,3))
                Format[int(PointName)-1] = pn
                Format[int(Easting)-1] = xx
                Format[int(Northing)-1] = yy
                Format[int(Elevation)-1] = zz
                Format[int(Description)-1] = ""
                Counter += 1

                File.write(Format[0]+Delimiter+Format[1]+Delimiter+Format[2]+Delimiter+Format[3]+Delimiter+Format[4]+"\n")
        File.close()

FreeCADGui.addCommand('Export Points',ExportPoints())
