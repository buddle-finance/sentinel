from concurrent.futures import ThreadPoolExecutor, Future
from threading import Event, Lock
from typing import Any

from sentinel.services.configManager import ConfigManager
from sentinel.services.logManager import BuddleLogger
from sentinel.services.singletonFactory import SingletonFactory


# To signal the thread and gracefully shutdown
class Signal:
    def __init__(self):
        self._signalled: bool = False

    @property
    def signalled(self) -> bool:
        return self._signalled

    def signal(self):
        self.signalled = True


class BuddleThread:
    def __init__(self):
        self.id: int = id
        self.threadFuture: Future = None
        self.event: Event = Event()


class ThreadManager:
    def __init__(self, singletonFactory: SingletonFactory) -> None:
        self.logger = singletonFactory.getService(BuddleLogger)
        self.configService = singletonFactory.getService(ConfigManager)
        self.maxThreads = self.configService.config.maxThreads
        self.criticalSection = Lock()
        self.threadPool = ThreadPoolExecutor(self.maxThreads)
        # TODO: Maintain own thread pool. Use simple thread objects instead of submitting to threadPool as
        # threadPool threads cannot be forcefully shut down.
        self.threads: dict[int, BuddleThread] = {}
        self.maxThreadId = 1

    def startThread(self, startFunc: function, *args, **kwargs) -> int:
        threadId = -1

        with self.criticalSection:
            threadId = self.maxThreadId
            self.maxThreadId += 1

        newThread = BuddleThread()
        try:
            threadFuture = self.threadPool.submit(
                startFunc, newThread.event, *args, **kwargs
            )
            newThread.id = threadId
            newThread.threadFuture = threadFuture
            self.threads[threadId] = newThread
        except Exception:
            self.logger.exception(
                "Thread could not be started for function [%s]", startFunc.__name__
            )
            raise

        return threadId

    def stopThread(self, threadId: int, timeout: int = -1) -> bool:
        curThread: BuddleThread = None
        with self.criticalSection:
            curThread = self.threads.get(threadId, None)

        if curThread is None:
            self.logger.warn("Thread ID [%d] does not exist, nothing to do", threadId)
            return True

        threadFuture = curThread.threadFuture
        if threadFuture.done() or threadFuture.cancelled():
            self.logger.debug(
                "Thread ID [%d] is already complete or cancelled", threadId
            )

        with self.criticalSection:
            threadFuture.cancel()
            curThread.event.set()

            if timeout > -1:
                threadFuture.result(timeout=timeout)
                # TODO: Join the thread with timeout and stop it otherwise
                # Log if thread did not exit gracefully
