

class Digitizer:

    decimation_factors = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

    def __init__(self, params):
        self._id: str = params.get("id")
        self._family: str = params.get("family")
        self._version: str = params.get("version")
        self._serial_number: str= params.get("serial_number")

        self._num_channels: int = params.get("num_channels")
        self._bits: float = params.get("bits")
        self._frequency : float = params.get("frequency")
        self._max_samples: int = params.get("max_samples")
        self._channel_groups: int = params.get("channel_groups", 0)
        self._zeroSupression: bool = params.get("zero_supression", False)
        self._inspection: bool = params.get("inspection", False)
        self._dual_edge: bool = params.get("dual_edge", False)
        self._voltage_range: tuple[float,float] = params.get("voltage_range", (0,0))
        self._windows: list[int] = params.get("windows", [])

    @property
    def num_channels(self):
        return self._num_channels
    
    @property
    def id(self):
        return self._id
    
    @property
    def family(self):
        return self._family
    
    @property
    def version(self):
        return self._version
    
    @property
    def serial_number(self):
        return self._serial_number
    
    @property
    def bits(self):
        return self._bits

    @property
    def frequency(self):
        return self._frequency
    
    @property
    def max_samples(self):
        return self._max_samples
    
    @property
    def channel_groups(self):
        return self._channel_groups
    
    @property
    def zero_supression(self):
        return self._zeroSupression
    
    @property
    def inspection(self):
        return self._inspection
    
    @property
    def dual_edge(self):
        return self._dual_edge
    
    @property
    def voltage_range(self):
        return self._voltage_range
    
    @property
    def windows(self):
        return self._windows.copy()
    
    def copy(self):
        return Digitizer({
            "id": self._id,
            "family": self._family,
            "version": self._version,
            "serial_number": self._serial_number,
            "num_channels": self._num_channels,
            "bits": self._bits,
            "frequency": self._frequency,
            "max_samples": self._max_samples,
            "channel_groups": self._channel_groups,
            "zero_supression": self._zeroSupression,
            "inspection": self._inspection,
            "dual_edge": self._dual_edge,
            "voltage_range": self._voltage_range,
            "windows": self._windows.copy()
        })


    

    


        