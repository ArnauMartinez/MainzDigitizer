from dataclasses import dataclass


@dataclass
class DigitizerDTO:
    id: str
    family: str
    version: str
    serial: str
    channels: int
    resolution: float
    frequency: float
    max_samples: int
    channel_groups: int
    zero_suppression: bool
    inspection: bool
    dual_edge: bool
    voltage_range: tuple[float, float]
    windows: list[int]

    def copy(self):
        return DigitizerDTO(
            id=self.id,
            family=self.family,
            version=self.version,
            serial=self.serial,
            channels=self.channels,
            resolution=self.resolution,
            frequency=self.frequency,
            max_samples=self.max_samples,
            channel_groups=self.channel_groups,
            zero_suppression=self.zero_suppression,
            inspection=self.inspection,
            dual_edge=self.dual_edge,
            voltage_range=self.voltage_range,
            windows=self.windows.copy()
        )

