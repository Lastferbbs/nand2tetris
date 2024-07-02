import os


FILE_PATH = "project_7/test.vm"
current_equal_number = 1
current_gt_number = 1
current_lt_number = 1

arith_logic_list = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]


def main():
    with open(FILE_PATH, "r") as input_file:
        lines = input_file.readlines()
    for line in lines:
        line = line.replace("\n", "")
        command_type = ""
        arg_1 = ""
        arg_2 = ""
        line = (line.replace("	", "")).split()
        if line[0] in arith_logic_list:
            command_type = "C_ARITHMETIC"
            arg_1 = line[0]
            writeArithmetic(arg_1)
            continue
        elif line[0] in "push":
            command_type = "C_PUSH"
            arg_1 = line[1]
            arg_2 = line[2]
            writePushPop(command_type, arg_1, arg_2)
            continue
        elif line[0] in "pop":
            command_type = "C_POP"
            arg_1 = line[1]
            arg_2 = line[2]
            writePushPop(command_type, arg_1, arg_2)
            continue


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


def writePushPop(command_type, arg_1, arg_2):
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
            lines_to_write = f"@Static.{arg_2}\n D=M\n @SP\n A=M\n M=D\n @SP\n M=M+1\n"
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
            lines_to_write = (
                f"@SP\n A=M-1\n D=M\n @Static.{arg_2}\n M=D\n @SP\n M=M-1\n "
            )
            writeToFile(lines_to_write.replace(" ", ""))
        elif arg_1 == "pointer":
            lines_to_write = (
                f"@SP\n A=M-1\n D=M\n @{3+int(arg_2)}\n M=D\n @SP\n M=M-1\n"
            )
            writeToFile(lines_to_write.replace(" ", ""))


def writeToFile(lines_to_write):
    with open("output.txt", "a") as output_file:
        if os.stat("output.txt").st_size == 0:
            output_file.write(
                "@256\n D=A\n @SP\n M=D\n @300\n D=A\n @LCL\n M=D\n @400\n D=A\n @ARG\n M=D\n @3000\n D=A\n @THIS\n M=D\n @3010\n D=A\n @THAT\n M=D\n".replace(
                    " ", ""
                )
            )
        output_file.write(lines_to_write)


if __name__ == "__main__":
    main()


# Parser class
# CodeWriter class
