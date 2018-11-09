#!/usr/bin/env python3
"""
    ctypes Python to C++ NunaceVOCEnt components API - (a partial example implementation)
"""
import os
import time
import logging
from ctypes import *
from datetime import datetime
from lxml import etree, objectify

TTS_CURRENT_VERSION = 1360

logger = logging.getLogger('tts_engine')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('logs/tts_engine.log')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

def print_status(c, func=""):
    CODES = {
        "0": {"state": "SUCCESS", "desc": ""},
        "1": {"state": "TTS_ERROR", "desc": "Generic error"},
        "2": {"state": "TTS_E_WRONG_STATE", "desc": "Generic error"},
        "3": {"state": "TTS_E_SYSTEMERROR", "desc": "Generic error"},
        "4": {"state": "TTS_E_INVALIDINST", "desc": "Generic error"},
        "5": {"state": "TTS_E_BADCOMMAND", "desc": "Generic error"},
        "6": {"state": "TTS_E_PARAMERROR", "desc": "Generic error"},
        "7": {"state": "TTS_E_OUTOFMEMORY", "desc": "Generic error"},
        "8": {"state": "TTS_E_INVALIDPARM", "desc": "Generic error"},
        "9": {"state": "TTS_E_MISSING_SL", "desc": "Generic error"},
        "10": {"state": "TTS_E_MISSING_FUNC", "desc": "Generic error"},
        "11": {"state": "TTS_E_BAD_LANG", "desc": "Generic error"},
        "12": {"state": "TTS_E_BAD_TYPE", "desc": "Generic error"},
        "13": {"state": "TTS_E_BAD_OUTPUT", "desc": "Generic error"},
        "14": {"state": "TTS_E_BAD_FREQ", "desc": "Generic error"},
        "15": {"state": "TTS_E_BAD_VOICE", "desc": "Generic error"},
        "16": {"state": "TTS_E_NO_MORE_MEMBERS", "desc": "Generic error"},
        "17": {"state": "TTS_E_NO_KEY", "desc": "Generic error"},
        "18": {"state": "TTS_E_KEY_EXISTS", "desc": "Generic error"},
        "19": {"state": "TTS_E_BAD_HANDLE", "desc": "Generic error"},
        "20": {"state": "TTS_E_TRANS_EMAIL", "desc": "Generic error"},
        "21": {"state": "TTS_E_NULL_STRING", "desc": "Generic error"},
        "22": {"state": "TTS_E_INTERNAL_ERROR", "desc": "Generic error"},
        "23": {"state": "TTS_E_NO_MATCH_FOUND", "desc": "Generic error"},
        "24": {"state": "TTS_E_NULL_POINTER", "desc": "Generic error"},
        "25": {"state": "TTS_E_BUF_TOO_SMALL", "desc": "Generic error"},
        "26": {"state": "TTS_W_UDCT_ALREADYLOADED", "desc": "User dictionary error"},
        "27": {"state": "TTS_E_UDCT_INVALIDHNDL", "desc": "User dictionary error"},
        "28": {"state": "TTS_E_UDCT_NOENTRY", "desc": "User dictionary error"},
        "29": {"state": "TTS_E_UDCT_MEMALLOC", "desc": "User dictionary error"},
        "30": {"state": "TTS_E_UDCT_DATAFAILURE", "desc": "User dictionary error"},
        "31": {"state": "TTS_E_UDCT_FILEIO", "desc": "User dictionary error"},
        "32": {"state": "TTS_E_UDCT_INVALIDFILE", "desc": "User dictionary error"},
        "33": {"state": "TTS_E_UDCT_MAXENTRIES", "desc": "User dictionary error"},
        "34": {"state": "TTS_E_UDCT_MAXSOURCESPACE", "desc": "User dictionary error"},
        "35": {"state": "TTS_E_UDCT_MAXDESTSPACE", "desc": "User dictionary error"},
        "36": {"state": "TTS_E_UDCT_DUPLSOURCEWORD", "desc": "User dictionary error"},
        "37": {"state": "TTS_E_UDCT_INVALIDENGHNDL", "desc": "User dictionary error"},
        "38": {"state": "TTS_E_UDCT_MAXENG", "desc": "User dictionary error"},
        "39": {"state": "TTS_E_UDCT_FULLENG", "desc": "User dictionary error"},
        "40": {"state": "TTS_E_UDCT_ALREADYINENG", "desc": "User dictionary error"},
        "41": {"state": "TTS_E_UDCT_OTHERUSER", "desc": "User dictionary error"},
        "42": {"state": "TTS_E_UDCT_INVALIDOPER", "desc": "User dictionary error"},
        "43": {"state": "TTS_E_UDCT_NOTLOADED", "desc": "User dictionary error - Can't disable dictionary, not loaded"},
        "44": {"state": "TTS_E_UDCT_STILLINUSE", "desc": "User dictionary error - Can't unload dictionary, still in use"},
        "45": {"state": "TTS_E_UDCT_NOT_LOCAL",
               "desc": "User dictionary error - Using a server dictionary for a local device or vice-versa"},
        "46": {"state": "TTS_E_UDCT_COULDNOTOPENFILE", "desc": "User dictionary error"},
        "47": {"state": "TTS_E_UDCT_FILEREADERROR", "desc": "User dictionary error"},
        "48": {"state": "TTS_E_UDCT_FILEWRITEERROR", "desc": "User dictionary error"},
        "49": {"state": "TTS_E_UDCT_WRONGTXTDCTFORMAT", "desc": "User dictionary error"},
        "50": {"state": "TTS_E_UDCT_LANGUAGECONFLICT", "desc": "User dictionary error"},
        "51": {"state": "TTS_E_UDCT_INVALIDENTRYDATA", "desc": "User dictionary error"},
        "52": {"state": "TTS_E_UDCT_READONLY", "desc": "User dictionary error"},
        "53": {"state": "TTS_E_UDCT_ACTIONNOTALLOWED", "desc": "User dictionary error"},
        "54": {"state": "TTS_E_UDCT_BUSY", "desc": "User dictionary error"},
        "55": {"state": "TTS_E_UDCT_PRIORITYINUSE", "desc": "User dictionary error"},
        "56": {"state": "TTS_E_UDCT_ALREADYENABLED", "desc": "User dictionary error"},
        "57": {"state": "TTS_E_MODULE_NOT_FOUND", "desc": "Extended generic error"},
        "58": {"state": "TTS_E_CONVERSION_FAILED", "desc": "Extended generic error"},
        "59": {"state": "TTS_E_OUT_OF_RANGE", "desc": "Extended generic error"},
        "60": {"state": "TTS_E_END_OF_INPUT", "desc": "Extended generic error"},
        "61": {"state": "TTS_E_NOT_COMPATIBLE", "desc": "Extended generic error"},
        "62": {"state": "TTS_E_INVALID_POINTER", "desc": "Extended generic error"},
        "63": {"state": "TTS_E_FEAT_EXTRACT", "desc": "Extended generic error"},
        "64": {"state": "TTS_E_MAX_CHANNELS", "desc": "Extended generic error"},
        "65": {"state": "TTS_E_ALREADY_DEFINED", "desc": "Extended generic error"},
        "66": {"state": "TTS_E_NOT_FOUND", "desc": "Extended generic error"},
        "67": {"state": "TTS_E_NO_INPUT_TEXT", "desc": "Extended generic error"},
        "80": {"state": "TTS_E_NETWORK_PROBLEM ", "desc": "Client/Server error"},
        "81": {"state": "TTS_E_NETWORK_TIMEOUT", "desc": "Client/Server error"},
        "82": {"state": "TTS_E_NETWORK_RETRANSMIT", "desc": "Client/Server error"},
        "83": {"state": "TTS_E_NETWORK_FUNCTION_ERROR", "desc": "Client/Server error"},
        "84": {"state": "TTS_E_QUEUE_FULL", "desc": "Client/Server error"},
        "85": {"state": "TTS_E_QUEUE_EMPTY", "desc": "Client/Server error"},
        "86": {"state": "TTS_E_ENGINE_NOT_FOUND", "desc": "Client/Server error"},
        "87": {"state": "TTS_E_ENGINE_ALREADY_INITIALIZED", "desc": "Client/Server error"},
        "88": {"state": "TTS_E_ENGINE_ALREADY_UNINITIALIZED", "desc": "Client/Server error"},
        "89": {"state": "TTS_E_DICTIONARY_ALREADY_UNLOADING", "desc": "Client/Server error"},
        "90": {"state": "TTS_E_INSTANCE_BUSY", "desc": "Client/Server error"},
        "91": {"state": "TTS_E_NETWORK_INTERNAL_ERROR", "desc": "Client/Server error"},
        "100": {"state": "TTS_E_NOTINITIALIZED", "desc": "Client/Server error"},
        "101": {"state": "TTS_E_NETWORK_CONNECTIONREFUSED", "desc": "Client/Server error"},
        "102": {"state": "TTS_E_NETWORK_OPENPORTFAILED", "desc": "Client/Server error"},
        "103": {"state": "TTS_E_NETWORK_SENDFAILED", "desc": "Client/Server error"},
        "104": {"state": "TTS_E_NETWORK_CONNECTIONCLOSED", "desc": "Client/Server error"},
        "105": {"state": "TTS_E_ENGINE_OVERLOAD", "desc": "Client/Server error"},
        "106": {"state": "TTS_E_UNKNOWN", "desc": "Unexpected error"},
        "120": {"state": "TTS_E_LIC_NO_LICENSE", "desc": "Licensing error"},
        "121": {"state": "TTS_E_LIC_LICENSE_ALLOCATED", "desc": "Licensing error"},
        "122": {"state": "TTS_E_LIC_UNSUPPORTED", "desc": "Licensing error"},
        "123": {"state": "TTS_E_LIC_LICENSE_FREED", "desc": "Licensing error"},
        "124": {"state": "TTS_E_LIC_SYSTEM_ERROR", "desc": "Licensing error"},
        "130": {"state": "TTS_W_WARNING ", "desc": "Non-fatal error or warnings"},
        "131": {"state": "TTS_W_ENDOFINPUT", "desc": "Non-fatal error or warnings"},
        "150": {"state": "TTS_E_INET_FATAL", "desc": "Internet fetch error"},
        "151": {"state": "TTS_E_INET_INPUTOUTPUT", "desc": "Internet fetch error"},
        "152": {"state": "TTS_E_INET_PLATFORM", "desc": "Internet fetch error"},
        "153": {"state": "TTS_E_INET_INVALID_PROP_NAME", "desc": "Internet fetch error"},
        "154": {"state": "TTS_E_INET_INVALID_PROP_VALUE", "desc": "Internet fetch error"},
        "155": {"state": "TTS_E_INET_NON_FATAL", "desc": "Internet fetch error"},
        "156": {"state": "TTS_E_INET_WOULD_BLOCK", "desc": "Internet fetch error"},
        "157": {"state": "TTS_E_INET_EXCEED_MAXSIZE", "desc": "Internet fetch error"},
        "158": {"state": "TTS_E_INET_NOT_ENTRY_LOCKED", "desc": "Internet fetch error"},
        "159": {"state": "TTS_E_INET_NOT_ENTRY_CREATED", "desc": "Internet fetch error"},
        "160": {"state": "TTS_E_INET_UNSUPPORTED", "desc": "Internet fetch error"},
        "161": {"state": "TTS_E_INET_UNMAPPED", "desc": "Internet fetch error"},
        "162": {"state": "TTS_E_INET_FETCH_TIMEOUT", "desc": "Internet fetch error"},
        "163": {"state": "TTS_E_INET_FETCH_ERROR", "desc": "Internet fetch error"},
        "164": {"state": "TTS_E_INET_NOT_MODIFIED", "desc": "Internet fetch error"},
        "180": {"state": "TTS_E_SSML_PARSE_ERROR", "desc": "Internet fetch error"}
    }
    if str(c) in CODES:
        # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f -'), func, "(%s)" % str(c), CODES[str(c)]['state'],
        #       CODES[str(c)]['desc'])
        logger.info(" ".join([func + " (%s)" % str(c), CODES[str(c)]['state'], CODES[str(c)]['desc']]))
    else:
        # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f -'), func, "(%s)" % str(c), 'UNKNOWN', 'UNKNOWN')
        logger.info(" ".join([func + " (%s)" % str(c), 'UNKNOWN', 'UNKNOWN']))
    return c


TTS_PARAM_APPLICATION_NAME = 'application_name'
TTS_PARAM_AUDIO_FETCH_HINT = 'audio_fetch_hint'
TTS_PARAM_CACHE_TIMEOUT_OPEN = 'cache_timeout_open'
TTS_PARAM_COMPANY_NAME = 'company_name'
TTS_PARAM_ESCAPE_SEQUENCE = 'escape_sequence'
TTS_PARAM_FETCH_HINT = 'fetch_hint'
TTS_PARAM_FREQUENCY = 'frequency'
TTS_PARAM_INET_ACCEPT_COOKIES = 'inet_accept_cookies'
TTS_PARAM_INET_CACHE_CONTROL_MAX_AGE = 'inet_cache_control_max_age'
TTS_PARAM_INET_CACHE_CONTROL_MAX_STALE = 'inet_cache_control_max_stale'
TTS_PARAM_INET_CACHE_CONTROL_MIN_FRESH = 'inet_cache_control_min_fresh'
TTS_PARAM_INET_TIMEOUT_DOWNLOAD = 'inet_timeout_download'
TTS_PARAM_INET_TIMEOUT_IO = 'inet_timeout_io'
TTS_PARAM_INET_TIMEOUT_OPEN = 'inet_timeout_open'
TTS_PARAM_LANGUAGE = 'language'
TTS_PARAM_LID_LANGUAGES = 'language_identifier_languages'
TTS_PARAM_LID_MODE = 'language_identifier_mode'
TTS_PARAM_LID_SCOPE = 'language_identifier_scope'
TTS_PARAM_MARKER_MODE = 'marker_mode'
TTS_PARAM_OUTPUT_TYPE = 'output_type'
TTS_PARAM_PRODUCT_VERSION = 'product_version'
TTS_PARAM_RATE = 'rate'
TTS_PARAM_SECURE_CONTEXT = 'secure_context'
TTS_PARAM_SSML_VALIDATION = 'ssml_validation'
TTS_PARAM_VOICE = 'voice'
TTS_PARAM_VOICE_AGE = 'voice_age'
TTS_PARAM_VOICE_GENDER = 'voice_gender'
TTS_PARAM_VOICE_MODEL = 'voice_model'
TTS_PARAM_VOICE_VARIANT = 'voice_variant'
TTS_PARAM_VOLUME = 'volume'

TTS_LINEAR_16BIT = 0
# TTS_MULAW_8BIT = 1
# TTS_ALAW_8BIT = 2

TTS_FREQ_8KHZ = 0
# TTS_FREQ_11KHZ = 1  # not supported
TTS_FREQ_22KHZ = 2

SAMPLE_RATE_CONV = {0: 8000, 1: 11025, 2: 22050}

TTS_SUCCESS = 0
TTS_ENDOFDATA = 21

MAX_BUFFER_SIZE_BYTES = 8192

TTSRETVAL = c_long
LH_VOID = None
HTTSINSTANCE = POINTER(LH_VOID)


class VXIVector(Structure):
    _fields_ = [
        ('dummy', POINTER(None)),
    ]

# CALL BACKS
# CFUNCTION TYPES


def unchecked(typ):
    """ avoid checking of CFUNCTYPES"""
    if hasattr(typ, "_type_") and isinstance(typ._type_, str) and typ._type_ != 'P':
        return typ
    else:
        return c_void_p

TTS_SOURCE_CB = CFUNCTYPE(c_ulong, c_void_p, c_void_p, c_ulong, POINTER(c_ulong))
TTS_DEST_CB = CFUNCTYPE(unchecked(POINTER(c_byte)), c_void_p, c_ushort, c_void_p, c_ulong, POINTER(c_ulong))
TTS_EVENT_CB = CFUNCTYPE(c_ulong, c_void_p, c_void_p, c_ushort, c_ushort)
TTS_LOG_ERROR_CB = CFUNCTYPE(None, c_void_p, c_ulong, c_wchar_p, c_int, POINTER(VXIVector), POINTER(VXIVector))
TTS_LOG_EVENT_CB = CFUNCTYPE(None, c_void_p, c_wchar_p, POINTER(VXIVector), POINTER(VXIVector))
TTS_LOG_DIAGNOSTIC_CB = CFUNCTYPE(None, c_void_p, c_long, c_char_p)


def convert_bytes(typ):
    if typ:
        if isinstance(typ, bytes):
            return typ
        else:
            if isinstance(typ, str):
                return typ.encode('utf-8')
            else:
                return typ
    return None


class TTSOpenSession:
    def __init__(self, session_id, freq=TTS_FREQ_8KHZ):
        #self.fake_buffer = create_string_buffer(MAX_BUFFER_SIZE_BYTES)
        self.audio_buffer = []
        self.httsinstance = HTTSINSTANCE()
        self.open_params = TTS_OPEN_PARAMS(
            fmtVersion=TTS_CURRENT_VERSION,
            szLanguage=cast(b'en-AU', POINTER(c_char)),
            szVoice=cast(b'karen', POINTER(c_char)),
            nFrequency=freq,
            nOutputType=TTS_LINEAR_16BIT,
            TtsSourceCb=TTS_SOURCE_CB(self.tts_source_callback),
            TtsDestCb=TTS_DEST_CB(self.tts_destination_callback),
            TtsEventCb=TTS_EVENT_CB(self.tts_event_callback),
            TtsLogErrorCb=TTS_LOG_ERROR_CB(self.tts_log_error_callback),
            TtsLogEventCb=TTS_LOG_EVENT_CB(self.tts_log_event_callback),
            TtsDiagnosticsCb=TTS_LOG_DIAGNOSTIC_CB(self.tts_log_diagnostic_callback)
        )

        self.speakdata = None
        self.session_id = session_id
        #self.open = print_status(TtsOpen(self.httsinstance, self.open_params, pointer(self.fake_buffer)), 'OPEN TTS')
        self.open = print_status(TtsOpen(self.httsinstance, self.open_params, None), 'OPEN TTS')
        self.session = print_status(TtsSessionStart(self.httsinstance, self.session_id),
                                    '%s SESSION START' % session_id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def process_tts(self, data, outfile='test.wav', typ=b'text/plain'):
        data = data.encode('utf-8') if isinstance(data, str) else data
        # Check Load of XML
        if typ == b'application/synthesis+ssml':
            try:
                tmpxml = etree.fromstring(data)
            except etree.XMLSyntaxError as e:
                print('\n',data, e)
                return e
            # We will override some !required! xml attributes
            # Alternative - Could use params to ignore smml errors UNTESTED

            for elem in tmpxml.getiterator():
                if not hasattr(elem.tag, 'find'): continue  # (1)
                i = elem.tag.find('}')
                if i >= 0:
                    elem.tag = elem.tag[i+1:]
            objectify.deannotate(tmpxml, cleanup_namespaces=True)
            tmpxml.set('xmlns', "http://www.w3.org/2001/10/synthesis")  # namespace for SSML 1.0
            tmpxml.set('{http://www.w3.org/XML/1998/namespace}lang', "en-AU")  # This is the only lang we will be using
            tmpxml.set('version', '1.0')  # Required to be version 1.0
            data = etree.tostring(tmpxml)

        # Create a buffer in the array
        # typ plain/text
        self.speakdata = TTS_SPEAK_DATA(
            uri=None,  # None  # we could use URI ....
            data=cast(data, c_char_p),
            contentType=cast(typ, c_char_p)
        )
        self.speakdata.lengthBytes = len(self.speakdata.data)
        self.audio_buffer.append({'buffer': create_string_buffer(MAX_BUFFER_SIZE_BYTES), 'bytes': b'', 'running': True})
        tc = len(self.audio_buffer)-1
        self.audio_buffer[tc]['address'] = addressof(self.audio_buffer[tc]['buffer'])

        status = -1
        for c in range(10):
            status = TtsProcessEx(self.httsinstance, self.speakdata)
            if status == TTS_SUCCESS:
                with wave.open(outfile, 'wb') as wavfile:
                    wavfile.setparams((1, 2, SAMPLE_RATE_CONV[self.open_params.nFrequency], 0, 'NONE', 'NONE'))
                    wavfile.writeframes(self.audio_buffer[tc]['bytes'])
                    # Clean up
                return status
            print_status(status, 'PROCESS FAILED TRY %s' % (c+1))
            time.sleep(1)

    def tts_ssml_file(self, file, typ=b'application/synthesis+ssml'):
        file = file.encode('utf-8') if isinstance(file, str) else file

    def close(self):
        if self.session == 0:
            print_status(TtsSessionEnd(self.httsinstance), 'SESSION END')
        if self.open == 0:
            print_status(TtsClose(self.httsinstance))

    # CALL BACK FUNCTIONS
    @staticmethod
    def tts_source_callback(pappdata, pinputbuffer, cinputbufferalloc, pcinputbuffer):
        """
            typedef TTSRETVAL (*TTS_SOURCE_CB)(
                LH_VOID* pAppData,
                LH_VOID* pInputBuffer,
                LH_U32 cInputBufferAlloc,
                LH_U32* pcInputBuffer);

        This callback is only invoked when the input streaming mode of the TTS engine is enabled.

        It is used by an engine instance to request a block of input text from the application. The function is called
        multiple times, allowing an unlimited amount of data to be delivered.

        Each time the application puts data into pInputBuffer, the function should return TTS_SUCCESS.

        When there is no more input data for the current TTS action the function should return TTS_ENDOFDATA.
        Then, the TTS engine knows the previous input corresponded with the last input block for a speak action and the
        callback will no longer be called until the TtsProcessEx function returns. Any data in the buffer when
        TTS_ENDOFDATA is returned is ignored.

        Return values:
         * TTS_SUCCESS
         * TTS_ENDOFDATA
        Note: This callback should not be registered unless both the uri and data member of the TTS_SPEAK_DATA structure
        can be NULL. This approach makes it possible to combine the TtsSource source callback function with the TtsProcessEx
        function. When using the source callback method, the input text must be encoded with the character set indicated by
        the TTS_SPEAK_DATA structure passed to TtsProcessEx. See TTS_SPEAK_DATA.

        :param pappdata: Application data pointer that was passed into TtsOpen
        :param pinputbuffer: [out] Pointer to a data buffer that is to be filled with the input text. This buffer is
                                   provided by the callback function, no need to allocate memory for it.
        :param cinputbufferalloc: Size in bytes of the buffer pointed to by pInputBuffer. This is the maximum amount of data
                                  that can be placed in pInputBuffer.
        :param pcinputbuffer: [out] Number of bytes that were actually placed in the buffer.
        :return: ttsretval
        """
        # TTS_SUCCESS
        # TTS_ENDOFDATA
        print('SOURCE CALLBACK')
        return TTS_SUCCESS

    @staticmethod
    def tts_event_callback(pappdata, pevent, ceventbytes, cevent):
        """
        typedef TTSRETVAL (*TTS_EVENT_CB)(
            LH_VOID* pAppData,
            LH_VOID* pEvent,
            LH_U16 cEventBytes,
            LH_U16 eEvent);

            This callback is used to return markers to the application. Each marker represents a single
            event. There is one call to TTS_EVENT_CB for each separate marker. A marker is thrown
            before the call to TTS_DEST_CB that delivers the first audio sample aligned with it. In
            other words, the user receives the marker information in advance of the corresponding
            speech.

            For a description of the different event types, see TTS_EVENT.
            You must specify which marker types to receive by calling TtsSetParamsEx for the
            TTS_MARKER_MODE_PARAM parameter. For a description of the supported marker
            types, see TTS_MARKER.

        :param pappdata: Application data pointer that was passed into TtsOpen.
        :param pevent:
        :param ceventbytes:
        :param cevent:
        :return:
        """

        print(['EVENT', pappdata, pevent, ceventbytes, cevent])

        return TTS_SUCCESS

    @staticmethod
    def tts_log_error_callback(pappdata, u32errorid, szerroridtext, errorseverity, pkeys, pvalues):
        """


        :param pappdata:
        :param u32errorid:
        :param szerroridtext:
        :param errorseverity:
        :param pkeys:
        :param pvalues:
        :return:
        """
        severity = {
            0: "UNKNOWN",  # Unknown error severity
            1: "CRITICAL",  # All instances out of service
            2: "SEVERE",  # Service affecting failure
            3: "WARNING",  # Application or non-service affecting failure
            4: "INFO",  # Informational message
        }
        message = "ERROR: LEVEL", errorseverity, '-', severity[errorseverity], ''.join([x for x in szerroridtext[0:100]])
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f -'), message)
        logger.error(message)


    @staticmethod
    def tts_log_event_callback(pappdata, szevent, pkeys, pvalues):
        events = {
            'NVOCapps': 'application session',
            'NVOCaudf': 'first audio',
            'NVOCaudn': 'next audio',
            'NVOClise': 'license end',
            'NVOClisr': 'license refused',
            'NVOCliss': 'license start',
            'NVOClock': 'license lock',
            'NVOCunlo': 'license unlock',
            'NVOCfrmt': 'file format',
            'NVOCsynd': 'synthesis end',
            'NVOCsyst': 'synthesis start',
            'NVOCsysw': 'synthesis switch',
            'NVOCactp': 'ActivePrompt was used',
            'NVOCifnd': 'internet fetch end',
            'NVOCifst': 'internet fetch start',
            'NVOCinpt': 'input text'
        }
        evcode = "".join([x for x in szevent[0:8]])
        if evcode in events:
            message = ' '.join(['EVENT LOG:', evcode, events[evcode]])
            logger.info(message)
            #print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), message)
            # if evcode == 'NVOCinptx':
            #     for i in range(vxi.VXIVectorLength(pkeys)):
            #         tmp = cast(vxi.VXIStringCStr(vxi.VXIVectorGetElement(pvalues, i)), POINTER(c_char))
            #         print(" ".join([x for x in tmp[0:200] if ord(x) < 128]))


    @staticmethod
    def tts_log_diagnostic_callback(pappdata, s32level, szmessage):
        pass

    def tts_destination_callback(self, pappdata, noutputtype, paudio, caudiobytes, pcaudiobufferalloc):
        """
        :param pappdata: pointer to the memmory buffer i.e. start memmory location of the buffer addressof(pcmBuf)
        :param noutputtype:
        :param paudio:
        :param caudiobytes:
        :param pcaudiobufferalloc: [OUT] set size of next buffer -
        :return:
        """
        # global feedBuf, pcmBuf
        if caudiobytes == 0:
            print('buffer request')
            if not paudio:
                paudio = self.audio_buffer[-1]['address']
        else:
            aubuf = None
            for i, v in enumerate(self.audio_buffer):
                if v['address'] == paudio:
                    aubuf = self.audio_buffer[i]
                    break
            if len([x for x in aubuf['buffer'] if x != b'\00']):
                aubuf['bytes'] += aubuf['buffer'][0:caudiobytes]
        pcaudiobufferalloc.contents.value = MAX_BUFFER_SIZE_BYTES
        return paudio


class TTS_OPEN_PARAMS(Structure):
    _fields_ = [
        ('fmtVersion', c_ushort),  # TTS_VERSION
        ('szLanguage', POINTER(c_char)),
        ('szVoice', POINTER(c_char)),
        ('nFrequency', c_ushort),
        ('nOutputType', c_ushort),

        ('TtsSourceCb', TTS_SOURCE_CB),
        ('TtsDestCb', TTS_DEST_CB),
        ('TtsEventCb', TTS_EVENT_CB),
        ('TtsLogErrorCb', TTS_LOG_ERROR_CB),
        ('TtsLogEventCb', TTS_LOG_EVENT_CB),
        ('TtsDiagnosticsCb', TTS_LOG_DIAGNOSTIC_CB),
    ]


class TTS_SPEAK_DATA(Structure):
    _fields_ = [
        ('uri', c_char_p),
        ('data', c_char_p),
        ('lengthBytes', c_ulong),
        ('contentType', c_char_p),
        ('fetchProperties', c_void_p),  # HTTSMAP
        ('fetchCookieJar', c_void_p),  # HTTSVECTOR
    ]


class TTS_VOICE_INFO(Structure):
    """
    The TTS_VOICE_INFO structure is used by TtsGetVoiceList to return information about an installed TTS engine voice.
    typedef struct TTS_VOICE_INFO {
        LH_CHAR szVersion[TTS_MAX_STRING_LENGTH];
        LH_CHAR szLanguage[TTS_MAX_STRING_LENGTH];
        LH_CHAR szLanguageIETF[TTS_MAX_STRING_LENGTH];
        LH_CHAR szLanguageTLW[4];
        LH_CHAR szVoice[TTS_MAX_STRING_LENGTH];
        LH_CHAR szAge[TTS_MAX_STRING_LENGTH];
        LH_CHAR szGender[TTS_MAX_STRING_LENGTH];
        LH_CHAR szVoiceModel[TTS_MAX_STRING_LENGTH];
        LH_U16 nFrequency;
    } TTS_VOICE_INFO;
    """

    _fields_ = [
        ('szVersion', c_char * 128),
        ('szLanguage', c_char * 128),
        ('szLanguageIETF', c_char * 128),
        ('szLanguageTLW', c_char * 4),
        ('szVoice', c_char * 128),
        ('szAge', c_char * 128),
        ('szGender', c_char * 128),
        ('szVoiceModel', c_char * 128),
        ('nFrequency', c_ushort),
    ]


# ****************************************************************************************
# ************************************** CFUNCTIONS **************************************
# ****************************************************************************************
# TtsSystemInit

# TODO - implement cross platform installations components
components = "c:/Program Files (x86)/*****/*****;-)*******/common/speech/components"

os.environ['PATH'] += os.pathsep + components
tts = cdll.LoadLibrary('lhstts.dll')
# vxi = cdll.LoadLibrary('VXIvalue.dll')


TtsSystemInit = tts.TtsSystemInit
TtsSystemInit.argtypes = [c_char_p]
TtsSystemInit.restype = TTSRETVAL
# TtsSystemTerminate
TtsSystemTerminate = tts.TtsSystemTerminate
TtsSystemTerminate.argtypes = []
TtsSystemTerminate.restype = TTSRETVAL

# TtsOpen
TtsOpen = tts.TtsOpen
TtsOpen.argtypes = [POINTER(HTTSINSTANCE), POINTER(TTS_OPEN_PARAMS), POINTER(LH_VOID)]
TtsOpen.restype = TTSRETVAL

# TtsClose
TtsClose = tts.TtsClose
TtsClose.argtypes = [c_void_p]
TtsClose.restype = TTSRETVAL
# TtsSessionStart
TtsSessionStart = tts.TtsSessionStart
TtsSessionStart.argtypes = [c_void_p, c_char_p]
TtsSessionStart.restype = TTSRETVAL
# TtsSessionEnd
TtsSessionEnd = tts.TtsSessionEnd
TtsSessionEnd.argtypes = [c_void_p]
TtsSessionEnd.restype = TTSRETVAL
# TtsProcessEx
TtsProcessEx = tts.TtsProcessEx
TtsProcessEx.argtypes = [c_void_p, POINTER(TTS_SPEAK_DATA)]
TtsProcessEx.restype = TTSRETVAL
