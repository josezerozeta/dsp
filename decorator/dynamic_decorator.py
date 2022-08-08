class FileWithLogging:
    def __init__(self, underlying):
        self.underlying = underlying

    def writelines(self, strings):
        self.underlying.writelines(strings)
        print(f'wrote {len(strings)} lines')

    def __iter__(self):
        return self.underlying.__iter__()

    def __next__(self):
        return self.underlying.__next__()

    def __getattr__(self, item):
        return getattr(self.__dict__['underlying'], item)

    def __delattr__(self, item):
        delattr(self.__dict__['underlying'], item)

    def __setattr__(self, key, value):
        if key == 'underlying':
            self.__dict__[key] = value
        else:
            setattr(self.__dict__['underlying'], key, value)


if __name__ == '__main__':
    file = FileWithLogging(open('hello.txt', 'w'))
    file.writelines(['hello', 'world'])
    file.write('testing')
    file.close()


