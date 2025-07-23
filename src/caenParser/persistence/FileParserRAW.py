from caen_cpp import CBinaryIn, Header, DigitizerDescriptor, DigitizerSettings, DigitizerSettingsFixedHeader, WaveformData, WaveformFixedHeader 
from .FileParser import FileParser
from .dtos import DigitizerDTO, SettingsDTO, EventDTO, TriggerDTO
from enum import Enum, auto
from datetime import datetime

class RecordType(Enum):
    DIGITIZER_DESCRIPTION = CBinaryIn.tp_DigitizerDescription
    DIGITIZER_SETTINGS = CBinaryIn.tp_DigitizerSettings
    WAVEFORM_DATA = CBinaryIn.tp_TraceData
    HEADER = auto()



class FileParserRAW(FileParser):
    def __init__(self):
        super().__init__()
        self._fileObj: CBinaryIn = None

        self._tmpEvent: dict[int, EventDTO] = {}

    def open(self, file_path: str):
        try:
            self._fileObj = CBinaryIn(file_path)
        except Exception as e:
            raise ValueError(f"Error opening RAW file: {e}")
            
    def parse(self) -> None:

        header = Header()
        controlInt = self._fileObj.readHeader(header)
        self._sanitize_control_int(controlInt, RecordType.HEADER)

        while (controlInt > 0):
            match header.s_type:
                case RecordType.DIGITIZER_DESCRIPTION.value:
                    desc = DigitizerDescriptor()
                    controlInt = self._fileObj.readDigitizerDescriptor(desc)
                    self._digitizers.append(self._convert_digitizer_descriptor_to_dto(desc))
                case RecordType.DIGITIZER_SETTINGS.value:
                    settings = DigitizerSettings()
                    controlInt = self._fileObj.readDigitizerSettings(settings)
                    self._settings.append(self._convert_digitizer_settings_to_dto(settings))
                case RecordType.WAVEFORM_DATA.value:
                    waveform = WaveformData()
                    controlInt = self._fileObj.readWaveformData(waveform)
                    self._convert_waveform_data_to_tmp_dto(waveform)
                case _:
                    raise ValueError(f"Unknown record type: {header.s_type}")
            
            # Sanitize controlInt for the next iteration
            self._sanitize_control_int(controlInt, RecordType(header.s_type))


            controlInt = self._fileObj.readHeader(header)
            if controlInt != 0:
                # Sanitize controlInt for the next header read
                self._sanitize_control_int(controlInt, RecordType.HEADER)

        #end of file reached
        if controlInt != 0:
            raise ValueError("File parsing did not end correctly")
        print("File parsing completed successfully.")
        self._events = list(self._tmpEvent.values())
        self._tmpEvent.clear()
        self._fileObj.close()


    def _convert_digitizer_descriptor_to_dto(self, desc: DigitizerDescriptor) -> DigitizerDTO:
        return DigitizerDTO(
            id=str(desc.s_id),
            family= "xx" + str(desc.s_family),
            version= str(desc.s_ROCVersion) + "." + str(desc.s_AMCVersion),
            serial=str(desc.s_SerialNumber),
            channels=desc.s_nChans,
            resolution=float(desc.s_bits),
            frequency=float(desc.s_Hz),
            max_samples=desc.s_maxSamples,
            channel_groups= int((desc.s_capflags & CBinaryIn.cap_hasGroups) > 0),
            zero_suppression=bool(desc.s_capflags & CBinaryIn.cap_canZsuppress),
            inspection=bool(desc.s_capflags & CBinaryIn.cap_canInspect),
            dual_edge=bool(desc.s_capflags & CBinaryIn.cap_DualEdgeClock),
            voltage_range=(desc.s_vlow/1000, desc.s_vhigh/10000), # Descriptor uses mV, convert to V
            windows= [-1] # Placeholder for windows, as this is not provided in the descriptor
        )

    def _convert_digitizer_settings_to_dto(self, settings: DigitizerSettings) -> SettingsDTO:
        s_header = settings.s_header
        return SettingsDTO(
            id = s_header.s_id,
            digitizer_id = str(s_header.s_did),
            dc_offsets = {i: int(settings.s_DCOffsets[i]) for i in range(s_header.s_nChannels)},
            trigger = self._convert_setting_descriptor_to_trigger_dto(settings),
            window = s_header.s_windowSize,
            post_trigger= s_header.s_postTrigger,
            channels_mask = s_header.s_channelMask
        )
    
    def _convert_setting_descriptor_to_trigger_dto(self, settings: DigitizerSettings) -> TriggerDTO:
        s_header = settings.s_header
        return TriggerDTO(
            direction = "rising" if bool(s_header.s_triggerCode & CBinaryIn.trg_Rising) else "falling",
            bitmask = s_header.s_TriggerMask,
            external = "disabled" if bool(s_header.s_triggerCode == CBinaryIn.trg_ExtTrigDisabled) else "acq", #inconsistency with XML, XML has one mode more.
            thresholds= {i: settings.s_TriggerLevels[i] for i in range(s_header.s_nChannels)},
        )


    def _convert_waveform_data_to_tmp_dto(self, waveform: WaveformData) -> None:
        s_header = waveform.s_header
        if not s_header.s_eventId in self._tmpEvent.keys():
            self._tmpEvent[s_header.s_eventId] = EventDTO(
                id = s_header.s_eventId,
                settings_id = s_header.s_sid,
                digitizer_id = str(s_header.s_did),
                time_stamp = s_header.s_triggerTag,
                clock_time= datetime.fromtimestamp(s_header.s_todStamp),
                trigger_shift= s_header.s_shift,
                trace = {s_header.s_channel: waveform.s_trace.copy()}
            )
        else:
            self._tmpEvent[s_header.s_eventId].trace[s_header.s_channel] = waveform.s_trace.copy()
        

    def _sanitize_control_int(self, controlInt: int, record_type: RecordType = RecordType.HEADER):
        match record_type:
            case RecordType.DIGITIZER_DESCRIPTION:
                if controlInt != DigitizerDescriptor.size():
                    raise ValueError(f"Digitizer description size mismatch: expected {DigitizerDescriptor.size()}, got {controlInt}")
            case RecordType.DIGITIZER_SETTINGS:
                if controlInt < DigitizerSettings.size():
                    raise ValueError(f"Digitizer settings size mismatch: expected {DigitizerSettings.size()}, got {controlInt}")
            case RecordType.WAVEFORM_DATA:
                if controlInt < WaveformData.size():
                    raise ValueError(f"Waveform data size mismatch: expected {WaveformData.size()}, got {controlInt}")
            case RecordType.HEADER:
                if controlInt != Header.size():
                    raise ValueError(f"Header size mismatch: expected {Header.size()}, got {controlInt}")