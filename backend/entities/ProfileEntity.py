class ProfileEntity(object):
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password

    def set(
        self,
        username: str,
        password: str
    ):
        self._username = username
        self._password = password

        return self

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @classmethod
    def check_password(self, password: str) -> bool:
        return self._password == password
