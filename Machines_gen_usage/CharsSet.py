import string


def globalChars():
    chars = string.punctuation + string.digits + ''.join(chr(i) for i in range(0, 256))
    return chars


def uppercaseCharSet():
    chars = string.ascii_uppercase + ''.join(chr(i) for i in range(192, 223) if chr(i) not in string.ascii_uppercase)
    return chars


def lowercaseCharSet():
    chars = string.ascii_lowercase + ''.join(chr(i) for i in range(224, 255) if chr(i) not in string.ascii_lowercase)
    return chars


def digitChars():
    chars = string.digits
    return chars


def obtainSet(first: str, second: str):
    if ord(first) > ord(second):
        return first + second
    return ''.join(chr(i) for i in range(ord(first), ord(second) + 1))
