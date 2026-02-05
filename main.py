from sys import argv
from pick import pick
from os import name as os_name

if os_name == "nt":
    import pyreadline3
else:
    import readline

operations = {
    "/": "not",
    "~": "not",
    "¬": "not",
    "*": "and",
    "∧": "and",
    "×": "and",
    "⋅": "and",
    "&": "and",
    "+": "or",
    "∨": "or",
    "|": "or",
}
notation_styles = [("0", "1"), ("F", "T"), ("L", "H")]

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

        notation_type = pick(
            ["1/0", "T/F", "H/L"],
            "Choose your notation:",
            indicator="=>",
        )[1]

        out_HTML = pick(
            ["YES", "NO"],
            "Create .HTML file for table viewing/exporting?",
            indicator="=>",
        )
        if out_HTML[1] == 0:
            HTML_path = "".join(char for char in equation if char.isalnum()) + ".html"

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
        for i in range(len(out)):
            line = out[i]
            ins = list(bin(line[0])[2:].zfill(pin_count))
            ins = [notation_styles[notation_type][int(n)] for n in ins]
            outs = notation_styles[notation_type][line[1]]
            print(" ".join(ins), end=" ")
            print("|", outs)
            out[i] = [ins, outs]
        print()

        if out_HTML[1] == 0:
            out_HTML = f'<table><colgroup><col span="{pin_count}" style="background-color:aqua"><col style="background-color:lime"></colgroup>'
            out_HTML += "<tr>"
            out_HTML += (
                "<th>"
                + "</th><th>".join(list(pin_mapping.keys()) + [output_pin])
                + "</th>"
            )
            out_HTML += "</tr>"
            for line in out:
                out_HTML += "<tr><td>"
                out_HTML += "</td><td>".join(line[0])
                out_HTML += f"</td><td>{line[1]}</td>"
                out_HTML += "</tr>"
            out_HTML += "</table>"
            with open(HTML_path, "w+") as file:
                file.write(out_HTML)
