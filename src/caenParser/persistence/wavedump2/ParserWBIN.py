from types import TypedDict
from abc import abstractmethod
import io, struct

from caenParser.persistence import FileParser


# e6 means that the value is multiplied by 10**6 for better precision

class channelDict(TypedDict):
    baseline: int
    sample_to_mv_e6: int
    channel_gain_e6: int
    channel_threshold_lsb : int




class ParserWBIN(FileParser):
    def __init__(self):
        super().__init__()
        self._fileObj : io.BufferedReader = None
        self._device_model: int = None
        self._devide_PID: int = None
        self._num_bits: int = None
        self._frequency : int = None
        self._device_trigger_source: int = None
        self._pre_trigger: int = None # Number of samples before trigger, although in 1.0 digitizers is the post trigger
        self._num_channels: int= None
        self._channel_dict: dict[int, channelDict] = {}  # This should be set to the events object or


    def open(self, file_path):
        try: 
            self._fileObj =  open(file_path, 'r')
        except Exception as e:
            raise ValueError(f"Error Opening the file: {e}")
        

    def parse(self):
        """
        Parses the WBIN file and extracts relevant information.
        This method should be implemented to read the file and populate the attributes.
        """
        # Implementation goes here
        with open(self.file_path, 'rb') as open_file:
            self._read_header(open_file)
            self._read_data(open_file)
            self._translate_objects(open_file)
        
        return 


    def _read_header(self, open_file: io.BufferedReader) -> None:
        """
        Reads the header of the WBIN file.
        This method should be implemented to parse the header data.
        """
        header_fmt = "@ I I I I I H I"
        header_size = struct.calcsize(header_fmt)
        header_data = open_file.read(header_size)
        if len(header_data) < header_size:
            raise ValueError("Not enough data to read header")
        header_values = struct.unpack(header_fmt, header_data)

        self._device_model = header_values[0]
        self._devide_PID = header_values[1]
        self._num_bits = header_values[2]
        self._frequency = (10 **12) / header_values[3]
        self._device_trigger_source = header_values[4]
        self._pre_trigger = header_values[5]
        self._num_channels = header_values[6]

        header_fmt = "@ I I I i"
        header_size = struct.calcsize(header_fmt)
        for channel in range(self._num_channels):
            header_data = open_file.read(header_size)
            if len(header_data) < header_size:
                raise ValueError(f"Not enough data to read channel {channel} header")
            channel_values = struct.unpack(header_fmt, header_data)
            self._channel_dict[channel] = {
                "baseline": channel_values[0],
                "sample_to_mv_e6": channel_values[1],
                "channel_gain_e6": channel_values[2],
                "channel_threshold_lsb": channel_values[3]
            }

    @abstractmethod
    def _read_data(self, open_file: io.BufferedReader) -> None:
        """
        Reads the data from the WBIN file.
        This method should be implemented to parse the data section of the file.
        """
        raise NotImplementedError("This method should be implemented in a subclass")
    
    @abstractmethod
    def _translate_objects(self, open_file: io.BufferedReader) -> None:
        """
        Translates the raw data into structured objects.
        This method should be implemented to convert the raw data into digitizer, settings, and events objects.
        """
        raise NotImplementedError("This method should be implemented in a subclass")
