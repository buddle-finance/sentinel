from sentinel.handlers.baseHandler import BaseHandler
from sentinel.services.singletonFactory import SingletonFactory


class LiquidityHandler(BaseHandler):
    def __init__(self, singletonFactory: SingletonFactory):
        super().__init__(singletonFactory)

    def handleEvent(self, eventData):
        pass
