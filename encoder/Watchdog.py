from encoder.DataEncoder import Data, ErrorData
from encoder.File import AbstractCommunication
from e21_util.simultaneous import StoppableThread, StopException
from devcontroller.encoder import EncoderFactory
import time

class PositionWatchdog(StoppableThread):
    def __init__(self, comm):
        super(PositionWatchdog, self).__init__()
        if not isinstance(comm,  AbstractCommunication):
            raise RuntimeError("comm must be an instance of AbstractCommunication")
        self._comm = comm
        self._initialized = False
        self._fac = EncoderFactory()
        self._encoder = self._fac.get_encoder()
        self._z = self._fac.get_z()
        self._theta = self._fac.get_theta()
        
    def initialize(self):
        if self._initialized is True:
            return
        
        self._fac.initialize()

    def do_execute(self):
        self.initialize()

        try:
            self._encoder.clear_buffer()
            self._encoder.read()

            data = Data({})

            self._set_theta(data)
            self._set_z(data)

            self._comm.save(data)
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt) or isinstance(e, StopException):
                raise e
            self._comm.save(ErrorData({}))
        time.sleep(0.1)
            # continue...

    def _set_theta(self, data):
        data.set_position_theta(self._theta.get_angle())
        data.set_trigger_count(self._theta.get_trigger())
        data.set_reference_theta(self._theta.get_reference())

    def _set_z(self, data):
        data.set_position_z(self._z.get_position())
        data.set_reference_z(self._z.get_reference())
