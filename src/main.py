from .information import Signal


def set_value(msg: bytearray, sig: Signal, ival: int) -> bytearray:
    i = sig.lsb // 8
    bits = sig.size
    if sig.size < 64:
        ival &= (1 << sig.size) - 1
    while 0 <= i < len(msg) and bits > 0:
        shift = sig.lsb % 8 if (sig.lsb // 8) == i else 0
        size = min(bits, 8 - shift)
        mask = ((1 << size) - 1) << shift
        msg[i] &= ~mask
        msg[i] |= (ival & ((1 << size) - 1)) << shift
        bits -= size
        ival >>= size
        i = i + 1 if sig.is_little_endian else i - 1
    return msg
