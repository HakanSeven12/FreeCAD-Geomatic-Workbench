import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import Draft, Part
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
        LL = int(L)*(-1000)
        RL = int(R)*1000

        Index = self.IPFui.AlignmentCB.currentIndex()
        AlignmentName = self.AlignmentList[Index]
        Alignment = FreeCAD.ActiveDocument.getObject(AlignmentName)

        pointsDirection  = []
        pointsDirection = Alignment.Proxy.model.discretize_geometry()
        for i in range(len(pointsDirection)-1):
            print (pointsDirection[i],pointsDirection[i+1])
            v=pointsDirection[i].sub(pointsDirection[i+1])
            r=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),v)

            pl=FreeCAD.Placement()
            pl.Rotation.Q = r.Q
            pl.Base = pointsDirection[i].Add(Alignment.Placement.Base)
            print (pl.Base)
            points = [FreeCAD.Vector(LL, 0.0, 0.0),FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Vector(RL, 0.0, 0.0)]
            GuideLine = Draft.makeWire(points,closed=False,face=False,support=None)
            GuideLine.Placement = pl


FreeCADGui.addCommand('Create Guide Lines',CreateGuideLines()) 
