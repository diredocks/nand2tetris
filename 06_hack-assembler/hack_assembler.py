import re
import time
import argparse

symbol_table = {
    "R0": 0, "R1": 1, "R2": 2, "R3": 3,
    "R4": 4, "R5": 5, "R6": 6, "R7": 7,
    "R8": 8, "R9": 9, "R10": 10, "R11": 11,
    "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "KBD": 24576, "SCREEN": 16384
}

c_comp_table = {
    "0": 0b0101010, "1": 0b0111111, "-1": 0b0111010,
    "D": 0b0001100, "A": 0b0110000, "!D": 0b0001101,
    "!A": 0b0110001, "-D": 0b0001111, "-A": 0b0110011,
    "D+1": 0b0011111, "A+1": 0b0110111, "D-1": 0b0001110,
    "A-1": 0b0110010, "D+A": 0b0000010, "D-A": 0b0010011,
    "A-D": 0b0000111, "D&A": 0b0000000, "D|A": 0b0010101,
    "M": 0b1110000, "!M": 0b1110001, "-M": 0b1110011,
    "M+1": 0b1110111, "M-1": 0b1110010, "D+M": 0b1000010,
    "D-M": 0b1010011, "M-D": 0b1000111, "D&M": 0b1000000,
    "D|M": 0b1010101
}

c_dest_table = {
    None: 0b000, "M": 0b001, "D": 0b010,
    "MD": 0b011, "A": 0b100, "AM": 0b101,
    "AD": 0b110, "AMD": 0b111
}

c_jump_table = {
    None: 0b000, "JGT": 0b001, "JEQ": 0b010,
    "JGE": 0b011, "JLT": 0b100, "JNE": 0b101,
    "JLE": 0b110, "JMP": 0b111
}

class ParserError(RuntimeError):
    pass

def read_source(file_name):
    # read symbolic asm source code from a given path
    source = []
    with open(file_name, 'r') as lines:
        for line in lines:
            source.append(line)
    return source

def source_beauty(line):
    # remove spaces and comments
    line = line.strip()
    line = line.replace(' ', '')
    if '//' in line:
        line = line[:line.find('//')]
    return line

def parse_instrction_type(instrction):
    if instrction == '':
        return 'e'
    elif instrction[0] == '@':
        return 'a'
    elif instrction[0] == '(':
        return 'l'
    else:
        return 'c'

def parse_label(line):
    label = line[line.find('(')+1:line.find(')')]
    if '(' in label or ')' in label:
        raise ParserError("Label not well defined")
    elif label == '':
        raise ParserError("Label not well defined")
    else:
        return label

def parse_a_instrction(instrction):
    dest_addr = instrction[1:]
    if dest_addr.isnumeric():
        return dest_addr
    elif dest_addr in symbol_table.keys():
        return symbol_table[dest_addr]
    elif dest_addr == '':
        raise ParserError("Address instrction contains error")

def parse_c_instrction(instrction):
    dest = None
    comp = None
    jump = None
    part = re.split('=|;', instrction)
    coma_times = instrction.count(';')
    eqal_times = instrction.count('=')
    if eqal_times == 1 and coma_times == 1:
        if instrction.index('=') < instrction.index(';'): # Make sure '=' is ahead of ';'
            dest = part[0]
            comp = part[1]
            jump = part[2]
        else:
            raise ParserError("In computation instrction, '=' should be ahead of ';'")
    elif eqal_times == 1 and coma_times == 0:
        dest = part[0]
        comp = part[1]
    elif eqal_times == 0 and coma_times == 1:
        comp = part[0]
        jump = part[1]
    else:
        raise ParserError("Computaion instrction contains something wrong")
    if [dest, comp, jump].count('') + [dest, comp, jump].count(None) >= 2:
        raise ParserError("Computaion instrction contains something wrong")
    return [dest, comp, jump]

def program_symbol_mapper(source):
    source_index = 0
    variable_index = 16
    program = [source_beauty(each_line) for each_line in source]
    # symbolic lables mapped to symbol_table
    for i, line in enumerate(program):
        line_type = parse_instrction_type(line)
        if line_type == 'l':
            try:
                label = parse_label(line)
            except ParserError as e:
                print("\033[91merror:\033[0m", e, end='')
                raise ParserError(f", which caused Mapping lable failed: \n [{i}] -> \033[96m{line}\033[0m")
            if label in symbol_table.keys():
                raise ParserError(f"Label define duplicated: \n [{i}] -> \033[96m{line}\033[0m")
            elif label == None:
                raise ParserError(f"Label empty: \n [{i}] -> \033[96m{line}\033[0m")
            else:
                symbol_table[parse_label(line)] = source_index
            continue
        elif line_type == 'e':
            continue
        source_index = source_index + 1
    print("\033[94mstage:\033[0m lable mapping - \033[92msucceed")
    # symbolic varibles mapped to symbol_table
    for line in program:
        line_type = parse_instrction_type(line)
        label = line[1:]
        if line_type == 'a' and label != '' and not label.isnumeric() and not label in symbol_table.keys():
            symbol_table[label] = variable_index
            variable_index = variable_index + 1
    print("\033[94mstage:\033[0m varibles mapping - \033[92msucceed")

def parse_generate_a_machine_code(dest_addr):
    return bin(0x0 ^ int(dest_addr))[2:].zfill(16) # 0x0 = 0b000000000000000

def parse_generate_c_machine_code(instrction_list):
    c_ins_machine_code = '111'
    if instrction_list[1] in c_comp_table.keys():
        c_ins_machine_code = c_ins_machine_code + bin(c_comp_table[instrction_list[1]])[2:].zfill(7)
    else:
        raise ParserError("Computaion instrction *comp contains error")
    if instrction_list[0] in c_dest_table.keys():
        c_ins_machine_code = c_ins_machine_code + bin(c_dest_table[instrction_list[0]])[2:].zfill(3)
    else:
        raise ParserError("Computaion instrction *dest contains error")
    if instrction_list[2] in c_jump_table.keys():
        c_ins_machine_code = c_ins_machine_code + bin(c_jump_table[instrction_list[2]])[2:].zfill(3)
    else:
        raise ParserError("Computaion instrction *jump contains error")
    return c_ins_machine_code

def asm(path):
    run_time = time.perf_counter()
    source = [x for x in read_source(path)]
    target_code = []
    error_i = 0
    try:
        program_symbol_mapper(source)
        print("\033[94mstage:\033[0m symbol table initialization - \033[92msucceed")
    except ParserError as e:
        error_i = error_i + 1 
        print(e)
        print("\033[94mstage:\033[0m symbol table initialization - \033[91mfailed")
    for i, each_line in enumerate(source):
        cleaned_line = source_beauty(each_line) # make this clean to parse
        line_type = parse_instrction_type(cleaned_line) # detect instrction type
        res = None
        if line_type == 'e' or line_type == 'l':
            continue
        elif line_type == 'a':
            try:
                res = parse_a_instrction(cleaned_line)
            except ParserError as e:
                error_i = error_i + 1 
                print("\033[91merror:\033[0m", e)
                print(f" [{i}] -> \033[96m{each_line}\033[0m", end='')
            else:
                try:
                    res = parse_generate_a_machine_code(res)
                except Exception as e:
                    error_i = error_i + 1 
                    print("\033[91merror:\033[0m", e)
                    print(f" [{i}] -> \033[96m{each_line}\033[0m", end='')
        elif line_type == 'c':
            try:
                res = parse_c_instrction(cleaned_line)
            except ParserError as e:
                error_i = error_i + 1 
                print("\033[91merror:\033[0m", e)
                print(f" [{i}] -> \033[96m{each_line}\033[0m", end='')
            else:
                try:
                    res = parse_generate_c_machine_code(res)
                except Exception as e:
                    error_i = error_i + 1 
                    print("\033[91merror:\033[0m", e)
                    print(f" [{i}] -> \033[96m{each_line}\033[0m", end='')

        try:
            if res and isinstance(int(res), int):
                target_code.append(res)
        except:
            pass

    run_time = time.perf_counter() - run_time

    if not error_i:
        print("\033[94mstage:\033[0m machine code generation - \033[92msucceed\033[0m")
    else:
        print(f"\033[94mstage:\033[0m machine code generation - \033[91mfailed, with {error_i} errors\033[0m")
    print(f"\033[95mstatistics:\033[0m generated {len(target_code)} lines in total, within {'%.4f' % run_time}s")


def main():
    cli_parser = argparse.ArgumentParser(description="Serves as a Hack Assembler.")
    cli_parser.add_argument("source_file", help="The name of the file to be convert.")
    cli_parser.add_argument("-o", help="Target file that contains generated machine code.", default=None)
    
    args = cli_parser.parse_args()

    asm(args.source_file)

if __name__ == "__main__":
    main()
