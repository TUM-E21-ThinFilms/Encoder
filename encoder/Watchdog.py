from encoder.DataEncoder import Data, ErrorData
from encoder.File import AbstractCommunication
from e21_util.simultaneous import StoppableThread, StopException
from encoder.heidenhain_encoder import EncoderFactory

class PositionWatchdog(StoppableThread):
    def __init__(self, comm):
        super(PositionWatchdog, self).__init__()
        if not isinstance(comm, AbstractCommunication):
            raise RuntimeError("comm must be an instance of AbstractCommunication")
        self._comm = comm
        self._initialized = False
        self._fac = EncoderFactory()
        self._encoder = self._fac.get_encoder()
        self._z = self._fac.get_z()
        self._theta = self._fac.get_theta()

    def get_encoder(self):
        return self._encoder

    def get_z(self):
        return self._z

    def get_theta(self):
        return self._theta

    def initialize(self):
        if self._initialized is True:
            return

        self._fac.initialize()
        self._encoder.clear_buffer()

    def _on_stop(self):
        self._encoder.disconnect()

    def do_execute(self):
        self.initialize()

        try:
            self._encoder.read()

            data = Data({})

            self._set_theta(data)
            self._set_z(data)

            self._comm.save(data)
        except KeyboardInterrupt as e:
            raise e
        except StopException as e:
            raise e
        except BaseException as e:
            self._comm.save(ErrorData({}, e))

    def _set_theta(self, data):
        try:
            data.set_position_theta(self._theta.get_angle())
            data.set_trigger_count(self._theta.get_trigger())
            data.set_reference_theta(self._theta.get_reference())
        except RuntimeError as e:
            data.add_exception(e)

    def _set_z(self, data):
        try:
            data.set_position_z(self._z.get_position())
            data.set_reference_z(self._z.get_reference())
        except RuntimeError as e:
            data.add_exception(e)
