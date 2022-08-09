class Buffer:
    def __init__(self, width=30, height=20):
        self.height = height
        self.width = width
        self.buffer = [' '] * (width * height)

    def __getitem__(self, item):
        return self.buffer.__getitem__(item)

    def write(self, text):
        self.buffer += text


class Viewport:
    def __init__(self, buffer=Buffer()):
        self.buffer = buffer
        self.offset = 0

    def get_char_at(self, index):
        return self.buffer[index + self.offset]

    def append(self, text):
        self.buffer += text


class Console:
    def __init__(self):
        buffer = Buffer()
        self.current_viewport = Viewport(buffer)
        self.buffers = [buffer]
        self.viewports = [self.current_viewport]

    def write(self, text):
        self.current_viewport.buffer.write(text)

    def get_char_at(self, index):
        return self.current_viewport.get_char_at(index)


if __name__ == '__main__':
    console = Console()
    console.write('hello')
    ch = console.get_char_at(0)


