/*
*-------------------------------------------------------------
 
 CAEN SpA 
 Via Vetraia, 11 - 55049 - Viareggio ITALY
 +390594388398 - www.caen.it

------------------------------------------------------------

**************************************************************************
* @note TERMS OF USE:
* This program is free software; you can redistribute it and/or modify it under
* the terms of the GNU General Public License as published by the Free Software
* Foundation. This program is distributed in the hope that it will be useful, 
* but WITHOUT ANY WARRANTY; without even the implied warranty of 
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. The user relies on the 
* software, documentation and results solely at his own risk.
*
* @file     CBinaryIn.h
* @brief    C++ class to do binary input.
* @author   Ron Fox
*
*/
#ifndef CBINARYIN_H
#define CBINARYIN_H
#define _CRT_NONSTDC_NO_WARNINGS    // To deal with Microsoft Posix idiocies.
#include <vector>
#include <string>
#include <stdint.h>


/**
 * @class CBinaryIn
 *     The form of the binary output file is such that it's just easier to
 *     read it in C++ as binary scan etc. just doesn't do as well as
 *     read(1) with variable sizes.  This class is then encapsulated via
 *     methods in CDigitizer.h s that it is accessible in Tcl.
 *  
 */
class CBinaryIn
{
    // public data structures.
public:
    // These are values for the s_type field of header
    static const uint32_t tp_DigitizerDescription = 1;
    static const uint32_t tp_DigitizerSettings    = 2;
    static const uint32_t tp_TraceData            = 3;
    
    // Record header:

#pragma pack(push, 1)
    typedef struct _header {
        uint32_t  s_size;                // Total record size.
        uint32_t  s_type;                // record types.
    } header, *pHeader;
#pragma pack(pop)
    
    // Bit s in s_capflags below
    
    static const uint32_t cap_hasGroups    = 1;
    static const uint32_t cap_canZsuppress = 2;
    static const uint32_t cap_canInspect   = 4;
    static const uint32_t cap_DualEdgeClock= 8;
    
    // Digitizer descriptor body:
    
    
#pragma pack(push, 1)

    typedef struct _DigitizerDescriptor {
        uint32_t    s_id;              // Unique id within the file.
        uint32_t    s_familyCode;      // Digitizer Family  code.
        char        s_ROCVersion[20];  // Readout controller firmware version.
        char        s_AMCVersion[20];  // AMC card firmware versions.
        uint32_t    s_SerialNumber;    // Card serial no.
        uint32_t    s_boardVersion;    // Board version.
        uint32_t    s_nChans;          // Number of channels.
        uint32_t    s_bits;            // Number of bits of resolution.
        uint64_t    s_Hz;              // digitizer frequency in Hz.
        uint32_t    s_maxSamples;      // Longest trace.
		uint32_t    s_capflags;         // capability flags.
		int32_t     s_vlow;             // Voltage low range.
		int32_t     s_vhigh;            // voltage high range.
    } DigitizerDescriptor, * pDigitizerDescriptor;
#pragma pack(pop)


    // Trigger code:
    
    static const uint32_t trg_ExternalOutput  = 0;  // output reflecting trigger.
    static const uint32_t trg_TriggerOnExtTrg = 1;  // Only ext trig.
    static const uint32_t trg_TriggerOnBoth   = 2;  // Ext and internal trig.
    static const uint32_t trg_ExtTrigDisabled = 3;  // Internal trigger only.
    static const uint32_t trg_Rising          = 4;  // Rising/falling edge bit.
    
    // Settings body:
    
#pragma pack(push, 1)

    typedef struct _DigitizerSettingsFixedHeader {
        uint32_t  s_sid;                // Unique settings id within the file.
        uint32_t  s_did;                // ID of digitizer this belongs to.
        uint32_t  s_TriggerMask;        // Trigger mask
        uint32_t  s_triggerCode;        // Triggering code.
        uint32_t  s_windowSize;        // Number of samples.
        uint32_t  s_postTrigger;        // % post-trigger * 100.
        uint32_t  s_channelMask;        // enabled channels.
        uint32_t  s_nChannels;          // Number of channels offset/level data.
    } DigitizerSettingsFixedHeader, *pDigitizerSettingsFixedHeader;
#pragma pack(pop)


#pragma pack(push, 1)

    typedef struct  _DigitizerSettings
    {
        DigitizerSettingsFixedHeader s_header; // Fixed header.
        std::vector<uint32_t> s_DCOffsets; // DC Offset values.
        std::vector<uint32_t> s_TriggerLevels; // Trigger level values.
    } DigitizerSettings, *pDigitizerSettings;
#pragma pack(pop)


    // Trace record:

#pragma pack(push, 1)
    typedef struct _WaveformFixedHeader {
        uint32_t   s_eventId;           // unique event number.
        uint32_t   s_did;               // Digitizer id.
        uint32_t   s_sid;               // Settings id.
        uint32_t   s_triggerTag;        // Trigger time tag.
        uint64_t   s_todStamp;          // Tcl [clock seconds] at trigger.
        int32_t    s_shift;             // Trigger jitter compensation shift
        uint32_t   s_channel;           // Channel number for the trace.
        uint32_t   s_nSamples;          // # of samples.
    } WaveformFixedHeader, *pWaveformFixedHeader;
#pragma pack(pop)

#pragma pack(push, 1)

    typedef struct _WaveformData {
        WaveformFixedHeader   s_header;
        std::vector<uint16_t> s_trace;  // The samples.
    } WaveformData, *pWaveformData;
#pragma pack(pop)


    // Class private data:
    
private:
   std::string m_filename;
   int         m_fd;
public:
    CBinaryIn(const char* filename);
    ~CBinaryIn();

    int readHeader(header& buffer);
    int readDigitizerDescriptor(DigitizerDescriptor& buffer);
    int readDigitizerSettings(DigitizerSettings& buffer);
    int readWaveform(WaveformData& buffer);
    
private:
    int readSettingsFixedHeader(DigitizerSettings& buffer);
    int readWaveformFixedHeader(WaveformData& buffer);
};

    

#endif