from numbers import Real


class Descriptor:
    def __init__(self, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError("expected " + str(self.expected_type))
        super().__set__(instance, value)


class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Expected >= 0")
        super().__set__(instance, value)


class FixedSized(Descriptor):
    def __init__(self, name, size):
        if not isinstance(size, int):
            raise TypeError("size must be int")
        super().__init__(name)
        self.size = size

    def __set__(self, instance, value):
        if len(value) != self.size:
            raise ValueError("size must be = " + str(self.size))
        super().__set__(instance, value)


class String(Typed):
    expected_type = str


class Integer(Typed):
    expected_type = int


class UnsignedReal(Typed, Unsigned):
    expected_type = Real


class StringOfFixedSize(String, FixedSized):
    pass
