import FreeCAD, FreeCADGui
from pivy import coin
import os

class AddTriangle:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap'  : Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Add Triangle",
        'ToolTip' : "Add a triangle to selected surface."
    }

    def __init__(self):
        print ("Add Triangle Added")

    def GetResources(self):
        #Return the command resources dictionary
        return self.resources

    def Activated(self):
        FreeCADGui.runCommand("Mesh_AddFacet")

FreeCADGui.addCommand('Add Triangle',AddTriangle())

class DeleteTriangle:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap'  : Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Delete Triangle",
        'ToolTip' : "Delete triangles from selected surface."
    }

    def __init__(self):
        print ("Delete Triangle Added")

    def GetResources(self):
        #Return the command resources dictionary
        return self.resources

    def Activated(self):
        FreeCADGui.runCommand("Mesh_RemoveComponents")

FreeCADGui.addCommand('Delete Triangle',DeleteTriangle())

class SwapEdge:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap'  : Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Swap Edge",
        'ToolTip' : "Swap Edge of selected surface."
    }

    def __init__(self):

        print ("Swap Edge Added")

    def GetResources(self):
        #Return the command resources dictionary
        return self.resources

    def Activated(self):
        self.FaceIndexes = []
        self.MC = FreeCADGui.ActiveDocument.ActiveView.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.SwapEdge)

    def SwapEdge(self,cb):
        event = cb.getEvent()
        if event.getButton() == coin.SoMouseButtonEvent.BUTTON2 and event.getState() == coin.SoMouseButtonEvent.DOWN:
            FreeCADGui.ActiveDocument.ActiveView.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.MC)
        if event.getButton() == coin.SoMouseButtonEvent.BUTTON1 and event.getState() == coin.SoMouseButtonEvent.DOWN:
            pp = cb.getPickedPoint()
            if not pp is None:
                detail = pp.getDetail()
                if detail.isOfType(coin.SoFaceDetail.getClassTypeId()):
                    face_detail = coin.cast(detail, str(detail.getTypeId().getName()))
                    index = face_detail.getFaceIndex()
                    self.FaceIndexes.append(index)
                    if len(self.FaceIndexes) == 2:
                        Surface = FreeCADGui.Selection.getSelection()[-1]
                        CopyMesh = Surface.Mesh.copy()
                        try:
                            CopyMesh.swapEdge(self.FaceIndexes[0],self.FaceIndexes[1])
                        except:
                            pass
                        Surface.Mesh = CopyMesh
                        self.FaceIndexes.clear()

FreeCADGui.addCommand('Swap Edge',SwapEdge())

class SmoothSurface:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap'  : Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Smooth Surface",
        'ToolTip' : "Smooth selected surface."
    }

    def __init__(self):

        print ("Smooth Surface Added")

    def GetResources(self):
        #Return the command resources dictionary
        return self.resources

    def Activated(self):
        Surface = FreeCADGui.Selection.getSelection()[0]
        Surface.Mesh.smooth()

FreeCADGui.addCommand('Smooth Surface',SmoothSurface())
