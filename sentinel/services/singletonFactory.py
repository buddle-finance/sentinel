from sentinel.types.exceptions import SingletonFactoryException
from typing import TypeVar, Callable

R, D = TypeVar("R"), TypeVar("D")


class SingletonFactory:
    def __init__(self) -> None:
        self.classes: dict[type, object] = {}

    def addService(self, cls: object) -> None:
        self.classes[type(cls)] = cls

    def removeService(self, clsType: type) -> bool:
        if self.classes.get(clsType):
            del self.classes[clsType]
            return True

        return False

    def getService(self, clsType: Callable[[D], R]) -> R:
        cls = self.classes.get(clsType)
        if not cls:
            cls = clsType(self)
            self.addService(cls)

        return cls

    def updateService(self, cls: object) -> bool:
        if self.classes.get(type(cls)):
            self.addClass(cls)
        else:
            raise SingletonFactoryException("Class not found in factory")
