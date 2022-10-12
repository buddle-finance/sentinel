# from multiprocessing import Event
# from concurrent.futures import Future

# # https://docs.python.org/3/library/concurrent.futures.html

# '''
# class ThreadManager:
#     self.threadSignals = {}

# @threaded
# def listenEvent(self, signal, *args):
#     while not signal.stop:
#         self.doStuff(*args)

#     print("thread signalled")
#     self.cleanup()
#     print("thread exited gracefully")
# '''

# class Threadable:
#     def __init__(self):
#         self.threadStopped = False
#         self.threadEvent = Event()

#     def startThread(self):
#         thread = Thread(target=self.loop)
#         thread.daemon = True
#         thread.start()
#         return thread

#     def stopThread(self):
#         self.threadEvent.set()
#         self.threadStopped = True

#     def loop(self):
#         while not self.threadStopped:

#             self.threadEvent.wait(1)  # Wait 1 seconds, returns bool of event set
#             self.threadEvent.clear()        # Reset event

#             self.processEvent()
#         else:
#             self.processStop()

#     def processEvent(self):
#         """ This function must be overwritten """
#         pass

#     def processStop(self):
#         pass
