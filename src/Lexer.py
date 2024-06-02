from Token import Token, TokenType

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '\n' and self.current_char:
            self.advance()
        self.advance()  # skip the newline character

    def number(self):
        result = ''
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        if result.count('.') > 1:
            raise ValueError("Invalid number format")
        return Token(TokenType.NUMBER, float(result))

    def _id_or_keyword(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return Token(TokenType.KEYWORD, result) if result in {'declare', 'mut', 'fn', 'int', 'if', 'return', 'main', '@gcd', '@printU'} else Token(TokenType.IDENTIFIER, result)

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/':
                self.advance()
                if self.current_char == '/':
                    self.skip_comment()
                    continue

            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id_or_keyword()

            tokens_dict = {
                '+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE, '%': TokenType.MODULUS, '^': TokenType.POWER,
                '(': TokenType.LPAREN, ')': TokenType.RPAREN, '{': TokenType.LBRACE,
                '}': TokenType.RBRACE, ',': TokenType.COMMA, ':': TokenType.COLON,
                '=': TokenType.ASSIGN, ';': TokenType.SEMICOLON, '@': TokenType.AT,
                '>': TokenType.ARROW, '!': TokenType.NOT_EQUALS
            }

            if self.current_char in tokens_dict:
                token_type = tokens_dict[self.current_char]
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQUALS) if token_type == TokenType.EQUALS else Token(TokenType.NOT_EQUALS)
                return Token(token_type)

            raise ValueError(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF)
    
lexer = Lexer("""
declare mut varA: int = 12; // **Declares** a mutable variable. Declares sets a global scope rather than locally. We can see it in the function more clearly.
declare mut varB: int = 15;

declare fn gcd(a: int, b: int) -> int { // **Declares** a function, which allows it to be used globally. like mutability. Declaration is mutable, definition is immutable.
    if (a == 0) {
        return b;
    }
    return a % b;
}

fn main() -> int {
    declare varC = @gcd(varA,varB);
    @printU(varC); // uses printU or universal print which allows it to take any type and print it.
}
""")

while True:
    token = lexer.get_next_token()
    if token.type == TokenType.EOF:
        break