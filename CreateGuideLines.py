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
        self.IPFui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        #To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateGuideLines)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)
        self.IPFui.CreateGroupChB.stateChanged.connect(self.CreateNewGroup)
        self.IPFui.AlignmentCB.currentIndexChanged.connect(self.ListGuideLinesGroups)

   def GetResources(self):
        return {'MenuText': 'Create Guide Lines', 'ToolTip': 'Create guide lines for sections.'}

   def Activated(self):
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

   def ListGuideLinesGroups(self):
        #List Guide Lines Groups
        self.IPFui.GuideLinesCB.clear()
        Index = self.IPFui.AlignmentCB.currentIndex()
        SelectedAlignment = self.AlignmentList[Index]
        AlignmentGLGName = SelectedAlignment + "_Guide_Lines"
        print (AlignmentGLGName)
        AlignmentGLG = FreeCAD.ActiveDocument.getObject(AlignmentGLGName)
        print (AlignmentGLG.Name)
        SelectedGLG = AlignmentGLG.Group
        GLGOutList = AlignmentGLG.OutList
        self.GuideLineList = []
        Count = 0

        for i in GLGOutList:
            self.GuideLineList.append(SelectedGLG[Count].Name)
            GLGName = SelectedGLG[Count].Label
            self.IPFui.GuideLinesCB.addItem(str(GLGName))
            Count = Count + 1

   def CreateNewGroup(self):
        if self.IPFui.CreateGroupChB.isChecked():
            self.IPFui.GuideLinesCB.setEditable(True)
        else:
            self.IPFui.GuideLinesCB.setEditable(False)

   def CreateGuideLines(self):
        L = self.IPFui.LeftLengthLE.text()
        R = self.IPFui.RightLengthLE.text()
        LL = int(L)*(-1000)
        RL = int(R)*1000

        Index = self.IPFui.AlignmentCB.currentIndex()
        AlignmentName = self.AlignmentList[Index]
        Alignment = FreeCAD.ActiveDocument.getObjectsByLabel(AlignmentName+" Alignment")

        pointsDirection  = []
        pointsDirection = Alignment.discretize(Number=500)
        v=pointsDirection[0].sub(pointsDirection[1])
        r=App.Rotation(FreeCAD.Vector(0,0,1),v)

        pl=FreeCAD.Placement()
        pl.Rotation.Q = r.Q
        pl.Base = pointsDirection[0]
        GuideLine.Placement = pl
        points = [FreeCAD.Vector(LL, 0.0, 0.0),FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Vector(RL, 0.0, 0.0)]
        GuideLine = Draft.makeWire(points,placement=pl,closed=False,face=False,support=None)
        del pointsDirection[:]
        print ("test")

FreeCADGui.addCommand('Create Guide Lines',CreateGuideLines()) 
