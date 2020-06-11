class SingletonStatus:
    # Here will be the instance stored.
    __instance = None
    run = False


    @staticmethod
    def getInstance():
        """ Static access method. """
        if SingletonStatus.__instance == None:
            SingletonStatus()

        return SingletonStatus.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SingletonStatus.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SingletonStatus.__instance = self
