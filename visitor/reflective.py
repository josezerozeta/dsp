from abc import ABC


class Expression(ABC):
    pass


class DoubleExpression(Expression):
    def __init__(self, value):
        self.value = value


class AdditionExpression(Expression):
    def __init__(self, left, right):
        self.right = right
        self.left = left


class ExpressionPrinter:
    @staticmethod
    def print(exp, buffer):
        if isinstance(exp, DoubleExpression):
            buffer.append(str(exp.value))
        elif isinstance(exp, AdditionExpression):
            buffer.append('(')
            ExpressionPrinter.print(exp.left, buffer)
            buffer.append('+')
            ExpressionPrinter.print(exp.right, buffer)
            buffer.append(')')

    Expression.print = lambda self, buffer: ExpressionPrinter.print(self, buffer)


if __name__ == '__main__':
    # 1 + (2+3)
    e = AdditionExpression(
        DoubleExpression(1),
        AdditionExpression(
            DoubleExpression(2),
            DoubleExpression(3)
        )
    )

    buffer = []
    e.print(buffer)
    print(''.join(buffer))
