snippets = {
    "jump_to_last_operand": ["@SP", "A=M-1", "D=M"],
    "jump_up_operand": ["A=A-1"],
    "save_stack_top_position": ["D=A+1", "@SP", "M=D"],
    "constant_push": lambda i: [f"@{i}", "D=A", "@SP", "A=M", "M=D"]
}

label_i = 0

def source_beauty(line):
    line = line.strip()
    if '//' in line:
        line = line[:line.find('//')]
    line = line.split(' ')
    line = [token for token in line if token != '']
    return line

def read_source(file_name):
    source = []
    with open(file_name, 'r') as lines:
        source = [source_beauty(line) for line in lines]
    return source

def arithmetic_op(operator):
    return \
        snippets["jump_to_last_operand"]\
        + snippets["jump_up_operand"]\
        + [f"M=M{operator}D"] if operator == "-"\
        else [f"M=D{operator}M"]\
        + snippets["save_stack_top_position"]

def comparison_op(operator):
    global label_i
    label_i = label_i + 1
    return \
        snippets["jump_to_last_operand"]\
        + snippets["jump_up_operand"]\
        + ["M=M-D"]\
        + snippets["save_stack_top_position"]\
        + ["A=D-1", "D=M", f"@cmp{label_i}", f"D;{operator}", "@SP", "A=M-1", "M=0"]\
        + [f"@ed{label_i}", "0;JMP"]\
        + [f"(cmp{label_i})", "@SP", "A=M-1", "M=-1"]\
        + [f"(ed{label_i})"]

binary_parser = {
    "add": arithmetic_op("+"),
    "sub": arithmetic_op("-"),
    "and": arithmetic_op("&"),
    "or": arithmetic_op("|"),
    "eq": comparison_op("JEQ"),
    "ne": comparison_op("JNE"),
    "lt": comparison_op("JLT"),
    "gt": comparison_op("JGT"),
    "lte": comparison_op("JLE"),
    "gte": comparison_op("JGE")
}

push_pop_parser = {
    "push": snippets["constant_push"](12) + snippets["save_stack_top_position"]
}

def main():
    source = read_source("./basic_test.vm")
    '''
    for each in source:
        if each[0] not in parser.keys():
            print("Unknow token:", each[0])
        else:
            print(parser[each[0]])
    '''
    print('\n'.join(push_pop_parser["push"]))

if __name__ == "__main__":
    main()
