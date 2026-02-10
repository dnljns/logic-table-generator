class _BitArray(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in args[0]:
            assert i == 0 or i == 1

    def fill_bits(self, n: int):
        n = bin(n)[2:][-len(self) :].zfill(len(self))
        self.clear()
        for i in n:
            self.append(int(i))

    def read_bits(self):
        return int("".join(map(str, self)), 2)


class MUX:
    def __init__(self, input_count: int):
        assert input_count > 1 and input_count & (input_count - 1) == 0
        self.SELECT = _BitArray([0] * (int.bit_length(input_count) - 1))
        self.DATA = _BitArray([0] * input_count)

    @property
    def OUTPUT(self):
        return self.DATA[self.SELECT.read_bits()]


if __name__ == "__main__":
    mux = MUX(4)
    mux.DATA.fill_bits(9)
    mux.SELECT.fill_bits(3)
    print(mux.OUTPUT)
