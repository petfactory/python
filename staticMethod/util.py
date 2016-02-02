class UI(object):

    __window = None

    def __init__(self, window):
        type(self).__window = window

    @staticmethod
    def getWindow():
        return UI.__window

