import struct
from enum import Enum, auto
import tkinter as tk
from tkinter import filedialog

data_size_map = {
    'float': 4,
    'uint': 2,
}

data_type_map = {
    'float': 'f',
    'uint': 'H',
}


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
    return file_path




class WaveDump2BinParser:



    def __init__(self, filename, multi_board=False, one_file_each_channel=False, data_type: str = 'float'):
        self._filename = filename
        self.multi_board = multi_board
        self.one_file_each_channel = one_file_each_channel
        self.data_type = data_type

        self.file_obj = open(filename, 'rb')  # Open file in binary read mode
        
        # Get file size
        self.file_obj.seek(0, 2)  # Seek to end
        self.file_size = self.file_obj.tell()
        self.file_obj.seek(0)  # Seek back to beginning

    def __iter__(self):
        """Make the class iterable"""
        return self

    def __next__(self):
        """Iterator protocol - returns next event or raises StopIteration"""
        if self.file_obj.tell() >= self.file_size:
            raise StopIteration
        
        try:
            if self.multi_board:
                event = self._parse_multi_board()
            elif self.one_file_each_channel:
                event = self._parse_one_file_each_channel()
            else:
                event = self._parse_normal_file()
            return event
        except ValueError as e:
            print(f"Error parsing event: {e}")
            raise StopIteration

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes file"""
        if hasattr(self, 'file_obj') and self.file_obj:
            self.file_obj.close()

    def parse_all(self):
        """Parse all events and return as list (for backward compatibility)"""
        events = []
        for event in self:
            events.append(event)
        return events

    def _parse_normal_file(self):
        header_fmt = '<I Q I Q i'  # Event number, Timestamp, Samples, Sampling Period, Channels
        header_size = struct.calcsize(header_fmt)
        header_bytes = self._safe_read(self.file_obj, header_size)
        if header_bytes is None:
            raise ValueError("File too small for header")
        
        event_num, timestamp, samples, samp_period, channels = struct.unpack(header_fmt, header_bytes)
        self.file_obj.read(2)  # Skip padding bytes
        waveform = []
        for _ in range(channels):   
            waveform.append(self._get_waveform(self.file_obj, samples, self.data_type))
        return {
            'event_num': event_num,
            'timestamp': timestamp,
            'samples': samples,
            'sampling_period_ns': samp_period,
            'channels': channels,
            'waveform': waveform
        }

    def _parse_multi_board(self):
        header_fmt = '<I Q I Q i'  # Global Event ID, Timestamp, Samples, Sampling Period, Channels
        header_size = struct.calcsize(header_fmt)
        header_bytes = self._safe_read(self.file_obj, header_size)
        if header_bytes is None:
            raise ValueError("File too small for multi-board header")
        
        event_id, timestamp, samples, samp_period, channels = struct.unpack(header_fmt, header_bytes)
        self.file_obj.read(2)  # Skip padding bytes
        waveform = []
        for _ in range(channels):
            waveform.append(self._get_waveform(self.file_obj, samples, self.data_type))
        return {
            'global_event_id': event_id,
            'timestamp': timestamp,
            'samples': samples,
            'sampling_period_ns': samp_period,
            'channels': channels,
            'waveform': waveform
        }
    
    def _parse_one_file_each_channel(self):
        header_fmt = '<I Q I Q'
        header_size = struct.calcsize(header_fmt)
        header_bytes = self._safe_read(self.file_obj, header_size)
        if header_bytes is None:
            raise ValueError("File too small for one-file-each-channel header")
        
        event_num, timestamp, samples, samp_period = struct.unpack(header_fmt, header_bytes)
        self.file_obj.read(2)  # Skip padding bytes
        waveform = []
        waveform.append(self._get_waveform(self.file_obj, samples, self.data_type))
        return {
            'event_num': event_num,
            'timestamp': timestamp,
            'samples': samples,
            'sampling_period_ns': samp_period,
            'channels': 1,
            'waveform': waveform
        }

    @staticmethod
    def _safe_read(f, num_bytes):
        """Safely read bytes from file, return None if not enough data available"""
        data = f.read(num_bytes)
        if len(data) < num_bytes:
            return None
        return data

    @staticmethod
    def _get_waveform(f, samples, data_type):
        bytes_needed = samples * data_size_map[data_type]
        wave_bytes = WaveDump2BinParser._safe_read(f, bytes_needed)
        if wave_bytes is None:
            raise ValueError("File too small for waveform data")
        
        wave_fmt = f'<{samples}{data_type_map[data_type]}'
        return struct.unpack(wave_fmt, wave_bytes)
    
    @property
    def filename(self):
        """Return the filename"""
        return self._filename




        