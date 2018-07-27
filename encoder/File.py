from encoder.DataEncoder import DataEncoder
from e21_util.lock import ENCODER_FILE_LOCK

class AbstractCommunication(object):
    """
    :return: Data
    """
    def load(self):
        raise RuntimeError('No implementation')

    def save(self, data):
        raise RuntimeError('No implementation')

class File(AbstractCommunication):
    def __init__(self, filepath):
        self._path = filepath
        self._encoder = DataEncoder()
        self._lock = ENCODER_FILE_LOCK()

    def load(self):
        """

        :return: encoder.DataEncoder.Data
        """
        with self._lock:
            with open(self._path, 'r') as f:
                raw = f.read()
                if raw == "":
                    raise RuntimeError("No data in file found.")
                data = self._encoder.decode(raw)
                return data

    def save(self, data):
        with self._lock:
            with open(self._path, 'w') as f:
                raw = self._encoder.encode(data)
                f.write(raw)
                return True
