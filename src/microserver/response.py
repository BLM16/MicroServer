class Response:
    """
    All server routes and error handlers must return a `Response`.
    Tracks the return data and its corresponding mime type.
    """

    def __init__(self, data: str, mime: str):
        self.data = data
        self.mime = mime
