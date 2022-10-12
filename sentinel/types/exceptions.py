class SingletonFactoryException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class RequiredConfigMissingException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)
