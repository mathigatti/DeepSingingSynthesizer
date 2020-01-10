from Voice import renderizeVoice
import sys
from convertor import convert
from pydub import AudioSegment
import math
from Constants import ROOT_PATH

def main(**kwargs):

    if "lyrics" in kwargs:
        lyrics = kwargs['lyrics']
    else:
        lyrics = "oo "

    if "notes" in kwargs:
        notes = list(map(int,kwargs['notes'].split(",")))
    else:
        notes = [0]

    if "dur" in kwargs:
        durations = list(map(float,kwargs['dur'].split(",")))
    else:
        durations = [1]

    if 'file' in kwargs:
        filename = kwargs['file']
    else:
        filename = 'output.wav'

    if 'tempo' in kwargs:
        tempo = kwargs['tempo']
    else:
        tempo = 100

    print(kwargs)
    if 'lang' in kwargs:
        languageCode = kwargs['lang']
    else:
        languageCode = "es"

    if 'scale' in kwargs:
        scale = list(map(int,kwargs['scale'].split(",")))
    else:
        scale = [0,2,4,5,7,9,11] # Major Scale

    if 'root' in kwargs:
        root_note = int(kwargs['root'])
    else:
        root_note = 0 # C is the root note

    if 'octave' in kwargs:
        octave = int(kwargs['octave'])
    else:
        octave = 5 # C is the root note

    if 'model' in kwargs:
        renderizeVoice(filename,lyrics,notes,durations,tempo,scale,root_note,octave,languageCode)

        model = kwargs['model']

        sound = AudioSegment.from_file(filename)
        lenght_in_miliseconds = len(sound)

        silence = AudioSegment.silent(duration=5000)

        sound = silence + sound + silence

        sound = sound.set_frame_rate(16000)
        sound = sound.apply_gain(-18 - sound.dBFS)

        # Trying to normalize to 85 db
        # Note: When REPLAYGAIN_REFERENCE_LOUDNESS is not provided the *_GAIN tags are interpreted relative to an assumed target of -18 dBFS.
        max_db = 20 * math.log(sound.apply_gain(-18 - sound.dBFS).max,10)

        print("The file was normalized so now it has {} db as peak value".format(round(max_db),2))
        sound.export(filename, format="wav")

        netA_path = "{}trained_model/{}/generator_ab.npz".format(ROOT_PATH,model)
        netB_path = "{}trained_model/{}/generator_ba.npz".format(ROOT_PATH,model)

        convert(netA_path,netB_path,filename)
        
        sound = AudioSegment.from_file(filename)

        sound = sound[len(silence):-len(silence)]

        padding_audio = AudioSegment.silent(duration=lenght_in_miliseconds-len(sound))
        sound = sound + padding_audio

        sound.export(filename, format="wav")
    else:
        renderizeVoice(filename,lyrics,notes,durations,tempo,scale,root_note,octave,languageCode)

# Run main
main(**dict(arg.split('=') for arg in sys.argv[1:]))