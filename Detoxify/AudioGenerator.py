from gtts import gTTS
from os import path
import wavio
import numpy as np
from pydub import AudioSegment


mytext = 'I have no idea who you are or what you want, but if  you’re seeking for ransom, I can tell you I don’t have any money'

# Language in which you want to convert
language = 'en'

data = gTTS(text=mytext, lang=language, slow=False)
# y = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
# wavio.write("transcript.wav", y, 22040 ,sampwidth=2)
data.save("transcript.mp3")

# sound = AudioSegment.from_mp3("transcript.mp3")

# sound.export("transcript-4.wav", format="wav")


