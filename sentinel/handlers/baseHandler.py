from sentinel.services.buddleNetwork import BuddleNetwork
from sentinel.services.singletonFactory import SingletonFactory


class BaseHandler:
    def __init__(self, singletonFactory: SingletonFactory):
        self.singletonFactory = singletonFactory

    # TODO: eventData should be a generic type for all possible events
    def handleEvent(self, eventData):
        pass
