from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

import motorlib.propellant

from ..views.PropMenu_ui import Ui_PropellantDialog


class PropellantMenu(QDialog):

    propellantEdited = pyqtSignal(dict)
    closed = pyqtSignal()

    def __init__(self, manager):
        QDialog.__init__(self)
        self.ui = Ui_PropellantDialog()
        self.ui.setupUi(self)

        self.manager = manager

        self.setupPropList()
        self.ui.listWidgetPropellants.currentItemChanged.connect(self.propSelected)

        self.ui.propEditor.changeApplied.connect(self.propEdited)
        self.ui.propEditor.closed.connect(self.editorClosed)

        self.ui.pushButtonNewPropellant.pressed.connect(self.newPropellant)
        self.ui.pushButtonDelete.pressed.connect(self.deleteProp)
        self.ui.pushButtonEdit.pressed.connect(self.editProp)

        self.setupButtons()

    def show(self):
        self.setupButtons()
        super().show()

    def setupButtons(self):
        self.ui.pushButtonEdit.setEnabled(False)
        self.ui.pushButtonDelete.setEnabled(False)
        self.repaint() # OSX needs this

    def setupPropList(self):
        self.ui.listWidgetPropellants.clear()
        self.ui.listWidgetPropellants.addItems(self.manager.getNames())

    def newPropellant(self):
        propName = "New Propellant"
        if propName in self.manager.getNames():
            propNumber = 1
            while propName + " " + str(propNumber) in self.manager.getNames():
                propNumber += 1
            propName = propName + " " + str(propNumber)
        newProp = motorlib.propellant.Propellant()
        newProp.setProperties({'name': propName,
                               'density': 1680,
                               'a': 3.517054143255937e-05,
                               'n': 0.3273,
                               't': 2800,
                               'm': 23.67,
                               'k': 1.21})
        self.manager.propellants.append(newProp)
        self.setupPropList()
        self.setupButtons()
        self.manager.savePropellants()
        self.ui.propEditor.loadProperties(newProp)
        self.repaint() # OSX needs this

    def deleteProp(self):
        del self.manager.propellants[self.ui.listWidgetPropellants.currentRow()]
        self.manager.savePropellants()
        self.setupPropList()
        self.setupButtons()
        self.repaint() # OSX needs this

    def editProp(self):
        prop = self.manager.propellants[self.ui.listWidgetPropellants.currentRow()]
        self.ui.propEditor.loadProperties(prop)
        self.toggleButtons(True)

    def propEdited(self, propDict):
        propNames = self.manager.getNames()
        if propDict['name'] in propNames:
            if propNames.index(propDict['name']) != self.ui.listWidgetPropellants.currentRow():
                print("Can't duplicate a prop name!")
                return
        self.manager.propellants[self.ui.listWidgetPropellants.currentRow()].setProperties(propDict)
        self.setupPropList()
        self.manager.savePropellants()
        self.repaint() # OSX needs this

    def propSelected(self):
        self.ui.pushButtonEdit.setEnabled(True)
        self.ui.pushButtonDelete.setEnabled(True)

    def editorClosed(self):
        self.toggleButtons(False)

    def toggleButtons(self, editing):
        self.ui.listWidgetPropellants.setEnabled(not editing)
        self.ui.pushButtonNewPropellant.setEnabled(not editing)
        self.ui.pushButtonEdit.setEnabled(not editing)
        self.ui.pushButtonDelete.setEnabled(not editing)
        self.ui.buttonBox.setEnabled(not editing)
        self.repaint() # OSX needs this

    def close(self):
        super().close()
        self.toggleButtons(False)
        self.ui.propEditor.cleanup()
        self.closed.emit()
