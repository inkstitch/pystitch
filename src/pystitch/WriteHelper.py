import struct

_pack_B = struct.Struct('B').pack
_pack_le_H = struct.Struct('<H').pack
_pack_be_H = struct.Struct('>H').pack
_pack_le_I = struct.Struct('<I').pack
_pack_be_I = struct.Struct('>I').pack
_pack_le_f = struct.Struct('<f').pack


def write_int_array_8(stream, int_array):
    stream.write(bytes(v & 0xFF for v in int_array))


def write_int_8(stream, value):
    stream.write(_pack_B(value & 0xFF))


def write_int_16le(stream, value):
    stream.write(_pack_le_H(value & 0xFFFF))


def write_int_16be(stream, value):
    stream.write(_pack_be_H(value & 0xFFFF))


def write_int_24le(stream, value):
    stream.write(bytes([
        value & 0xFF,
        (value >> 8) & 0xFF,
        (value >> 16) & 0xFF,
    ]))


def write_int_24be(stream, value):
    stream.write(bytes([
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF,
    ]))


def write_int_32le(stream, value):
    stream.write(_pack_le_I(value & 0xFFFFFFFF))


def write_int_32be(stream, value):
    stream.write(_pack_be_I(value & 0xFFFFFFFF))


def write_float_32le(stream, value):
    stream.write(_pack_le_f(float(value)))


def write_string(stream, string, encoding="utf8"):
    stream.write(bytes(string, encoding))


def write_string_utf8(stream, string):
    stream.write(bytes(string, "utf8"))
