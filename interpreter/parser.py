from enum import Enum, auto


class Token:
    class Type(Enum):
        INTEGER = auto()
        PLUS = auto()
        MINUS = auto()
        LEFT_PAREN = auto()
        RIGHT_PAREN = auto()

    def __init__(self, type_enum, text):
        self.text = text
        self.type = type_enum

    def __str__(self):
        return f'`{self.text}`'
        

def lex(input_data):
    result = []
    i = 0
    while i < len(input_data):
        if input_data[i] == '+':
            result.append(Token(Token.Type.PLUS, '+'))
        elif input_data[i] == '-':
            result.append(Token(Token.Type.MINUS, '-'))
        elif input_data[i] == '(':
            result.append(Token(Token.Type.LEFT_PAREN, '('))
        elif input_data[i] == ')':
            result.append(Token(Token.Type.RIGHT_PAREN, ')'))
        else:
            digits = [input_data[i]]
            for j in range(i+1, len(input_data)):
                if input_data[j].isdigit():
                    digits.append(input_data[j])
                    i += 1
                else:
                    result.append(Token(Token.Type.INTEGER, ''.join(digits)))
                    break
        i += 1

    return result


class Integer:
    def __init__(self, value):
        self.value = value


class BinaryExpression:
    class Type(Enum):
        ADDITION = auto()
        SUBTRACTION = auto()

    def __init__(self):
        self.type = None
        self.left = None
        self.right = None

    @property
    def value(self):
        if self.type == self.Type.ADDITION:
            return self.left.value + self.right.value
        else:
            return self.left.value - self.right.value


def parse(tokens):
    result = BinaryExpression()
    have_lhs = False
    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.type == Token.Type.INTEGER:
            integer = Integer(int(token.text))
            if not have_lhs:
                result.left = integer
                have_lhs = True
            else:
                result.right = integer
        elif token.type == Token.Type.PLUS:
            result.type = BinaryExpression.Type.ADDITION
        elif token.type == Token.Type.MINUS:
            result.type = BinaryExpression.Type.SUBTRACTION
        elif token.type == Token.Type.LEFT_PAREN:
            j = i
            while j < len(tokens):
                if tokens[j].type == Token.Type.RIGHT_PAREN:
                    break
                j += 1
            subexpression = tokens[i+1:j]
            element = parse(subexpression)
            if not have_lhs:
                result.left = element
                have_lhs = True
            else:
                result.right = element
            i = j
        i += 1
    return result


def calc(input_data):
    tokens = lex(input_data)
    print(' '.join(map(str, tokens)))

    parsed = parse(tokens)
    print(f'{input_data} = {parsed.value}')


if __name__ == '__main__':
    calc('(13+4)-(12+1)')
