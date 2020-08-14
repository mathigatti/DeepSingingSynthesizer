# Deep Singing Synthesis
Extension of Sinsy-NG using deep learning models for voice cloning conversion in order to synthesize good and realistic vocals.

## Requirements
- python (Should work on 3 and 2.7 versions)
- musescore (It's used to convert midi to musicxml)

## Installation

Software contained in synthesisSoftware must be installed. 

- libespeag-NG (Install this first)
- Sinsy-NG (Install this second)

## Usage

You can try `main.py` script as a small singing synthesis example. After running this an output wav file will be generated containing the specified vocals.

All the parameters are optional, they contain a default value in case they are not specified. You can specify them in any order when running the program in the command line.

- _notes_: The numerical value of notes in the scale, in C Major would be something like 0:C, 1:D, 2:E, 3:F and so on...
The scale is C major by default, it's hardcoded in the main.py file and can be modified.

- _lyrics_: The text where spaces delimit w

- _dur_: The BPM of each note

- _lang_: the language code, "es" for spanish and "en" for english. There are several languages supported, you can check them [here](http://espeak.sourceforge.net/languages.html).

- _tempo_: The tempo in BPM, 100 by default

- _file_: the name of the output file

### Usage examples

```
python main.py notes=0,1,2,3,4,5,6 octave=5 lang=en file="trump.wav" tempo=80 model=trump lyrics="hello I am donald trump"
```

You can easily modify `main.py` and add notes, duration, language and more as parameters.
