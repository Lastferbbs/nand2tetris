import os
import glob

DIR_PATH = "project_8/files"
OUTPUT_FILE = "output.asm"
current_equal_number = 1
current_gt_number = 1
current_lt_number = 1

arith_logic_list = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

functions = {}


def main():
    files = glob.glob(os.path.join(DIR_PATH, "*"))
    with open(OUTPUT_FILE, "w") as file:
        pass
    writeCall("Sys.init", "0")
    for file_path in files:
        with open(file_path, "r") as input_file:
            lines = input_file.readlines()
        file_name = ((file_path.split("/"))[-1].split("."))[0]
        for line in lines:
            line = line.replace("\n", "")
            command_type = ""
            arg_1 = ""
            arg_2 = ""
            line = line.split()
            if not line or "//" in line[0]:
                continue
            if line[0] in arith_logic_list:
                command_type = "C_ARITHMETIC"
                arg_1 = line[0]
                writeArithmetic(arg_1)
                continue
            elif line[0] in "push":
                command_type = "C_PUSH"
                arg_1 = line[1]
                arg_2 = line[2]
                writePushPop(command_type, arg_1, arg_2, file_name)
                continue
            elif line[0] in "pop":
                command_type = "C_POP"
                arg_1 = line[1]
                arg_2 = line[2]
                writePushPop(command_type, arg_1, arg_2, file_name)
                continue
            elif "goto" == line[0]:
                arg_1 = line[1]
                writeGoto(arg_1)
            elif "if-goto" in line[0]:
                arg_1 = line[1]
                writeIf(arg_1)
            elif "label" in line[0]:
                arg_1 = line[1]
                writeLabel(arg_1)
            elif "function" in line[0]:
                arg_1 = line[1]
                arg_2 = line[2]
                writeFunction(arg_1, arg_2)
            elif "call" in line[0]:
                arg_1 = line[1]
                arg_2 = line[2]
                writeCall(arg_1, arg_2)
            elif "return" in line[0]:
                writeReturn()


def writeFunction(name, numVars):
    lines_to_write = f"({name})\n"
    writeToFile(lines_to_write.replace(" ", ""))
    for i in range(int(numVars)):
        writePushPop("C_PUSH", "constant", 0, "")

    pass


def writeCall(name, nArgs):
    functions[name] = functions.get(name, 0) + 1
    lines_to_write = "// Ustawianie returnAddresu\n"
    writeToFile(lines_to_write)
    lines_to_write = f"@{name}.returnAddress.{functions[name]}\n D=A\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
    writeToFile(lines_to_write.replace(" ", ""))

    lines_to_write = "// Zapisanie LCL\n"
    writeToFile(lines_to_write)
    lines_to_write_LCL = f"@LCL\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
    writeToFile(lines_to_write_LCL.replace(" ", ""))

    lines_to_write = "// Zapisanie ARG\n"
    writeToFile(lines_to_write)
    lines_to_write_ARG = f"@ARG\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
    writeToFile(lines_to_write_ARG.replace(" ", ""))

    lines_to_write = "// Zapisanie THIS\n"
    writeToFile(lines_to_write)
    lines_to_write_THIS = f"@THIS\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
    writeToFile(lines_to_write_THIS.replace(" ", ""))

    lines_to_write = "// Zapisanie THAT\n"
    writeToFile(lines_to_write)
    lines_to_write_THAT = f"@THAT\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
    writeToFile(lines_to_write_THAT.replace(" ", ""))

    lines_to_write = "// Ustawienie ARG pointera\n"
    writeToFile(lines_to_write)
    lines_to_write_reposition_ARG = (
        f"@{nArgs}\n D=A\n @5\n D=D+A\n @SP\n D=M-D\n @ARG\n M=D\n"
    )
    writeToFile(lines_to_write_reposition_ARG.replace(" ", ""))

    lines_to_write = "// Ustawienie LCL na SP\n"
    writeToFile(lines_to_write)
    lines_to_write_LCL_equals_SP = f"@SP\n D=M\n @LCL\n M=D\n"
    writeToFile(lines_to_write_LCL_equals_SP.replace(" ", ""))

    lines_to_write = f"// Skok do funkcji {name}\n"
    writeToFile(lines_to_write)
    writeGoto(name)

    lines_to_write = f"// Stworzenie labela do skoku dla funkcji {name}\n"
    writeToFile(lines_to_write)
    writeLabel(f"{name}.returnAddress.{functions[name]}")


def writeReturn():
    lines_to_write = (
        f"@LCL\n D=M\n @endFrame\n M=D\n @5\n D=D-A\n A=D\n D=M\n @retAddr\n M=D\n"
    )
    writeToFile(lines_to_write.replace(" ", ""))
    writePushPop("C_POP", "argument", 0, "")
    lines_to_write = f"@ARG\n D=M+1\n @SP\n M=D\n @endFrame\n D=M-1\n M=M-1\n A=D\n D=M\n @THAT\n M=D\n @endFrame\n D=M-1\n M=M-1\n A=D\n D=M\n @THIS\n M=D\n @endFrame\n D=M-1\n M=M-1\n A=D\n D=M\n @ARG\n M=D\n @endFrame\n D=M-1\n M=M-1\n A=D\n D=M\n @LCL\n M=D\n @retAddr\n A=M\n 0;JMP\n"
    writeToFile(lines_to_write.replace(" ", ""))


def writeLabel(arg_1):
    lines_to_write = f"({arg_1})\n"
    writeToFile(lines_to_write.replace(" ", ""))


def writeGoto(arg_1):
    lines_to_write = f"@{arg_1}\n 0;JMP\n"
    writeToFile(lines_to_write.replace(" ", ""))


def writeIf(arg_1):
    lines_to_write = f"// If goto\n"
    writeToFile(lines_to_write)
    lines_to_write = (
        f"@SP\n A=M-1\n D=M\n @SP\n M=M-1\n @{arg_1}\n D;JLT\n @{arg_1}\n D;JGT\n"
    )
    writeToFile(lines_to_write.replace(" ", ""))


def writeArithmetic(arg_1):
    if arg_1 == "add":
        lines_to_write = "@SP\n M=M-1\n A=M\n D=M\n @SP\n A=M-1\n M=D+M\n"
    elif arg_1 == "sub":
        lines_to_write = "@SP\n M=M-1\n A=M\n D=M\n @SP\n A=M-1\n M=M-D\n"
    elif arg_1 == "neg":
        lines_to_write = "@SP\n A=M-1\n M=!M\n M=M+1\n"
    elif arg_1 == "and":
        lines_to_write = "@SP\n M=M-1\n A=M\n D=M\n @SP\n A=M-1\n M=D&M\n"
    elif arg_1 == "or":
        lines_to_write = "@SP\n M=M-1\n A=M\n D=M\n @SP\n A=M-1\n M=D|M\n"
    elif arg_1 == "not":
        lines_to_write = "@SP\n A=M-1\n M=!M\n"
    elif arg_1 == "eq":
        global current_equal_number
        lines_to_write = f"@SP\n M=M-1\n A=M\n D=M\n @SP\n A=M-1\n D=D-M\n @EQUAL_{current_equal_number}\n D;JEQ\n @SP\n A=M-1\n M=0\n @SKIP_EQUAL_{current_equal_number}\n D;JNE\n (EQUAL_{current_equal_number})\n @SP\n A=M-1\n M=-1\n (SKIP_EQUAL_{current_equal_number})\n"
        current_equal_number = current_equal_number + 1
    elif arg_1 == "gt":
        global current_gt_number
        lines_to_write = f"@SP\n M=M-1\n A=M\n D=M\n @SP\n A=M-1\n D=D-M\n @GT_{current_gt_number}\n D;JLT\n @SP\n A=M-1\n M=0\n @SKIP_GT_{current_gt_number}\n D;JGE\n (GT_{current_gt_number})\n @SP\n A=M-1\n M=-1\n (SKIP_GT_{current_gt_number})\n"
        current_gt_number = current_gt_number + 1
    elif arg_1 == "lt":
        global current_lt_number
        lines_to_write = f"@SP\n M=M-1\n A=M\n D=M\n @SP\n A=M-1\n D=D-M\n @LT_{current_lt_number}\n D;JGT\n @SP\n A=M-1\n M=0\n @SKIP_LT_{current_lt_number}\n D;JLE\n (LT_{current_lt_number})\n @SP\n A=M-1\n M=-1\n (SKIP_LT_{current_lt_number})\n"
        current_lt_number = current_lt_number + 1

    writeToFile(lines_to_write.replace(" ", ""))


def writePushPop(command_type, arg_1, arg_2, file_name):
    if command_type == "C_PUSH":
        if arg_1 == "constant":
            lines_to_write = f"@{arg_2}\n D=A\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "local":
            lines_to_write = (
                f"@{arg_2}\n D=A\n @LCL\n A=D+M\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
            )
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "argument":
            lines_to_write = (
                f"@{arg_2}\n D=A\n @ARG\n A=D+M\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
            )
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "this":
            lines_to_write = f"@{arg_2}\n D=A\n @THIS\n A=D+M\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "that":
            lines_to_write = f"@{arg_2}\n D=A\n @THAT\n A=D+M\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "temp":
            lines_to_write = (
                f"@{arg_2}\n D=A\n @5\n A=D+A\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
            )
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "static":
            lines_to_write = (
                f"@Static.{file_name}.{arg_2}\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
            )
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "pointer":
            lines_to_write = f"@{3+int(arg_2)}\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
            writeToFile(lines_to_write.replace(" ", ""))

    elif command_type == "C_POP":
        if arg_1 == "local":
            lines_to_write = f"@{arg_2}\n D=A\n @LCL\n D=D+M\n @SP\n A=M-1\n A=M\n D=D+A\n A=D-A\n D=D-A\n M=D\n @SP\n M=M-1\n"
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "argument":
            lines_to_write = f"@{arg_2}\n D=A\n @ARG\n D=D+M\n @SP\n A=M-1\n A=M\n D=D+A\n A=D-A\n D=D-A\n M=D\n @SP\n M=M-1\n"
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "this":
            lines_to_write = f"@{arg_2}\n D=A\n @THIS\n D=D+M\n @SP\n A=M-1\n A=M\n D=D+A\n A=D-A\n D=D-A\n M=D\n @SP\n M=M-1\n"
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "that":
            lines_to_write = f"@{arg_2}\n D=A\n @THAT\n D=D+M\n @SP\n A=M-1\n A=M\n D=D+A\n A=D-A\n D=D-A\n M=D\n @SP\n M=M-1\n"
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "temp":
            lines_to_write = f"@{arg_2}\n D=A\n @5\n D=D+A\n @SP\n A=M-1\n A=M\n D=D+A\n A=D-A\n D=D-A\n M=D\n @SP\n M=M-1\n"
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "static":
            lines_to_write = f"@SP\n A=M-1\n D=M\n @Static.{file_name}.{arg_2}\n M=D\n @SP\n M=M-1\n "
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "pointer":
            lines_to_write = (
                f"@SP\n A=M-1\n D=M\n @{3+int(arg_2)}\n M=D\n @SP\n M=M-1\n"
            )
            writeToFile(lines_to_write.replace(" ", ""))


def writeToFile(lines_to_write):
    with open(OUTPUT_FILE, "a") as output_file:
        if os.stat(OUTPUT_FILE).st_size == 0:
            output_file.write("@256\n D=A\n @SP\n M=D\n".replace(" ", ""))
        output_file.write(lines_to_write)


if __name__ == "__main__":
    main()
