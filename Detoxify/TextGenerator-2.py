#!/usr/bin/python
import sys
import urllib.request
import json
try:
    filename = "text1.txt"
except IndexError:
    print('Usage: transcribe.py <file>')
    sys.exit(1)

f = open(filename)
data = f.read()
f.close()

req = urllib.request.Request('https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US', data=data, headers={'Content-type': 'audio/x-flac; rate=16000'})

try:
    ret = urllib.request.urlopen(req)
except urllib.request.URLError:
    print("Error Transcribing Voicemail")
    sys.exit(1)

resp = ret.read()
text = json.loads(resp)['hypotheses'][0]['utterance']
print(text)