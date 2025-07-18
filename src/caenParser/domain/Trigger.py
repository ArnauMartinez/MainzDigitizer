from enum import Enum, auto

class TriggerMode(Enum):
    RISING_EDGE = auto()
    FALLING_EDGE = auto()

class ExternalTrigger(Enum):
    ACQ = auto() # When an external trigger is forced.
    BOTH = auto() # When an external trigger is forced, it is outputed on the GPO
    DISABLED = auto() # Represents no external trigger

class Trigger:
    def __init__(self, params):
        self._direction: TriggerMode = params.get("direction", TriggerMode.RISING_EDGE)
        self._bitmask: int = params.get("bitmask", 0)
        self._external: ExternalTrigger = params.get("external")
        self._thresholds: dict[int, int] = params.get("thresholds") # Tags are called levels inside trigger
        

    def copy(self):
        return Trigger({
            "direction": self._direction,
            "bitmask": self._bitmask,
            "external": self._external,
            "thresholds": self._thresholds.copy(),
        })