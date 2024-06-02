from llvmlite import ir

class IRGenerator:
    def __init__(self):
        self.module = ir.Module(name="module")
        self.builder = None
        self.func = None
        self.block = None

    def generate_ir(self, ast):
        # Define the main function
        func_type = ir.FunctionType(ir.DoubleType(), ())
        self.func = ir.Function(self.module, func_type, name="main")
        self.block = self.func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(self.block)

        # Generate the IR code
        result = self.generate_code(ast)
        self.builder.ret(result)

        return self.module

    def generate_code(self, node):
        if node['type'] == 'Num':
            return ir.Constant(ir.DoubleType(), node['value'])
        elif node['type'] == 'BinOp':
            left = self.generate_code(node['left'])
            right = self.generate_code(node['right'])
            if node['op'] == 'PLUS':
                return self.builder.fadd(left, right, name="addtmp")
            elif node['op'] == 'MINUS':
                return self.builder.fsub(left, right, name="subtmp")
            elif node['op'] == 'MULTIPLY':
                return self.builder.fmul(left, right, name="multmp")
            elif node['op'] == 'DIVIDE':
                return self.builder.fdiv(left, right, name="divtmp")
            elif node['op'] == 'MODULUS':
                return self.builder.frem(left, right, name="modtmp")
            elif node['op'] == 'POWER':
                # LLVM does not have a direct power function; we will call the LLVM intrinsic function for power
                pow_func = ir.Function(self.module, ir.FunctionType(ir.DoubleType(), [ir.DoubleType(), ir.DoubleType()]), name="llvm.pow.f64")
                return self.builder.call(pow_func, [left, right], name="powtmp")
        elif node['type'] == 'UnaryOp':
            expr = self.generate_code(node['expr'])
            if node['op'] == 'PLUS':
                return expr
            elif node['op'] == 'MINUS':
                return self.builder.fsub(ir.Constant(ir.DoubleType(), 0.0), expr, name="negtmp")
        else:
            raise Exception(f"Unknown node type: {node['type']}")