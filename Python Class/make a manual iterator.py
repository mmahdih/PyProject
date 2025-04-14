class Iterator:
    def __init__(self, sequence):
        self._sequence = sequence
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._sequence):
            value = self._sequence[self._index]
            self._index += 1
            return value
        else:
            raise StopIteration


sequence = Iterator([1, 2, 3])
iterator = iter(sequence)
while True:
    try:
        item = next(iterator)
    except StopIteration:
        break
    print(item)