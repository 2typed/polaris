class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, value):
        self.value = value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

# Helper function to convert AST to JSON serializable dictionary
def ast_to_dict(node):
    if isinstance(node, BinOp):
        return {
            'type': 'BinOp',
            'op': node.op.type.name,
            'left': ast_to_dict(node.left),
            'right': ast_to_dict(node.right)
        }
    elif isinstance(node, UnaryOp):
        return {
            'type': 'UnaryOp',
            'op': node.op.type.name,
            'expr': ast_to_dict(node.expr)
        }
    elif isinstance(node, Num):
        return {
            'type': 'Num',
            'value': node.value
        }
    else:
        raise Exception('Unknown node type')
