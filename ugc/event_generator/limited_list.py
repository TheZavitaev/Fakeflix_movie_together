from collections.abc import Sequence


class LimitedList(Sequence):  # noqa: WPS214
    def __init__(self, size: int):
        self._size = size
        self.data = [None for _ in range(size)]
        self.next_ix = 0

    def __getitem__(self, index):
        return self.data[index]

    def __iter__(self):
        return LimitedListIterator(self)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def append(self, item) -> None:
        if self.next_ix == self._size:
            self.next_ix = 0

        self.data[self.next_ix] = item

        self.next_ix += 1

    def values(self) -> list:
        return self.data[: self.next_ix]


class LimitedListIterator:
    def __init__(self, ll: LimitedList):
        self._limited_list = ll
        self._index = 0

    def __next__(self):
        if self._index < len(self._limited_list):
            self._index += 1
            return self._limited_list.data[self._index]
        raise StopIteration
