from pick import pick


class _BitArray(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in args[0]:
            assert i == 0 or i == 1
        self._active_lows = []

    def set_active_low(self, index: int):
        self._active_lows.append(index)

    def flip_active_lows(self):
        for i in range(len(self)):
            if i in self._active_lows:
                self[i] = int(not bool(self[i]))

    def fill_bits(self, n: int):
        n = bin(n)[2:][-len(self) :].zfill(len(self))
        self.clear()
        for i in n:
            self.append(int(i))

    def __str__(self):
        return "".join(map(str, self))

    def read_bits(self):
        return int(str(self), 2)


# Multiplexer
class MUX:
    def __init__(self, input_count: int):
        assert input_count > 1 and input_count & (input_count - 1) == 0
        self.SELECT = _BitArray([0] * (int.bit_length(input_count) - 1))
        self.DATA = _BitArray([0] * input_count)

    @property
    def OUTPUT(self):
        return self.DATA[-self.SELECT.read_bits() - 1]


notation_styles = [("0", "1"), ("F", "T"), ("L", "H")]

if __name__ == "__main__":
    ct = int(input("N-input MUX?\n> "))
    mux = MUX(ct)

    for low in pick(
        ["S%d" % s for s in range(len(mux.SELECT))],
        "Select all active-low select pins:",
        indicator="=>",
        multiselect=True,
    ):
        mux.SELECT.set_active_low(len(mux.SELECT) - low[1] - 1)
    for low in pick(
        ["D%d" % d for d in range(len(mux.DATA))],
        "Select all active-low data pins:",
        indicator="=>",
        multiselect=True,
    ):
        mux.DATA.set_active_low(len(mux.DATA) - low[1] - 1)

    out_low = pick(
        ["NO", "YES"],
        "Is the output pin active-low?",
        indicator="=>",
    )

    # notation_type = pick(
    #    ["1/0", "T/F", "H/L"],
    #    "Choose your notation:",
    #    indicator="=>",
    # )[1]

    table = []
    for sel in range(ct):
        mux.SELECT.fill_bits(sel)
        for dat in range(2**ct):
            mux.DATA.fill_bits(dat)
            out = int(not bool(mux.OUTPUT)) if out_low[1] == 1 else mux.OUTPUT
            mux.SELECT.flip_active_lows()
            mux.DATA.flip_active_lows()
            table.append((mux.SELECT.read_bits(), mux.DATA.read_bits(), out))
    table.sort()

    print("%d-input MUX:" % ct)
    print("S" * len(mux.SELECT), "D" * len(mux.DATA), "| Y")
    print("-" * (len(mux.SELECT) + len(mux.DATA) + 5))
    for row in table:
        sel = _BitArray([0] * len(mux.SELECT))
        sel.fill_bits(row[0])
        dat = _BitArray([0] * len(mux.DATA))
        dat.fill_bits(row[1])
        print(str(sel), str(dat), "|", row[2])
