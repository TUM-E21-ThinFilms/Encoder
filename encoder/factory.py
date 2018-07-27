from encoder.interface import EncoderInterface
from encoder.Watchdog import PositionWatchdog
from encoder.File import File, AbstractCommunication
from e21_util.paths import Paths


class Factory(object):
    def __init__(self):
        pass

    def get_communication(self):
        return File(Paths().ENCODER_PATH)

    def get_watchdog(self):
        return PositionWatchdog(self.get_communication())

    def get_interface(self, comm=None):
        if not isinstance(comm, AbstractCommunication) and not comm is None:
            raise RuntimeError("Given communication is not an instance of AbstractCommunication")

        if comm is None:
            comm = self.get_communication()

        return EncoderInterface(comm)
