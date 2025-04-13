from enum import Enum


class User:
    class Role(Enum):
        ADMIN = 'admin'
        CLIENT = 'client'
        COURIER = 'courier'
        KITCHENER = 'kitchener'

    def __init__(self, role: Role) -> None:
        self._name: str = ""
        self._gender: str = ""
        self._role: User.Role = role
        self._phone_num: str = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def role(self) -> Role:
        return self._role

    @property
    def phone_num(self) -> str:
        return self._phone_num

    @phone_num.setter
    def phone_num(self, value: str) -> None:
        self._phone_num = value
