import subprocess

def compile_ir(ir_filename, obj_filename="a"):
    obj = subprocess.call(['clang', ir_filename, '-o', obj_filename])
    return obj