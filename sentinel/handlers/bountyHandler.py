from sentinel.handlers.baseHandler import BaseHandler
from sentinel.services.singletonFactory import SingletonFactory
from sentinel.types.configTypes import Network


class BountyHandler(BaseHandler):
    def __init__(self, singletonFactory: SingletonFactory, network: Network):
        super().__init__(singletonFactory)
        pass
