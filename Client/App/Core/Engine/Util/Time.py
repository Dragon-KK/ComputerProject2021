import time

class Time:

    def __init__(self):
        self.__prevTime = 0

    @property
    def DeltaTime(self):
        if self.__prevTime == 0:
            self.__prevTime = time.time()
            return 0
        tmp = time.time()
        ret = tmp - self.__prevTime
        self.__prevTime = tmp
        return ret

    # use this to reset delta time
    @DeltaTime.setter
    def DeltaTime(self, v):
        self.__prevTime = v