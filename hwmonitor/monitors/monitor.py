import enum
from typing import Tuple

from hwmonitor.core.has_properties import HasProperties, Property, WriteOnceProperty
from hwmonitor.core.memento import Memento
from hwmonitor.core.signals import Signal


class MonitorOrientation(enum.IntEnum):
    Landscape = 0
    Portrait = 1
    FlippedLandscape = 2
    FlippedPortrait = 3


class MonitorSyncState(enum.Enum):
    SYNCHRONIZED = enum.auto()
    UNSYNCHRONIZED = enum.auto()


class Monitor(HasProperties, Memento):
    """A monitor is an item which models the data of an computer monitor registered in windows
    and showing on the virtual screen.

    The virtual screen is the bounding rectangle of all display monitors.

    Monitor provide **(and any subclass should do the same)** properties via
    HasProperties/Property specification.
    """
    device_name = WriteOnceProperty(default='')
    monitor_name = Property(default='')
    friendly_monitor_name = Property(default='')
    display_adapter = Property(default='')

    screen_width = Property(default=0)
    screen_height = Property(default=0)
    position_x = Property(default=0)
    position_y = Property(default=0)
    orientation = Property(default=MonitorOrientation.Landscape)
    primary = Property(default=False)

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
        """
        :param device_name: Unique device name associated with OS-based display device model
        :param monitor_name: OS related name of the associated display device
        :param friendly_monitor_name: Easy-to-understand name of the monitor
        :param display_adapter: Display Adapter of the display device
        :param screen_width: Width of the screen in pixels
        :param screen_height: Height of the screen in pixels
        :param position_x: x-position of the screen on the virtual screen in pixel-coordinates
        :param position_y: y-position of the screen on the virtual screen in pixel-coordinates
        :param orientation: Real-world orientation of the display device
        :param primary: Whether the display device is the primary one or not
        """
        super().__init__()
        self.device_name = device_name
        self.monitor_name = monitor_name
        self.friendly_monitor_name = friendly_monitor_name
        self.display_adapter = display_adapter
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position_x = position_x
        self.position_y = position_y
        self.orientation = MonitorOrientation(orientation)
        self.primary = primary

        self._state = MonitorSyncState.SYNCHRONIZED

        self.pre_apply_changes = Signal()
        self.post_apply_changes = Signal()
        self.error_apply_changes = Signal()

        self.property_changed.connect(self._update_sync_state)

    def apply_changes(self):
        """Apply changes on the application monitor item into OS associated monitor model"""
        self.pre_apply_changes.emit()
        try:
            result = self.__apply_changes__()
            if not result:
                raise OSError
            self._state = MonitorSyncState.SYNCHRONIZED
            self.post_apply_changes.emit(self, result)
            return result
        except OSError as error:
            self.error_apply_changes.emit(self, error)

    def __apply_changes__(self):
        """Implement the monitor 'apply_changes' behavior.

        If execution is successful should return True, otherwise False.
        Function is also able to rise OSError-based exception to quit processing
        """
        return False

    @property
    def aspect_ratio(self) -> float:
        if self.screen_height == 0:
            raise ValueError("Invalid Monitor defined: Impossible height.")
        return self.screen_width / self.screen_height

    @property
    def position(self) -> Tuple[float, float]:
        return self.position_x, self.position_y

    @property
    def size(self) -> Tuple[int, int]:
        return self.screen_width, self.screen_height

    def create_memento(self):
        return (self.device_name,
                self.monitor_name,
                self.friendly_monitor_name,
                self.display_adapter,
                self.screen_width,
                self.screen_height,
                self.position_x,
                self.position_y,
                self.orientation,
                self.primary)

    def set_memento(self, memento):
        (self.device_name,
         self.monitor_name,
         self.friendly_monitor_name,
         self.display_adapter,
         self.screen_width,
         self.screen_height,
         self.position_x,
         self.position_y,
         self.orientation,
         self.primary) = memento

    @classmethod
    def from_memento(cls, memento):
        monitor = Monitor()
        monitor.set_memento(memento)
        return monitor

    def _update_sync_state(self, instance, name, value):
        if getattr(self, name) == value:
            self._state = MonitorSyncState.UNSYNCHRONIZED
