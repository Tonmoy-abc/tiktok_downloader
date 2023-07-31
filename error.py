class NotFound(Exception):
    def __init__(self, status, message="Url Not Found"):
        self.message = f"code: {status}, {message}"
        super().__init__(self.message)