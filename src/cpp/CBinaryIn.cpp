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
* @file     CBinaryIn.cpp
* @brief    Implement the CBinaryIn class
* @author   Ron Fox
*
*/
#include "CBinaryIn.h"

// The I/O headers in MSVC don't conform to POSIX for POSIX functions _sigh_

#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <iostream>

#ifdef __GNUG__
#include <unistd.h>
#endif

#ifdef _MSVC_LANG
#include <io.h>
#endif

// For the open:

#ifdef __GNUG__
#define O_BINARY 0     // There is no O_BINARY in linux/gnucc.
#endif

#include <stdexcept>
#include <system_error>


/**
 * CBinaryIn
 *   constructor
 *     @param name - filename the data are in.
 */
CBinaryIn::CBinaryIn(const char* filename) : m_filename(filename),
    m_fd(-1)
{
	int mode = O_RDONLY;

    m_fd = open(m_filename.c_str(), O_RDONLY | O_BINARY);
    if (m_fd < 0) {
        std::string msg = "Open failed for: ";
         msg += filename;
        throw std::system_error(errno, std::generic_category(), msg.c_str());
    }
}
/**
 * destructor
 *   - close the file if the open worked
 */
CBinaryIn::~CBinaryIn()
{
    if (m_fd >= 0) {
        close(m_fd);
    }
}

/**
 * readHeader
 *     Read a record header:
 *  @param buffer - references a header struct.
 *  @return bytes read on success.
 *  @retval 0     End file encountered.
 *  @retval <0    Some error condition in errno.
 * 
 */
int
CBinaryIn::readHeader(header& buffer)
{
    auto nBytes = read(m_fd, &buffer, sizeof(header));
    return static_cast<int>(nBytes);    // will fit in an int.
}
/**
 * readDigitizerDescriptor
 *   Read the body of a digitizer descriptor record.
 *
 * @param buffer - references a DigitizerDescriptor struct into which
 *                 the record will be read.
 * @return int  - number of bytes read on success (should be sizeof(DigitizerDescriptor))
 * @retval  0     end of file hit (prematurely).
 * @retval <0     Some error condition in errno.
 */
int
CBinaryIn::readDigitizerDescriptor(DigitizerDescriptor& buffer)
{
    auto nBytes = read(m_fd, &buffer, sizeof(DigitizerDescriptor));
    return static_cast<int>(nBytes);
}
/*
 * readDigitizerSettings
 *    Reads a digitizer settings record. Note that what we do is
 *    - Read the fixed header part of the record.
 *    - Allocate size in the vectors for the DCoffsets and Trigger levels and
 *    - Read those into the .data member of those vectors.
 * @param buffer - references a DigitizersSettings that will get this information.
 * @return int  - number of bytes read on success.
 * @retval  0     end of file hit (prematurely).
 * @retval <0     Some error condition in errno.
 */
int
CBinaryIn::readDigitizerSettings(DigitizerSettings& buffer)
{
    int n = readSettingsFixedHeader(buffer);
    if (n > 0) {
        
        // Reserver storage for the DC offsets and Trigger levels:
        
        buffer.s_DCOffsets.resize(buffer.s_header.s_nChannels);
        buffer.s_TriggerLevels.resize(buffer.s_header.s_nChannels);
        
        // Read in the DC offsets -- if possible:
        
        auto nBytes = read(
            m_fd, buffer.s_DCOffsets.data(),
            buffer.s_header.s_nChannels*sizeof(uint32_t)
        );
        // Exceptional condition handling: Errors or premature EOF:
        
        if (nBytes < 0) return nBytes;
        if (nBytes == 0) {
            return 0;               // Premature EOF.
        }
        n += static_cast<int>(nBytes); // Total up the bytes read.
        // Read in the trigger levels in the same way:
            
		nBytes = read(
			m_fd, buffer.s_TriggerLevels.data(),
			buffer.s_header.s_nChannels * sizeof(uint32_t)
		);
        if (nBytes < 0) return nBytes;
        if (nBytes == 0) return 0;       // Premature EOF.
        
        n += nBytes;                     // Total up the bytes read.
    }
    return n;
}

/**
 * readWaveform
 *   Reads the body of a waveform record.  The logic here is very similar
 *   to that of readDigitizerSettings.
 * @param buffer - reference to a WaveformData struct into which the data
 *               will be read.
 * @return int  - number of bytes read on success.
 * @retval  0     end of file hit (prematurely).
 * @retval <0     Some error condition in errno.
 */
int
CBinaryIn::readWaveform(WaveformData& buffer)
{
    int n = readWaveformFixedHeader(buffer);
    if (n > 0) {
        // Allocate storage for the trace:
        
        buffer.s_trace.resize(buffer.s_header.s_nSamples);

        auto nBytes = read(
            m_fd, buffer.s_trace.data(),
            buffer.s_header.s_nSamples*sizeof(uint16_t)
        );
        if (nBytes <=0)  return nBytes;
        n += static_cast<int>(nBytes);
    }
    return n;
}
///////////////////////////////////////////////////////////////////////////////
// Utility methods

/**
 * readSettingsFixedHeader
 *     Reads the fixed header par tof a DigitizerSettings record.
 * @param buffer - reference to a DigitizerSettings struct.
 * @return int   - Number of bytes read. Should be sizeof(DigitizerSettingsFixedHeader)
 * @retval  0     end of file hit (prematurely 0-- only readHeader should
 *                get an EOF in a properly formatted file.
 * @retval <0     Some error condition in errno.
*/
int
CBinaryIn::readSettingsFixedHeader(DigitizerSettings& buffer)
{
    auto n = read(
        m_fd, &(buffer.s_header), sizeof(DigitizerSettingsFixedHeader)
    );
    return static_cast<int>(n);
}
/**
 * readWaveformFixedHeader
 *    Read the fixed header part of a waveform record.
 * @param buffer - reference to a WaveformData struct.
 * @return int   - Number of bytes read. Should be sizeof(DigitizerSettingsFixedHeader)
 * @retval  0     end of file hit (prematurely 0-- only readHeader should
 *                get an EOF in a properly formatted file.
 * @retval <0     Some error condition in errno.
*/
int
CBinaryIn::readWaveformFixedHeader(WaveformData& buffer)
{
    auto n = read(
        m_fd, &(buffer.s_header), sizeof(WaveformFixedHeader)
    );
#ifdef DEBUG_OUTPUT
    std::cerr << "----------------- read waveform header  ----\n";
    std::cerr << "Read " << sizeof(WaveformFixedHeader) << "bytes\n";
    std::cerr << "triggerTag: " << buffer.s_header.s_triggerTag << std::endl;
    std::cerr << "Tod Stamp : " << buffer.s_header.s_todStamp << std::endl;
    std::cerr << "shift     : " << buffer.s_header.s_shift    << std::endl;
    std::cerr << "channel   : " << buffer.s_header.s_channel  << std::endl;
    std::cerr << "no. pts   : " << buffer.s_header.s_nSamples << std::endl;
#endif
    return static_cast<int>(n);
}
