from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QApplication

from ..views.SimulationAlertsDialog_ui import Ui_SimAlertsDialog

class SimulationAlertsDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_SimAlertsDialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QApplication.instance().icon)

        header = self.ui.tableWidgetAlerts.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.hide()

    def displayAlerts(self, simRes):
        self.ui.tableWidgetAlerts.setRowCount(0) # Clear the table
        if len(simRes.alerts) == 0:
            return

        self.ui.tableWidgetAlerts.setRowCount(len(simRes.alerts))
        for row, alert in enumerate(simRes.alerts):
            self.ui.tableWidgetAlerts.setItem(row, 0, QTableWidgetItem(alert.level))
            self.ui.tableWidgetAlerts.setItem(row, 1, QTableWidgetItem(alert.type))
            self.ui.tableWidgetAlerts.setItem(row, 2, QTableWidgetItem(alert.location))
            self.ui.tableWidgetAlerts.setItem(row, 3, QTableWidgetItem(alert.description))
        self.show()
