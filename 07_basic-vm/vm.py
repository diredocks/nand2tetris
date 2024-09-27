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
    "jump_to_stack_head": ["@SP", "A=M"],
    "jump_to_last_operand": ["@SP", "A=M-1"],
    "jump_up_operand": ["D=M", "A=A-1"],
    "save_stack_top_position_uni": ["D=A+1", "@SP", "M=D"],
    "save_stack_top_position_pop": ["@SP", "M=M-1"],
    "save_stack_top_position_push": ["@SP", "M=M+1"],
}

snippets_lam = {
    "pointer_push":\
        lambda segment:\
        [f"@{segment}", "D=M"]\
        + snippets["jump_to_stack_head"] + ["M=D"]\
        + snippets["save_stack_top_position_push"],
    "pointer_pop":\
        lambda segment:\
        snippets["jump_to_last_operand"] + ["D=M"]\
        + [f"@{segment}", "M=D"]\
        + snippets["save_stack_top_position_pop"],
   "temp_push":\
        lambda offset:\
        [f"@{int(offset)+5}", "D=M"]\
        + snippets["jump_to_stack_head"] + ["M=D"]\
        + snippets["save_stack_top_position_push"],
    "temp_pop":\
        lambda offset:\
        snippets["jump_to_last_operand"] + ["D=M"]\
        + [f"@{int(offset)+5}", "M=D"]\
        + snippets["save_stack_top_position_pop"],
    "segment_push":\
        lambda offset, segment:\
        [f"@{segment}", "A=M"]\
        + ["A=A+1"]*int(offset) + ["D=M"]\
        + snippets["jump_to_stack_head"] + ["M=D"]\
        + snippets["save_stack_top_position_push"],
    "segment_pop":\
        lambda offset, segment:\
        snippets["jump_to_last_operand"] + ["D=M"]\
        + [f"@{segment}", "A=M"] + ["A=A+1"]*int(offset)\
        + ["M=D"] + snippets["save_stack_top_position_pop"],
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
    },
}

segment_map = {
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "local": "LCL",
    "static": "STATIC"
}

def main():
    label_i = 0
    source = read_source("./pointer_test.vm")
    gen = []
    for each in source:
        cmd = each[0]
        gen.append(["//"+" ".join(each)])
        if cmd in operator_map["arithmetic_op"].keys():
            gen.append(snippets_lam["arithmetic_op"](operator_map["arithmetic_op"][cmd]))
        elif cmd in operator_map["comparison_op"].keys():
            gen.append(snippets_lam["comparison_op"](operator_map["comparison_op"][cmd], label_i))
            label_i = label_i + 1
        elif cmd in operator_map["unary_op"].keys():
            gen.append(snippets_lam["unary_op"](operator_map["unary_op"][cmd]))
        elif cmd == "push":
            if each[1] == "constant":
                gen.append(snippets_lam["constant_push"](each[2]))
            elif each[1] == "temp":
                gen.append(snippets_lam["temp_push"](each[2]))
            elif each[1] == "pointer" and each[2] == "0":
                gen.append(snippets_lam["pointer_push"]("THIS"))
            elif each[1] == "pointer" and each[2] == "1":
                gen.append(snippets_lam["pointer_push"]("THAT"))
            elif each[1] in segment_map.keys():
                gen.append(snippets_lam["segment_push"](each[2], segment_map[each[1]]))
            else:
                pass
        elif cmd == "pop":
            if each[1] in segment_map.keys():
                gen.append(snippets_lam["segment_pop"](each[2], segment_map[each[1]]))
            elif each[1] == "temp":
                gen.append(snippets_lam["temp_pop"](each[2]))
            elif each[1] == "pointer" and each[2] == "0":
                gen.append(snippets_lam["pointer_pop"]("THIS"))
            elif each[1] == "pointer" and each[2] == "1":
                gen.append(snippets_lam["pointer_pop"]("THAT"))
            else:
                pass
    gen = [each for eaches in gen for each in eaches]
    print("\n".join(gen))

if __name__ == "__main__":
    main()
