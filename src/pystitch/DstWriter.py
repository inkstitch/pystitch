from typing import BinaryIO

from .EmbConstant import *
from .EmbPattern import EmbPattern
from .WriteHelper import write_string_utf8

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_UTILIZE
FULL_JUMP = False
ROUND = True
MAX_JUMP_DISTANCE = 121
MAX_STITCH_DISTANCE = 121

PPMM = 10
DSTHEADERSIZE = 512


def bit(b):
    return 1 << b


# Pre-compute lookup tables for x and y encoding (balanced ternary-like).
# Each axis maps an integer delta [-121..121] to (b0_bits, b1_bits, b2_bits).
def _build_xy_tables():
    xt = {}
    for val in range(-121, 122):
        b0 = b1 = b2 = 0
        v = val
        if v > 40:
            b2 |= 0x04
            v -= 81
        if v < -40:
            b2 |= 0x08
            v += 81
        if v > 13:
            b1 |= 0x04
            v -= 27
        if v < -13:
            b1 |= 0x08
            v += 27
        if v > 4:
            b0 |= 0x04
            v -= 9
        if v < -4:
            b0 |= 0x08
            v += 9
        if v > 1:
            b1 |= 0x01
            v -= 3
        if v < -1:
            b1 |= 0x02
            v += 3
        if v > 0:
            b0 |= 0x01
            v -= 1
        if v < 0:
            b0 |= 0x02
            v += 1
        xt[val] = (b0, b1, b2)
    yt = {}
    for val in range(-121, 122):
        b0 = b1 = b2 = 0
        v = -val  # flips y
        if v > 40:
            b2 |= 0x20
            v -= 81
        if v < -40:
            b2 |= 0x10
            v += 81
        if v > 13:
            b1 |= 0x20
            v -= 27
        if v < -13:
            b1 |= 0x10
            v += 27
        if v > 4:
            b0 |= 0x20
            v -= 9
        if v < -4:
            b0 |= 0x10
            v += 9
        if v > 1:
            b1 |= 0x80
            v -= 3
        if v < -1:
            b1 |= 0x40
            v += 3
        if v > 0:
            b0 |= 0x80
            v -= 1
        if v < 0:
            b0 |= 0x40
            v += 1
        yt[val] = (b0, b1, b2)
    return xt, yt

_X_TABLE, _Y_TABLE = _build_xy_tables()

# Lazy-built lookup tables for STITCH and JUMP commands.
# Built on first access to avoid 0.115s import overhead.
_STITCH_LUT = None
_JUMP_LUT = None

def _ensure_luts():
    global _STITCH_LUT, _JUMP_LUT
    if _STITCH_LUT is not None:
        return
    stitch_lut = {}
    jump_lut = {}
    xt = _X_TABLE
    yt = _Y_TABLE
    for _dx in range(-121, 122):
        _xb = xt[_dx]
        for _dy in range(-121, 122):
            _yb = yt[_dy]
            _key = (_dx, _dy)
            stitch_lut[_key] = bytes((_xb[0] | _yb[0], _xb[1] | _yb[1], 0x03 | _xb[2] | _yb[2]))
            jump_lut[_key] = bytes((_xb[0] | _yb[0], _xb[1] | _yb[1], 0x83 | _xb[2] | _yb[2]))
    _STITCH_LUT = stitch_lut
    _JUMP_LUT = jump_lut

_COLOR_CHANGE_RECORD = bytes((0, 0, 0b11000011))
_STOP_RECORD = bytes((0, 0, 0b11000011))
_END_RECORD = bytes((0, 0, 0b11110011))
_SEQUIN_MODE_RECORD = bytes((0, 0, 0b01000011))


def encode_record(x, y, flags):
    if flags == COLOR_CHANGE:
        return _COLOR_CHANGE_RECORD
    elif flags == STOP:
        return _STOP_RECORD
    elif flags == END:
        return _END_RECORD
    elif flags == SEQUIN_MODE:
        return _SEQUIN_MODE_RECORD
    _ensure_luts()
    assert _STITCH_LUT is not None
    assert _JUMP_LUT is not None
    if flags == STITCH:
        return _STITCH_LUT.get((int(x), int(y))) or _encode_record_slow(x, y, flags)
    elif flags == JUMP:
        return _JUMP_LUT.get((int(x), int(y))) or _encode_record_slow(x, y, flags)
    elif flags == SEQUIN_EJECT:
        return _JUMP_LUT.get((int(x), int(y))) or _encode_record_slow(x, y, flags)
    return bytes((0, 0, 0))


def _encode_record_slow(x, y, flags):
    """Fallback for values outside lookup table range."""
    y = -y
    b0 = b1 = b2 = 0
    if flags == JUMP or flags == SEQUIN_EJECT:
        b2 += 0x80
    if flags == STITCH or flags == JUMP or flags == SEQUIN_EJECT:
        b2 |= 0x03
        if x > 40:
            b2 |= 0x04
            x -= 81
        if x < -40:
            b2 |= 0x08
            x += 81
        if x > 13:
            b1 |= 0x04
            x -= 27
        if x < -13:
            b1 |= 0x08
            x += 27
        if x > 4:
            b0 |= 0x04
            x -= 9
        if x < -4:
            b0 |= 0x08
            x += 9
        if x > 1:
            b1 |= 0x01
            x -= 3
        if x < -1:
            b1 |= 0x02
            x += 3
        if x > 0:
            b0 |= 0x01
            x -= 1
        if x < 0:
            b0 |= 0x02
            x += 1
        if y > 40:
            b2 |= 0x20
            y -= 81
        if y < -40:
            b2 |= 0x10
            y += 81
        if y > 13:
            b1 |= 0x20
            y -= 27
        if y < -13:
            b1 |= 0x10
            y += 27
        if y > 4:
            b0 |= 0x20
            y -= 9
        if y < -4:
            b0 |= 0x10
            y += 9
        if y > 1:
            b1 |= 0x80
            y -= 3
        if y < -1:
            b1 |= 0x40
            y += 3
        if y > 0:
            b0 |= 0x80
            y -= 1
        if y < 0:
            b0 |= 0x40
            y += 1
    return bytes((b0, b1, b2))


def write(pattern: EmbPattern, f: BinaryIO, settings=None):
    extended_header = False
    trim_at = 3
    if settings is not None:
        extended_header = settings.get(
            "extended header", extended_header
        )  # deprecated, use version="extended"
        version = settings.get("version", "default")
        if version == "extended":
            extended_header = True
        trim_at = settings.get("trim_at", trim_at)
    bounds = pattern.bounds()

    name = pattern.get_metadata("name", "Untitled")

    write_string_utf8(f, "LA:%-16s\r" % name)
    write_string_utf8(f, "ST:%7d\r" % pattern.count_stitches())
    write_string_utf8(f, "CO:%3d\r" % (pattern.count_color_changes()
                      + pattern.count_stitch_commands(STOP)))
    write_string_utf8(f, "+X:%5d\r" % abs(bounds[2]))
    write_string_utf8(f, "-X:%5d\r" % abs(bounds[0]))
    write_string_utf8(f, "+Y:%5d\r" % abs(bounds[3]))
    write_string_utf8(f, "-Y:%5d\r" % abs(bounds[1]))
    ax = 0
    ay = 0
    if len(pattern.stitches) > 0:
        last = len(pattern.stitches) - 1
        ax = int(pattern.stitches[last][0])
        ay = -int(pattern.stitches[last][1])
    if ax >= 0:
        write_string_utf8(f, "AX:+%5d\r" % ax)
    else:
        write_string_utf8(f, "AX:-%5d\r" % abs(ax))
    if ay >= 0:
        write_string_utf8(f, "AY:+%5d\r" % ay)
    else:
        write_string_utf8(f, "AY:-%5d\r" % abs(ay))
    write_string_utf8(f, "MX:+%5d\r" % 0)
    write_string_utf8(f, "MY:+%5d\r" % 0)
    write_string_utf8(f, "PD:%6s\r" % "******")
    if extended_header:
        author = pattern.get_metadata("author")
        if author is not None:
            write_string_utf8(f, "AU:%s\r" % author)
        meta_copyright = pattern.get_metadata("copyright")
        if meta_copyright is not None:
            write_string_utf8(f, "CP:%s\r" % meta_copyright)
        if len(pattern.threadlist) > 0:
            for thread in pattern.threadlist:
                write_string_utf8(
                    f,
                    "TC:%s,%s,%s\r"
                    % (thread.hex_color(), thread.description, thread.catalog_number),
                )
    f.write(b"\x1a")
    for i in range(f.tell(), DSTHEADERSIZE):
        f.write(b"\x20")  # space

    stitches = pattern.stitches
    xx = 0
    yy = 0
    chunks = []
    chunks_append = chunks.append
    # Ensure LUTs are built (lazy init)
    _ensure_luts()
    assert _STITCH_LUT is not None
    assert _JUMP_LUT is not None
    # Local refs for hot loop
    _stitch_lut = _STITCH_LUT
    _jump_lut = _JUMP_LUT
    _round = round
    _STITCH = STITCH
    _TRIM = TRIM
    _JUMP = JUMP
    _COMMAND_MASK = COMMAND_MASK
    _encode = encode_record
    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2] & _COMMAND_MASK
        dx = int(_round(x - xx))
        dy = int(_round(y - yy))

        xx += dx
        yy += dy
        if data == _STITCH:
            rec = _stitch_lut.get((dx, dy))
            if rec is not None:
                chunks_append(rec)
            else:
                chunks_append(_encode(dx, dy, _STITCH))
        elif data == _TRIM:
            delta = -4
            chunks_append(_jump_lut[(2, 2)])
            for p in range(1, trim_at - 1):
                chunks_append(_jump_lut[(delta, delta)])
                delta = -delta
            chunks_append(_jump_lut[(int(delta / 2), int(delta / 2))])
        elif data == _JUMP:
            rec = _jump_lut.get((dx, dy))
            if rec is not None:
                chunks_append(rec)
            else:
                chunks_append(_encode(dx, dy, _JUMP))
        else:
            chunks_append(_encode(dx, dy, data))
    f.write(b"".join(chunks))
