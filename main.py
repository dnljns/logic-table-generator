from sys import argv
from pick import pick
from os import name as os_name

if os_name == "nt":
    import pyreadline3
else:
    import readline

operations = {"/": "not", "*": "and", "+": "or"}

if __name__ == "__main__":
    if len(argv) > 1:
        with open(argv[1], "r") as file:
            equations = [
                equation for equation in file.readlines() if not equation.isspace()
            ]
    else:
        lines = []
        line = input("Input your logic equation:\n> ")
        lines.append(line)
        while line:
            line = input("> ")
            lines.append(line)
        equations = ["\n".join(lines)]
    equations = ["".join(equation.split()) for equation in equations]

    for equation in equations:
        pin_count = 0
        pin_mapping = {}

        for char in equation:
            if char == equation[0]:
                output_pin = equation[0]
                continue  # Skip output pin
            if char.isalpha() and char not in pin_mapping:
                pin_mapping[char] = pin_count
                pin_count += 1

        selected = pick(
            list(pin_mapping.keys()) + [output_pin],
            "Select all active-low pins:\n(Enter none for truth table)",
            indicator="=>",
            multiselect=True,
        )
        print(equation)

        for symbol in operations:
            equation = equation.replace(symbol, " %s " % operations[symbol])
        equation = equation.replace("[", "(").replace("]", ")")

        n_logic = lambda i: i in [n[0] for n in selected]
        out = []
        for pin_voltages in range(2**pin_count):
            out.append([[]])
            for var in pin_mapping:
                globals()[var] = i = bool((pin_voltages >> pin_mapping[var]) & 1)
                out[-1][0].append(int(not i if n_logic(var) else i))
            o = eval(equation[2:])
            out[-1].append(int(not o if n_logic(equation[0]) else o))
            out[-1][0] = int("".join(map(str, out[-1][0])), 2)
        out.sort()

        print()
        print(" ".join(list(pin_mapping.keys())), "|", output_pin)
        print("-" * (len(pin_mapping) * 2 + 3))
        for line in out:
            print(" ".join(bin(line[0])[2:].zfill(pin_count)), end=" ")
            print("|", line[1])
        print()
