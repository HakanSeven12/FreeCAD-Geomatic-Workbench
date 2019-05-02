import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import Draft
import os

class CreateGuideLines:

    def __init__(self):
        #Import *.ui file(s)
        self.Path = os.path.dirname(os.path.abspath(__file__))
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/Resources/UI/CreateGuideLines.ui")

        #To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateGuideLines)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)
        #self.IPFui.CreateGroupChB.stateChanged.connect(self.CreateNewGroup)
        #self.IPFui.AlignmentCB.currentIndexChanged.connect(self.ListGuideLinesGroups)

    def GetResources(self):
        return {'MenuText': 'Create Guide Lines', 'ToolTip': 'Create guide lines for sections.'}

    def Activated(self):
        try:
            self.GLGroups = FreeCAD.ActiveDocument.Guide_Lines
        except:
            self.GLGroups = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Guide_Lines')
            self.GLGroups.Label = "Guide Lines"

        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()

        #List Alignments.
        self.IPFui.AlignmentCB.clear()
        SelectedAG = FreeCAD.ActiveDocument.Alignments.Group
        AGOutList = FreeCAD.ActiveDocument.Alignments.OutList
        self.AlignmentList = []
        Count = 0

        for i in AGOutList:
             self.AlignmentList.append(SelectedAG[Count].Name)
             AlignmentName = SelectedAG[Count].Label
             self.IPFui.AlignmentCB.addItem(str(AlignmentName))
             Count = Count + 1

    def CreateGuideLines(self):
        L = self.IPFui.LeftLengthLE.text()
        R = self.IPFui.RightLengthLE.text()
        Index = self.IPFui.AlignmentCB.currentIndex()
        AlignmentName = self.AlignmentList[Index]
        Alignment = FreeCAD.ActiveDocument.getObject(AlignmentName)
        Increment = self.IPFui.IncrementLE.text()

        Stations = []
        Start = Alignment.Proxy.model.data['meta']['StartStation']
        Length = Alignment.Proxy.model.data['meta']['Length']
        End = Start + Length/1000

        for i in range(round(Start), round(End)):
            if i % int(Increment) == 0:
                Stations.append(i)
        Stations.pop(0)

        Geometry = Alignment.Proxy.model.data['geometry']
        for Geo in Geometry:
            Stations.append(Geo.get('StartStation'))

        Stations.append(round(End,3))
        Stations.sort()

        for Station in Stations:
            coord, vec = Alignment.Proxy.model.get_orthogonal( Station, "Left")
            LeftEnd = coord.add(FreeCAD.Vector(vec).multiply(int(L)*1000))

            coord, vec = Alignment.Proxy.model.get_orthogonal( Station, "Right")
            RightEnd = coord.add(FreeCAD.Vector(vec).multiply(int(R)*1000))

            GuideLine = Draft.makeWire([LeftEnd,RightEnd])
            GuideLine.Label = str(round(Station,3))
            self.GLGroups.addObject(GuideLine)

FreeCADGui.addCommand('Create Guide Lines',CreateGuideLines())
