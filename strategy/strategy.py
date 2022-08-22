from abc import ABC
from enum import Enum, auto


class ListStrategy(ABC):
    def start(self, buffer):
        pass

    def end(self, buffer):
        pass

    def add_list_itme(self, buffer, item):
        pass


class MarkdownListStrategy(ListStrategy):
    def add_list_itme(self, buffer, item):
        buffer.append(f' * {item}\n')


class HtmlListStrategy(ListStrategy):
    def start(self, buffer):
        buffer.append('<ul>\n')

    def end(self, buffer):
        buffer.append('</ul>\n')

    def add_list_itme(self, buffer, item):
        buffer.append(f' <li>{item}</li>\n')


class OutputFormat(Enum):
    MARKDOWN = auto()
    HTML = auto()


class TextProcessor:
    def __init__(self):
        self.list_strategy = HtmlListStrategy()
        self.buffer = []

    def append_list(self, list_items):
        ls = self.list_strategy
        ls.start(self.buffer)
        for item in list_items:
            ls.add_list_itme(self.buffer, item)
        ls.end(self.buffer)

    def set_output_format(self, output_format):
        if output_format == OutputFormat.MARKDOWN:
            self.list_strategy = MarkdownListStrategy()
        elif output_format == OutputFormat.HTML:
            self.list_strategy = HtmlListStrategy()

    def clear(self):
        self.buffer.clear()

    def __str__(self):
        return ''.join(self.buffer)


if __name__ == '__main__':
    items = ['foo', 'bar', 'baz']

    tp = TextProcessor()
    tp.set_output_format(OutputFormat.MARKDOWN)
    tp.append_list(items)
    print(tp)

    tp.set_output_format(OutputFormat.HTML)
    tp.clear()
    tp.append_list(items)
    print(tp)

