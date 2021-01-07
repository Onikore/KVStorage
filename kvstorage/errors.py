class APIError(Exception):
    message: str


class KeyNotFoundError(APIError):
    def __str__(self):
        return 'Key not found'


class ListLengthError(APIError):
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return f'(0-{self.length - 1})'


class NegativeLengthError(APIError):
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return 'length must be greater than 0'
