import numpy as np


class replayBuffer:
    def __init__(self, maxSize=200):
        self.__buffer = []
        self.__maxSize = maxSize

    def append(self, transition):

        if len(self.__buffer) >= self.__maxSize:

            self.__buffer.pop(0)
        self.__buffer.append(transition)

    @property
    def buff_to_array(self):
        return self.__buffer

    def __len__(self):
        return len(self.__buffer)
