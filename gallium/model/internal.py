class Internal(object):
    def __init__(self, container = None):
        self.container = container or ContainerMode.DEFAULT # Container Mode

class ContainerMode(object):
    """ Valid Constant Collection on Container Mode

        - ``builtin``:    The process will use the configuration from the standalone container.
        - ``standalone``: The process will use the configuration from the standalone container.
        - ``splitter``:   The process will have two separated containers.
    """
    BUILTIN    = 'builtin'    # The process will use the configuration from the standalone container.
    STANDALONE = 'standalone' # The process will use the configuration from the standalone container.
    SPLITTER   = 'splitter'   # The process will have two separated containers.

    DEFAULT = SPLITTER

    __valid_modes__ = (BUILTIN, STANDALONE, SPLITTER)

    @staticmethod
    def valid_modes():
        return ContainerMode.__valid_modes__

    @staticmethod
    def is_valid(mode):
        return mode in ContainerMode.valid_modes()
