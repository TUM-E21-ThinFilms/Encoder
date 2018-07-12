from encoder.Watchdog import PositionWatchdog
from encoder.File import File
from e21_util.paths import Paths


class Factory(object):
    def __init__(self):
        pass

    def get_communication(self):
        return File(Paths().ENCODER_PATH)

    def get_watchdog(self):
        return PositionWatchdog(self.get_communication())
