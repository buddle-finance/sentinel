from sentinel.handlers.baseHandler import BaseHandler
from sentinel.types.configTypes import Network
from sentinel.utils.threadable import Threadable


class Listener(Threadable):
    def __init__(self, network: Network, handler: BaseHandler):
        self.name = name
        self.handler = handler

    def startThread(self):
        pass

    def __str__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

    def processEvent(self):
        self.handler.handleEvent([])
