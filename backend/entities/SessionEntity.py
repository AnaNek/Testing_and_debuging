class SessionEntity(object):
    def __init__(self, id=None, token=None, username=None):
        self._id = id
        self._token = token
        self._username = username

    def set(
        self,
        id: int,
        token,
        username: str
    ):
        self._id = id
        self._token = token
        self._username = username

        return self

    def set_token(
        self,
        token
    ):
        self._token = token

        return self

    @property
    def id(self):
        return self._id

    @property
    def token(self):
        return self._token

    @property
    def username(self):
        return self._username
