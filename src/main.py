import sys
import json
from Lexer import Lexer
from AST import ast_to_dict
from Parser import Parser
from IR import IRGenerator
from Compiler import compile_ir
from tempfile import TemporaryFile

SINGLEARG_FLAGS = {
    '-h', '-help', '--version'
}

if __name__ == "__main__":
    argv = sys.argv
    input_code = None
    flag = None
    if len(argv) < 3:
        if argv[1] in SINGLEARG_FLAGS:
            flag = argv[1].replace('-', '')
        else:
            print("Missing input file. Usage: polaris [src-flags] [input-file] [output-file]")
            exit(1)
    else:
        if argv[1].startswith('-'):
            flag = argv[1].replace('-', '')
            if len(argv) < 3:
                print("Missing input file. Usage: polaris [src-flags] [compiler-flags] [input-file] [output-file]")
                exit(1)
            input_file = argv[2]
            try: output_filename = argv[3]
            except: output_filename = "a"
        else:
            flag = 'build'
            input_file = argv[1]
            try: output_filename = argv[2]
            except: output_filename = "a"

        with open(input_file, 'r') as f:
            input_code = f.read()

    lexer = Lexer(input_code)
    parser = Parser(lexer)
    if flag == 'build':
        AST = json.loads(json.dumps(ast_to_dict(parser.parse())))
        IRG = IRGenerator()
        IR_MODULE = IRG.generate_ir(AST)
        IR_TEMP = TemporaryFile(prefix='ir_',suffix='.ll')
        IR_TEMP.write(bytearray(str(IR_MODULE),encoding='utf 8'))
        IR_TEMP.seek(0)
        OBJ = compile_ir(IR_TEMP.name, output_filename)
        print('Sucessfully compiled.')
    elif flag == "ir":
        AST = json.loads(json.dumps(ast_to_dict(parser.parse())))
        IRG = IRGenerator()
        IR_MODULE = IRG.generate_ir(AST)
        with open(str(output_filename+'.ll'), "w") as IR_FILE:
            IR_FILE.write(str(IR_MODULE))
    elif flag in {'help', 'h'}:
        print('Usage: polaris [src-flags] [compiler-flags] [input-file] [output-file]')