import struct

_unpack_b = struct.Struct('b').unpack
_unpack_B = struct.Struct('B').unpack
_unpack_le_h = struct.Struct('<h').unpack
_unpack_le_H = struct.Struct('<H').unpack
_unpack_be_h = struct.Struct('>h').unpack
_unpack_be_H = struct.Struct('>H').unpack
_unpack_le_i = struct.Struct('<i').unpack
_unpack_le_I = struct.Struct('<I').unpack
_unpack_be_i = struct.Struct('>i').unpack
_unpack_be_I = struct.Struct('>I').unpack


def signed8(b):
    if b > 127:
        return b - 256
    return b


def signed16(v):
    v &= 0xFFFF
    if v > 0x7FFF:
        return v - 0x10000
    return v


def signed24(v):
    v &= 0xFFFFFF
    if v > 0x7FFFFF:
        return v - 0x1000000
    return v


def read_signed(stream, n):
    data = stream.read(n)
    if len(data) != n:
        return []
    return list(struct.unpack(f'{n}b', data))


def read_sint_8(stream):
    data = stream.read(1)
    if len(data) == 1:
        return _unpack_b(data)[0]
    return None


def read_int_8(stream):
    data = stream.read(1)
    if len(data) == 1:
        return data[0]
    return None


def read_int_16le(stream):
    data = stream.read(2)
    if len(data) == 2:
        return _unpack_le_H(data)[0]
    return None


def read_int_16be(stream):
    data = stream.read(2)
    if len(data) == 2:
        return _unpack_be_H(data)[0]
    return None


def read_int_24le(stream):
    data = stream.read(3)
    if len(data) == 3:
        return data[0] | (data[1] << 8) | (data[2] << 16)
    return None


def read_int_24be(stream):
    data = stream.read(3)
    if len(data) == 3:
        return data[2] | (data[1] << 8) | (data[0] << 16)
    return None


def read_int_32le(stream):
    data = stream.read(4)
    if len(data) == 4:
        return _unpack_le_I(data)[0]
    return None


def read_int_32be(stream):
    data = stream.read(4)
    if len(data) == 4:
        return _unpack_be_I(data)[0]
    return None


def read_string_8(stream, length):
    data = stream.read(length)
    try:
        return data.decode("utf8")
    except (UnicodeDecodeError, AttributeError):
        return None


def read_string_16(stream, length):
    data = stream.read(length)
    try:
        return data.decode("utf16")
    except (UnicodeDecodeError, AttributeError):
        return None
