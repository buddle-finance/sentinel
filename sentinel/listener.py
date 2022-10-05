class Listener(object):
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback

    def __str__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)
