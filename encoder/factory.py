from encoder.interface import EncoderInterface
from encoder.Watchdog import PositionWatchdog
from encoder.File import File, AbstractCommunication
from encoder.heidenhain_encoder import EncoderFactory
from e21_util.paths import Paths


class Factory(object):
    def __init__(self, encoder_factory=None):
        if not isinstance(encoder_factory, EncoderFactory):
            encoder_factory = EncoderFactory()

        self._fac = encoder_factory

    def get_encoder_factory(self):
        return self._fac

    def get_communication(self):
        return File(Paths().ENCODER_PATH)

    def get_watchdog(self):
        return PositionWatchdog(self.get_communication(), self._fac)

    def get_interface(self, comm=None):
        if not isinstance(comm, AbstractCommunication) and not comm is None:
            raise RuntimeError("Given communication is not an instance of AbstractCommunication")

        if comm is None:
            comm = self.get_communication()

        return EncoderInterface(comm)
