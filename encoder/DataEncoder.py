import json
import time


class Data(object):
    KEY_TRIGGER_COUNT = 'trigger'
    KEY_THETA_POSITION = 'theta'
    KEY_THETA_REFERENCE = 'theta_ref'
    KEY_Z_POSITION = 'z'
    KEY_Z_REFERENCE = 'z_reference'
    KEY_ERROR = 'error'
    KEY_TIME = 'time'
    KEY_EXCEPTION = 'exception'

    def __init__(self, dict):
        if dict is None:
            dict = {}
        dict[self.KEY_TIME] = time.time()
        self._dict = dict

    def get_trigger_count(self):
        return self._dict[self.KEY_TRIGGER_COUNT]

    def get_position_theta(self):
        return self._dict[self.KEY_THETA_POSITION]

    def get_references_theta(self):
        try:
            return self._dict[self.KEY_THETA_REFERENCE]
        except:
            return None

    def has_reference_theta(self):
        return self.KEY_THETA_REFERENCE in self._dict

    def get_position_z(self):
        return self._dict[self.KEY_Z_POSITION]

    def get_references_z(self):
        try:
            return self._dict[self.KEY_Z_REFERENCE]
        except:
            return None

    def has_reference_z(self):
        return self.KEY_Z_REFERENCE in self._dict

    def get_dict(self):
        return self._dict

    def set_trigger_count(self, trigger_count):
        self._dict[self.KEY_TRIGGER_COUNT] = int(trigger_count)

    def set_position_theta(self, position):
        self._dict[self.KEY_THETA_POSITION] = float(position)

    def set_reference_theta(self, references):
        self._dict[self.KEY_THETA_REFERENCE] = references

    def set_position_z(self, position):
        self._dict[self.KEY_Z_POSITION] = float(position)

    def set_reference_z(self, references):
        self._dict[self.KEY_Z_REFERENCE] = references


class ErrorData(Data):
    def __init__(self, dict, exception=None):
        super(ErrorData, self).__init__(dict)

        self._dict[self.KEY_ERROR] = True
        if not exception is None:
            self._dict[self.KEY_EXCEPTION] = exception

    def _error(self):
        raise RuntimeError('Encoder data cannot be read')

    def get_trigger_count(self):
        self._error()

    def get_position_theta(self):
        self._error()

    def get_references_theta(self):
        self._error()

    def has_reference_theta(self):
        self._error()

    def get_position_z(self):
        self._error()

    def get_references_z(self):
        self._error()

    def has_reference_z(self):
        self._error()


class DataEncoder(object):
    def __init__(self):
        pass

    def encode(self, object):
        if not isinstance(object, Data):
            raise RuntimeError("object is not an instance of Data")
        return json.dumps(object.get_dict())

    def decode(self, encoded_object):
        try:
            return Data(json.loads(encoded_object))
        except:
            return ErrorData()
