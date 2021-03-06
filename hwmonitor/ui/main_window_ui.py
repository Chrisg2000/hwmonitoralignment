from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QDialogButtonBox, QSizePolicy

from hwmonitor.ui.common.monitor_info_box_ui import UiMonitorInfoBox
from hwmonitor.ui.widgets.overview.vscreen_overview import VScreenOverview
from hwmonitor.vscreen.vscreen import VScreen


class UiMainWindow:

    def __init__(self, window: QMainWindow, vscreen: VScreen):
        self.window = window
        self.vscreen = vscreen

        window.setWindowFlags(Qt.Window
                              | Qt.MSWindowsFixedSizeDialogHint
                              | Qt.WindowMinimizeButtonHint
                              | Qt.WindowCloseButtonHint
                              | Qt.CustomizeWindowHint)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(QVBoxLayout())
        self.centralWidget.layout().setContentsMargins(0, 0, 0, 0)
        window.setCentralWidget(self.centralWidget)

        self.monitor_overview_widget = VScreenOverview(vscreen, window)
        self.centralWidget.layout().addWidget(self.monitor_overview_widget)

        self.sub_widget = QWidget()
        self.sub_layout = QVBoxLayout()
        self.sub_widget.setLayout(self.sub_layout)
        self.centralWidget.layout().addWidget(self.sub_widget)

        self.monitor_info_group = QGroupBox()
        self.monitor_info_group.setLayout(QHBoxLayout())

        for monitor in self.vscreen.monitor_order:
            info_box = QGroupBox("Monitor Information")
            info_box.ui = UiMonitorInfoBox(info_box, monitor)
            self.monitor_info_group.layout().addWidget(info_box)
        self.sub_layout.addWidget(self.monitor_info_group)

        self.button_group = QDialogButtonBox(Qt.Horizontal)
        self.button_group.setStyleSheet('* { button-layout: 2 }')
        self.close_button = self.button_group.addButton("Close", QDialogButtonBox.RejectRole)
        self.adjust_button = self.button_group.addButton("Adjust", QDialogButtonBox.ActionRole)
        self.about_button = self.button_group.addButton("About", QDialogButtonBox.HelpRole)
        self.sub_layout.addWidget(self.button_group)

        self.translate_ui()

    def translate_ui(self):
        self.window.setWindowTitle("HwMonitorAlignment")
        self.monitor_info_group.setTitle("Monitor Setup Information")
        self.close_button.setText("Close")
        self.adjust_button.setText("Adjust")
