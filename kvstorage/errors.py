class APIError(Exception):
    pass


class KeyNotFoundError(APIError):
    def __str__(self):
        return 'Key not found'


class ListLengthError(APIError):
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return f'Available places are (0-{self.length - 1})'


class InvalidValueError(APIError):
    def __str__(self):
        return 'Number must be positive integer'
