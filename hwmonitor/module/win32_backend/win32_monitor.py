from hwmonitor.backend.backend import Backend
from hwmonitor.backend.backend_error import NoBackendFoundError
from hwmonitor.monitors.monitor import Monitor, MonitorOrientation


class Win32Monitor(Monitor):

    def __init__(self,
                 device_name='',
                 monitor_name='',
                 friendly_monitor_name='',
                 display_adapter='',
                 screen_width=0,
                 screen_height=0,
                 position_x=0,
                 position_y=0,
                 orientation=MonitorOrientation.Landscape,
                 primary=False):
        super().__init__(device_name=device_name,
                         monitor_name=monitor_name,
                         friendly_monitor_name=friendly_monitor_name,
                         display_adapter=display_adapter,
                         screen_width=screen_width,
                         screen_height=screen_height,
                         position_x=position_x,
                         position_y=position_y,
                         orientation=orientation,
                         primary=primary)
        self.backend = None

    def set_backend(self, backend: Backend):
        self.backend = backend

    def __apply_changes__(self):
        if self.backend:
            self.backend.set_monitor_position(self.device_name, self.position_x, self.position_y, reset=False)
            return True
        else:
            raise NoBackendFoundError('Win32Monitor requires an backend')
