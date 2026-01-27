from sys import argv
from pick import pick

operations = {"/": "not", "*": "and", "+": "or"}

if __name__ == "__main__":
    if len(argv) > 1:
        with open(argv[1], "r") as file:
            equations = [
                equation for equation in file.readlines() if not equation.isspace()
            ]
    else:
        equations = [
            input("Input your logic equation:\n> "),
        ]
    equations = [equation.strip().replace(" ", "") for equation in equations]

    for equation in equations:
        print(equation)

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
            "Select all active-low pins:",
            indicator="=>",
            multiselect=True,
        )
        for pin in selected:
            if pin[0] == output_pin:
                equation = f"{pin[0]}=not ({equation[2:]})"
            else:
                equation = equation.replace(pin[0], f"(/{pin[0]})")

        for symbol in operations:
            equation = equation.replace(symbol, " %s " % operations[symbol])

        print()
        print(" ".join(list(pin_mapping.keys())), "|", output_pin)
        print("-" * (len(pin_mapping) * 2 + 3))
        for pin_voltages in range(2**pin_count):
            for var in pin_mapping:
                globals()[var] = (pin_voltages >> pin_mapping[var]) & 1
                print(globals()[var], end=" ")
            output = int(eval(equation[2:]))
            print("|", output)
