import numpy as np
from random import shuffle
import copy
from torch import Tensor


class replayBuffer:
    class BatchedIterator:
        def __init__(self, l, batchSize, shuffle_data=True):

            self.__l = []
            self.__l_ori = l

            self.__shuffle_data = shuffle_data
            self.__batchSize = batchSize

        def __next__(self):

            if len(self.__l) < 1:

                self.__l = copy.copy(self.__l_ori)

                if self.__shuffle_data:
                    shuffle(self.__l)

            batch = self.__l[: self.__batchSize]
            self.__l = self.__l[self.__batchSize :]

            return tuple((Tensor(np.array([t[i] for t in batch])) for i in range(len(batch[0]))))

        def __len__(self):
            return len(self.__l)

    def __init__(self, maxSize=200, batchSize=1, shuffle_data=True):
        self.__buffer = []
        self.__maxSize = maxSize
        self.__batchSize = batchSize
        self.__shuffle_data = shuffle_data

    def append(self, transition):

        if len(self.__buffer) >= self.__maxSize:

            self.__buffer.pop(0)
        self.__buffer.append(transition)

    def __iter__(self):
        return replayBuffer.BatchedIterator(
            self.__buffer, batchSize=self.__batchSize, shuffle_data=self.__shuffle_data
        )

    @property
    def buff_to_array(self):
        return self.__buffer

    def __len__(self):
        return len(self.__buffer)
