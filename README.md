# TTS Engine Python API

A sample bit of code that interfaces python to Vocalizer enterprise c++ API components using python ctypes

Streams Text to speach pcm audio converts to wav file via plain text or SSML...

**requires**
* [python](https://www.python.org/) - 3.6+
* [lxml](https://lxml.de/) -  feature-rich and easy-to-use library for processing XML and HTML in the Python language

> There are caveats around licencing restrictions & arrangements.

## Example TTS call
```python
from tts_types import *
sysinit = print_status(TtsSystemInit(None), 'INITIALISE')
TTS_SESSION = TTSOpenSession(session_id=b'TTS', freq=TTS_FREQ_8KHZ) # TTS_FREQ_22KHZ

TTS_SESSION.process_tts(data=data,
                                outfile='out.wav',  # Exported Wav file
                                typ=b'text/plain',  #  b'application/synthesis+ssml' or b'text/plain'
                                freq=TTS_FREQ_8KHZ)
TTS_SESSION.close()
```
