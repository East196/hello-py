from ctypes import *

msvcrt = cdll.msvcrt
message_string = "hello world!\n"
msvcrt.printf("%s", message_string)
print((c_int()))
print((c_long()))
print((c_ushort(65531)))
print((c_short(-5)))
print((c_char_p(b"ssss")))
print((c_char_p(b"ssss").value))


class Stt(Structure):
    _fields_ = [
        ("fire", c_int),
        ("water", c_int)
    ]

    def toString(self):
        return "" + str(self.fire) + " " + str(self.water)


class Unn(Union):
    _fields_ = [
        ("fire_long", c_long),
        ("fire_int", c_int),
        ("fire_char", c_char * 8)
    ]

    def toString(self):
        return "" + str(self.fire_long) + " " + str(self.fire_int) + " " + str(self.fire_char)


print((Stt(55, 2).toString()))
print((Unn(11).toString()))

msvcrt = cdll.msvcrt
message_string = "HelloWorld!\n"
msvcrt.printf("using c printf: %s", message_string)
