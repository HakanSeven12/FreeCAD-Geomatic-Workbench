import FreeCAD, FreeCADGui
from pivy import coin
import os


class AddTriangle:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap': Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Add Triangle",
        'ToolTip': "Add a triangle to selected surface."
    }

    def __init__(self):
        # todo : does not make sense
        print("Add Triangle Added")

    def get_resources(self):
        # Return the command resources dictionary
        return self.resources

    def activated(self):
        FreeCADGui.runCommand("Mesh_AddFacet")


# todo : does not make sense
FreeCADGui.addCommand('Add Triangle', AddTriangle())


class DeleteTriangle:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap' : Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Delete Triangle",
        'ToolTip': "Delete triangles from selected surface."
    }

    def __init__(self):
        print ("Delete Triangle Added")

    def get_resources(self):
        # Return the command resources dictionary
        return self.resources

    @staticmethod
    def activated():
        FreeCADGui.runCommand("Mesh_RemoveComponents")


FreeCADGui.addCommand('Delete Triangle',DeleteTriangle())


class SwapEdge:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap': Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Swap Edge",
        'ToolTip': "Swap Edge of selected surface."
    }

    def __init__(self):
        # todo : does not make sense
        print("Swap Edge Added")

    def get_resources(self):
        # Return the command resources dictionary
        return self.resources

    def activated(self):
        self.face_indexes = []
        self.mc = FreeCADGui.ActiveDocument.ActiveView.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(),
                                                                            self.swap_edge)

    def swap_edge(self, cb):
        event = cb.getEvent()
        if event.getButton() == coin.SoMouseButtonEvent.BUTTON2 and event.getState() == coin.SoMouseButtonEvent.DOWN:
            FreeCADGui.ActiveDocument.ActiveView.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(),
                                                                         self.mc)
        if event.getButton() == coin.SoMouseButtonEvent.BUTTON1 and event.getState() == coin.SoMouseButtonEvent.DOWN:
            pp = cb.getPickedPoint()

            if not pp is None:
                detail = pp.getDetail()

                if detail.isOfType(coin.SoFaceDetail.getClassTypeId()):
                    face_detail = coin.cast(detail, str(detail.getTypeId().getName()))
                    index = face_detail.getFaceIndex()
                    self.face_indexes.append(index)

                    if len(self.face_indexes) == 2:
                        surface = FreeCADGui.Selection.getSelection()[-1]
                        copy_mesh = surface.Mesh.copy()

                        try:
                            copy_mesh.swapEdge(self.face_indexes[0], self.face_indexes[1])
                        except:
                            pass

                        surface.Mesh = copy_mesh
                        self.face_indexes.clear()


# todo : does not make sense
FreeCADGui.addCommand('Swap Edge', SwapEdge())


class SmoothSurface:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap': Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Smooth Surface",
        'ToolTip': "Smooth selected surface."
    }

    def __init__(self):
        # todo : does not make sense
        print("Smooth Surface Added")

    def get_resources(self):
        # Return the command resources dictionary
        return self.resources

    @staticmethod
    def activated():
        surface = FreeCADGui.Selection.getSelection()[0]
        surface.Mesh.smooth()


# todo : does not make sense
FreeCADGui.addCommand('Smooth Surface',SmoothSurface())
