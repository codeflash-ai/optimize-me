from dataclasses import dataclass
from collections.abc import Callable


class SignalType:
  DEFAULT = 0
  COUNTER = 1
  HONDA_CHECKSUM = 2
  TOYOTA_CHECKSUM = 3
  BODY_CHECKSUM = 4
  VOLKSWAGEN_MQB_MEB_CHECKSUM = 5
  XOR_CHECKSUM = 6
  SUBARU_CHECKSUM = 7
  CHRYSLER_CHECKSUM = 8
  HKG_CAN_FD_CHECKSUM = 9
  FCA_GIORGIO_CHECKSUM = 10
  TESLA_CHECKSUM = 11
  PSA_CHECKSUM = 12


@dataclass
class Signal:
  name: str
  start_bit: int
  msb: int
  lsb: int
  size: int
  is_signed: bool
  factor: float
  offset: float
  is_little_endian: bool
  type: int = SignalType.DEFAULT
  calc_checksum: "Callable[[int, Signal, bytearray], int] | None" = None

