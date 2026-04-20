from typing import BinaryIO

from .EmbPattern import EmbPattern


# --- Precomputed lookup tables for DST decoding ---
# DST encodes dx/dy using specific bits across 3 bytes.
# Instead of 20 getbit() calls per stitch, we precompute all 256*256*256
# combinations for byte2 (since byte0 and byte1 contribute partial bits
# to both dx and dy, but byte2 only has 4 relevant bits for each axis).
#
# dx bits: b2[2]=+81, b2[3]=-81, b1[2]=+27, b1[3]=-27,
#          b0[2]=+9, b0[3]=-9, b1[0]=+3, b1[1]=-3, b0[0]=+1, b0[1]=-1
# dy bits: b2[5]=+81, b2[4]=-81, b1[5]=+27, b1[4]=-27,
#          b0[5]=+9, b0[4]=-9, b1[7]=+3, b1[6]=-3, b0[7]=+1, b0[6]=-1
# dy is negated at the end.

def _build_dx_table():
    """Build 256-entry tables for each byte's contribution to dx."""
    t0 = [0] * 256
    t1 = [0] * 256
    t2 = [0] * 256
    for b in range(256):
        t0[b] = ((b >> 0) & 1) * 1 + ((b >> 1) & 1) * (-1) + ((b >> 2) & 1) * 9 + ((b >> 3) & 1) * (-9)
        t1[b] = ((b >> 0) & 1) * 3 + ((b >> 1) & 1) * (-3) + ((b >> 2) & 1) * 27 + ((b >> 3) & 1) * (-27)
        t2[b] = ((b >> 2) & 1) * 81 + ((b >> 3) & 1) * (-81)
    return t0, t1, t2

def _build_dy_table():
    """Build 256-entry tables for each byte's contribution to dy."""
    t0 = [0] * 256
    t1 = [0] * 256
    t2 = [0] * 256
    for b in range(256):
        t0[b] = ((b >> 7) & 1) * 1 + ((b >> 6) & 1) * (-1) + ((b >> 5) & 1) * 9 + ((b >> 4) & 1) * (-9)
        t1[b] = ((b >> 7) & 1) * 3 + ((b >> 6) & 1) * (-3) + ((b >> 5) & 1) * 27 + ((b >> 4) & 1) * (-27)
        t2[b] = ((b >> 5) & 1) * 81 + ((b >> 4) & 1) * (-81)
    return t0, t1, t2

_DX0, _DX1, _DX2 = _build_dx_table()
_DY0, _DY1, _DY2 = _build_dy_table()


def process_header_info(out: EmbPattern, prefix, value):
    if prefix == "LA":
        out.metadata("name", value)
    elif prefix == "AU":
        out.metadata("author", value)
    elif prefix == "CP":
        out.metadata("copyright", value)
    elif prefix == "TC":
        values = [x.strip() for x in value.split(",")]
        out.add_thread({"hex": values[0], "description": values[1], "catalog": values[2]})
    else:
        out.metadata(prefix, value)


def dst_read_header(f: BinaryIO, out: EmbPattern):
    header = f.read(512)
    start = 0
    for i, element in enumerate(header):
        if (
            element == 13 or element == 10 or element == "\n" or element == "\r"
        ):  # 13 =='\r', 10 = '\n'
            end = i
            data = header[start:end]
            start = end
            try:
                line = data.decode("utf8").strip()
                if len(line) > 3:
                    process_header_info(out, line[0:2].strip(), line[3:].strip())
            except UnicodeDecodeError:  # Non-utf8 information. See #83
                continue


def dst_read_stitches(f: BinaryIO, out: EmbPattern, settings=None):
    # Bulk-read entire stitch data at once
    raw = f.read()
    data_len = len(raw)
    if data_len < 3:
        out.end()
        return

    # Local references for speed
    dx0, dx1, dx2 = _DX0, _DX1, _DX2
    dy0, dy1, dy2 = _DY0, _DY1, _DY2
    stitch = out.stitch
    move = out.move
    color_change = out.color_change
    sequin_mode_fn = out.sequin_mode
    sequin_eject = out.sequin_eject

    sequin_mode = False
    offset = 0
    end_offset = data_len - 2  # Need at least 3 bytes

    while offset < end_offset:
        b0 = raw[offset]
        b1 = raw[offset + 1]
        b2 = raw[offset + 2]
        offset += 3

        dx = dx0[b0] + dx1[b1] + dx2[b2]
        dy = -(dy0[b0] + dy1[b1] + dy2[b2])

        if b2 & 0b11110011 == 0b11110011:
            break
        elif b2 & 0b11000011 == 0b11000011:
            color_change(dx, dy)
        elif b2 & 0b01000011 == 0b01000011:
            sequin_mode_fn(dx, dy)
            sequin_mode = not sequin_mode
        elif b2 & 0b10000011 == 0b10000011:
            if sequin_mode:
                sequin_eject(dx, dy)
            else:
                move(dx, dy)
        else:
            stitch(dx, dy)

    out.end()

    count_max = 3
    clipping = True
    trim_distance = None
    if settings is not None:
        count_max = settings.get("trim_at", count_max)
        trim_distance = settings.get("trim_distance", trim_distance)
        clipping = settings.get("clipping", clipping)
    if trim_distance is not None:
        trim_distance *= 10  # Pixels per mm. Native units are 1/10 mm.
    out.interpolate_trims(count_max, trim_distance, clipping)


def read(f: BinaryIO, out: EmbPattern, settings=None):
    dst_read_header(f, out)
    dst_read_stitches(f, out, settings)
