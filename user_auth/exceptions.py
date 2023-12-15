class UnauthenticatedException(Exception):
    def __init__(self, message="Unauthenticated!"):
        self.message = message
        super().__init__(self.message)
