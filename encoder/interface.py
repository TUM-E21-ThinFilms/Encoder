import time
from encoder.File import AbstractCommunication


class EncoderInterface(object):

    PARAMETER_TIME_DIFF = 5 # more than 5 sec time diff is not allowed
    PARAMETER_ANGLE_DIFF = 13
    PARAMETER_ANGLE_TOL = 0.1

    def __init__(self, comm):
        if not isinstance(comm, AbstractCommunication):
            raise RuntimeError("comm must be an instance of AbstractCommunication")

        self._comm = comm

    def get_data(self):
        return self._comm.load()

    def _check_time(self, data):
        diff = time.time() - data.get_time()
        if abs(diff) >= self.PARAMETER_TIME_DIFF:
            raise RuntimeError("No new encoder data given (Too old)")

    def _check_reference_theta(self, data):
        if not data.has_reference_theta():
            raise RuntimeError("No reference given, cannot calculate angle")

        ref = data.get_references_theta()
        if not len(ref) == 2:
            raise RuntimeError("Should have exactly two reference positions")

        diff = abs(ref[0] - ref[1])

        if abs(diff - self.PARAMETER_ANGLE_DIFF) > self.PARAMETER_ANGLE_TOL:
            raise RuntimeError("Given reference angles are not in range")

    def get_angle(self):
        data = self.get_data()
        self._check_time(data)
        self._check_reference_theta(data)

        return data.get_position_theta()

    def _check_reference_z(self, data):
        pass
        #todo

    def get_z(self):
        data = self.get_data()
        self._check_time(data)
        self._check_reference_z(data)

        return data.get_position_z()