from dicts import COMP_DICT, JMP_DICT, DEST_DICT, PREDEFINED_DICT

INPUT_FILE = "test.asm"
OUTPUT_FILE = "output.hack"


def instruction_a(line):
    return "{0:016b}".format(int(line))


def remove_comments(line):
    return ((line.split("/"))[0]).replace("\n", "")


def save_file(output_list):
    with open(OUTPUT_FILE, "w") as output:
        for line in output_list:
            output.write(line + "\n")


def handle_loops_vars(file):
    i = 0
    for line in file:
        line = remove_comments(line)
        if "/" in line or not line or line.isspace():
            continue
        if line[0] == "(":
            name = ((line.split(")"))[0]).replace("(", "")
            PREDEFINED_DICT[name] = i
            continue
        i = i + 1
    return 0


def handle_A_instructions(line, output_list, first_free_address):
    line = line.replace(" ", "")
    if line[1].isalpha():
        if line[1:] in PREDEFINED_DICT:
            output_list.append(instruction_a(PREDEFINED_DICT[line[1:]]))
        else:
            PREDEFINED_DICT[line[1:]] = first_free_address
            output_list.append(instruction_a(PREDEFINED_DICT[line[1:]]))
            first_free_address = first_free_address + 1
    else:
        output_list.append(instruction_a(line[1:]))

    return first_free_address


def handle_C_instructions(line, output_list, dest):
    bin_output = ""
    if "=" in line:
        dest = True
        dest_bin = ((line.split("="))[0]).replace(" ", "")
        dest_bin = DEST_DICT[dest_bin]
    else:
        dest_bin = "000"
    if ";" in line:
        jmp_bin = ((line.split(";"))[-1]).replace(" ", "")

        jmp_bin = JMP_DICT[jmp_bin]
    else:
        jmp_bin = "000"
    comp_bin = line.replace(";", "=")
    if dest:
        comp_bin = ((comp_bin.split("="))[1]).replace(" ", "")
    else:
        comp_bin = ((comp_bin.split("="))[0]).replace(" ", "")
    comp_bin = COMP_DICT[comp_bin]
    bin_output = "111" + comp_bin + dest_bin + jmp_bin
    output_list.append(bin_output)


def main():
    output_list = []
    first_free_address = 16

    # First loop finding loop variables
    with open(INPUT_FILE, "r") as file:
        handle_loops_vars(file)

    with open(INPUT_FILE, "r") as file:
        for line in file:
            dest = False
            line = remove_comments(line)
            if "/" in line or not line or line.isspace() or "(" in line:
                continue
            if "@" in line:
                first_free_address = handle_A_instructions(
                    line, output_list, first_free_address
                )
            else:
                handle_C_instructions(line, output_list, dest)

    save_file(output_list)


if __name__ == "__main__":
    main()
