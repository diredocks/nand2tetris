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
        + ([f"M=M{operator}D"] if operator == "-"\
        else [f"M=D{operator}M"])\
        + snippets["save_stack_top_position"]

def comparison_op(operator, label_i):
    return \
        snippets["jump_to_last_operand"]\
        + snippets["jump_up_operand"]\
        + ["M=M-D"]\
        + snippets["save_stack_top_position"]\
        + ["A=D-1", "D=M", f"@cmp{label_i}", f"D;{operator}", "@SP", "A=M-1", "M=0"]\
        + [f"@ed{label_i}", "0;JMP"]\
        + [f"(cmp{label_i})", "@SP", "A=M-1", "M=-1"]\
        + [f"(ed{label_i})"]

def unary_op(operator):
    return \
        snippets["jump_to_last_operand"]\
        + [f"M={operator}M"]\

snippets = {
    "jump_to_last_operand": ["@SP", "A=M-1"],
    "jump_up_operand": ["D=M", "A=A-1"],
    "save_stack_top_position": ["D=A+1", "@SP", "M=D"],
    "constant_push": lambda i: [f"@{i}", "D=A", "@SP", "A=M", "M=D"]
}

operator_map = {
    "arithmetic_op": {
        "add": "+",
        "sub": "-",
        "and": "&",
        "or": "|"
    },
    "comparison_op": {
        "eq": "JEQ",
        "ne": "JNE",
        "lt": "JLT",
        "gt": "JGT",
        "lte": "JLE",
        "gte": "JGE"
    },
    "unary_op": {
        "not": "!",
        "neg": "-"
    }
}

def writer(line, label_i):
    cmd = line[0]
    if cmd in operator_map["arithmetic_op"].keys():
        return arithmetic_op(
                operator_map["arithmetic_op"][cmd]
                )
    elif cmd in operator_map["comparison_op"].keys():
        return comparison_op(
                operator_map["comparison_op"][cmd], label_i
                )
    elif cmd in operator_map["unary_op"].keys():
        return unary_op(
                operator_map["unary_op"][cmd]
                )
    elif cmd == "push":
        if line[1] == "constant":
            return snippets["constant_push"](line[2])\
                    + snippets["save_stack_top_position"]
    else:
        return None

def main():
    label_i = 0
    source = read_source("./simple_add.vm")
    for each in source:
        print("\n".join(writer(each, label_i)))
        label_i = label_i + 1

if __name__ == "__main__":
    main()
