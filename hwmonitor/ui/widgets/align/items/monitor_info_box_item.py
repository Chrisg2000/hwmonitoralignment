from PySide2.QtWidgets import QWidget

from hwmonitor.ui.common.monitor_info_box_ui import UiMonitorInfoBox
from hwmonitor.ui.graphics.graphics_window import GraphicsWindow


class MonitorInfoBoxItem(GraphicsWindow):

    def __init__(self, model, text='Display Information', parent=None):
        self.model = model
        self.widget = QWidget()
        self.ui = UiMonitorInfoBox(self.widget, monitor=self.model.monitor)

        super().__init__(self.widget, text, 0, parent)
