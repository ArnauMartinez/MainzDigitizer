from dataclasses import dataclass
from datetime import datetime

@dataclass
class EventDTO:
    id: int
    settings_id: int
    digitizer_id: str
    time_stamp: int
    clock_time: datetime
    trigger_shift: int
    trace: dict[int, list[int]]  # Assuming trace is a dictionary with channel indices as keys and lists of integers as values
    
    
    def copy(self):
        return EventDTO(
            id=self.id,
            settings_id=self.settings_id,
            digitizer_id=self.digitizer_id,
            time_stamp=self.time_stamp,
            clock_time=self.clock_time,
            trigger_shift=self.trigger_shift,
            trace={k: v.copy() for k, v in self.trace.items()} if self.trace is not None else None
        )
