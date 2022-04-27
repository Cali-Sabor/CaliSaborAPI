class ClientException(RuntimeError):
    """
    Raised when hot trends information is not found
    """
    def __init__(self, *args, **kwargs):
        self.message = args[0]

    def __str__(self):
        return self.message


class AttendantException(RuntimeError):
    """
    Raised when hot trends information is not found
    """
    def __init__(self, *args, **kwargs):
        self.message = args[0]

    def __str__(self):
        return self.message
