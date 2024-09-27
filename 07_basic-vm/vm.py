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

snippets = {
    "jump_to_last_operand": ["@SP", "A=M-1"],
    "jump_up_operand": ["D=M", "A=A-1"],
    "save_stack_top_position_uni": ["D=A+1", "@SP", "M=D"],
    "save_stack_top_position_pop": ["@SP", "M=M-1"],
    "save_stack_top_position_push": ["@SP", "M=M+1"],
}

snippets_lam = {
    "constant_push":\
        lambda i:\
        [f"@{i}", "D=A", "@SP", "A=M", "M=D"]\
        + snippets["save_stack_top_position_push"],
    "comparison_op":\
        lambda operator, label_i:\
        snippets["jump_to_last_operand"]\
        + snippets["jump_up_operand"]\
        + ["M=M-D"]\
        + snippets["save_stack_top_position_pop"]\
        + ["A=M-1", "D=M", f"@cmp{label_i}", f"D;{operator}"]\
        + snippets["jump_to_last_operand"] + ["M=0"]\
        + [f"@ed{label_i}", "0;JMP"]\
        + [f"(cmp{label_i})"] + snippets["jump_to_last_operand"]\
        + ["M=-1", f"(ed{label_i})"],
    "arithmetic_op":\
        lambda operator:\
        snippets["jump_to_last_operand"]\
        + snippets["jump_up_operand"]\
        + ([f"M=M{operator}D"] if operator == "-"\
        else [f"M=D{operator}M"])\
        + snippets["save_stack_top_position_pop"],
    "unary_op":\
        lambda operator:\
        snippets["jump_to_last_operand"]\
        + [f"M={operator}M"]
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

def main():
    label_i = 0
    source = read_source("./simple_add.vm")
    for key in operator_map:
        print("eq" in operator_map[key].keys())

if __name__ == "__main__":
    main()
