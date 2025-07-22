
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include "CBinaryIn.h"


namespace py = pybind11;

PYBIND11_MODULE(caen_cpp, m) {
    py::class_<CBinaryIn>(m, "CBinaryIn")
        .def(py::init<const char*>())
        .def("readHeader", &CBinaryIn::readHeader)
        .def("readDigitizerDescriptor", &CBinaryIn::readDigitizerDescriptor)
        .def("readDigitizerSettings", &CBinaryIn::readDigitizerSettings)
        .def("readWaveform", &CBinaryIn::readWaveform)
        .def_readonly_static("tp_DigitizerDescription", &CBinaryIn::tp_DigitizerDescription)
        .def_readonly_static("tp_DigitizerSettings", &CBinaryIn::tp_DigitizerSettings)
        .def_readonly_static("tp_TraceData", &CBinaryIn::tp_TraceData)
        .def_readonly_static("cap_hasGroups", &CBinaryIn::cap_hasGroups)
        .def_readonly_static("cap_canZsuppress", &CBinaryIn::cap_canZsuppress)
        .def_readonly_static("cap_canInspect", &CBinaryIn::cap_canInspect)
        .def_readonly_static("cap_DualEdgeClock", &CBinaryIn::cap_DualEdgeClock)
        .def_readonly_static("trg_TriggerOnExtTrg", &CBinaryIn::trg_TriggerOnExtTrg)
        .def_readonly_static("trg_TriggerOnBoth", &CBinaryIn::trg_TriggerOnBoth)
        .def_readonly_static("trg_ExtTrigDisabled", &CBinaryIn::trg_ExtTrigDisabled)
        .def_readonly_static("trg_Rising", &CBinaryIn::trg_Rising);


    py::class_<CBinaryIn::header>(m, "Header")
        .def_readwrite("s_size", &CBinaryIn::header::s_size)
        .def_readwrite("s_type", &CBinaryIn::header::s_type)
        .def_static("size", [](){ return sizeof(CBinaryIn::header); });


    py::class_<CBinaryIn::DigitizerDescriptor>(m, "DigitizerDescriptor")
        .def_readwrite("s_id", &CBinaryIn::DigitizerDescriptor::s_id)
        .def_readwrite("s_familyCode", &CBinaryIn::DigitizerDescriptor::s_familyCode)
        .def_readonly("s_ROCVersion", &CBinaryIn::DigitizerDescriptor::s_ROCVersion)
        .def_readonly("s_AMCVersion", &CBinaryIn::DigitizerDescriptor::s_AMCVersion)
        .def_readwrite("s_SerialNumber", &CBinaryIn::DigitizerDescriptor::s_SerialNumber)
        .def_readwrite("s_boardVersion", &CBinaryIn::DigitizerDescriptor::s_boardVersion)
        .def_readwrite("s_nChans", &CBinaryIn::DigitizerDescriptor::s_nChans)
        .def_readwrite("s_bits", &CBinaryIn::DigitizerDescriptor::s_bits)
        .def_readwrite("s_Hz", &CBinaryIn::DigitizerDescriptor::s_Hz)
        .def_readwrite("s_maxSamples", &CBinaryIn::DigitizerDescriptor::s_maxSamples)
        .def_readwrite("s_capflags", &CBinaryIn::DigitizerDescriptor::s_capflags)
        .def_readwrite("s_vlow", &CBinaryIn::DigitizerDescriptor::s_vlow)
        .def_readwrite("s_vhigh", &CBinaryIn::DigitizerDescriptor::s_vhigh)
        .def_static("size", [](){ return sizeof(CBinaryIn::DigitizerDescriptor); });


    py::class_<CBinaryIn::DigitizerSettings>(m, "DigitizerSettings")
        .def_readwrite("s_header", &CBinaryIn::DigitizerSettings::s_header)
        .def_readwrite("s_DCOffsets", &CBinaryIn::DigitizerSettings::s_DCOffsets)
        .def_readwrite("s_TriggerLevels", &CBinaryIn::DigitizerSettings::s_TriggerLevels)
        .def_static("size", [](){ return sizeof(CBinaryIn::DigitizerSettings); });


    py::class_<CBinaryIn::DigitizerSettingsFixedHeader>(m, "DigitizerSettingsFixedHeader")
        .def_readwrite("s_sid", &CBinaryIn::DigitizerSettingsFixedHeader::s_sid)
        .def_readwrite("s_did", &CBinaryIn::DigitizerSettingsFixedHeader::s_did)
        .def_readwrite("s_TriggerMask", &CBinaryIn::DigitizerSettingsFixedHeader::s_TriggerMask)
        .def_readwrite("s_triggerCode", &CBinaryIn::DigitizerSettingsFixedHeader::s_triggerCode)
        .def_readwrite("s_windowSize", &CBinaryIn::DigitizerSettingsFixedHeader::s_windowSize)
        .def_readwrite("s_postTrigger", &CBinaryIn::DigitizerSettingsFixedHeader::s_postTrigger)
        .def_readwrite("s_channelMask", &CBinaryIn::DigitizerSettingsFixedHeader::s_channelMask)
        .def_readwrite("s_nChannels", &CBinaryIn::DigitizerSettingsFixedHeader::s_nChannels);


    py::class_<CBinaryIn::WaveformData>(m, "WaveformData")
        .def_readwrite("s_header", &CBinaryIn::WaveformData::s_header)
        .def_readwrite("s_trace", &CBinaryIn::WaveformData::s_trace)
        .def_static("size", [](){ return sizeof(CBinaryIn::WaveformData); });


    py::class_<CBinaryIn::WaveformFixedHeader>(m, "WaveformFixedHeader")
        .def_readwrite("s_eventId", &CBinaryIn::WaveformFixedHeader::s_eventId)
        .def_readwrite("s_did", &CBinaryIn::WaveformFixedHeader::s_did)
        .def_readwrite("s_sid", &CBinaryIn::WaveformFixedHeader::s_sid)
        .def_readwrite("s_triggerTag", &CBinaryIn::WaveformFixedHeader::s_triggerTag)
        .def_readwrite("s_todStamp", &CBinaryIn::WaveformFixedHeader::s_todStamp)
        .def_readwrite("s_shift", &CBinaryIn::WaveformFixedHeader::s_shift)
        .def_readwrite("s_channel", &CBinaryIn::WaveformFixedHeader::s_channel)
        .def_readwrite("s_nSamples", &CBinaryIn::WaveformFixedHeader::s_nSamples);
}