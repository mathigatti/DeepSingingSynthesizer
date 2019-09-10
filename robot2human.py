from Voice import renderizeVoice
import sys
from convertor import convert
from pydub import AudioSegment
import math
from Constants import ROOT_PATH


def main():
        filename = sys.argv[1]
        model = sys.argv[2]

        sound = AudioSegment.from_file(filename)
        lenght_in_miliseconds = len(sound)
        sound = sound.set_frame_rate(16000)
        sound = sound.apply_gain(-18 - sound.dBFS)

        # Trying to normalize to 85 db
        # Note: When REPLAYGAIN_REFERENCE_LOUDNESS is not provided the *_GAIN tags are interpreted relative to an assumed target of -18 dBFS.
        max_db = 20 * math.log(sound.apply_gain(-18 - sound.dBFS).max,10)

        print("The file was normalized so now it has {} db as peak value".format(round(max_db),2))

        silence = AudioSegment.silent(duration=5000)
        sound = silence + sound + silence
        sound.export(filename, format="wav")

        netA_path = "{}trained_model/{}/generator_ab.npz".format(ROOT_PATH,model)
        netB_path = "{}trained_model/{}/generator_ba.npz".format(ROOT_PATH,model)

        convert(netA_path,netB_path,filename)
        
        sound = AudioSegment.from_file(filename)

        sound = sound[len(silence):-len(silence)]

        padding_audio = AudioSegment.silent(duration=lenght_in_miliseconds-len(sound))
        sound = sound + padding_audio

        sound.export(filename, format="wav")

main()