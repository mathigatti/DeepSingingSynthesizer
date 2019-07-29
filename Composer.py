from __future__ import absolute_import, print_function

from MidiFactory import createMidi
import os
from math import ceil

def matchListsSize(rhythm,melody):
    n_rhythm =len(rhythm)
    n_melody = len(melody)
    if n_rhythm < n_melody:
        rhythm = (rhythm*int(ceil(n_melody/float(n_rhythm))))[:n_melody]
    elif n_rhythm != n_melody:
        melody = (melody*int(ceil(n_rhythm/float(n_melody))))[:n_rhythm]

    return rhythm,melody

def toList(rhythm, melody, scale, root_note, octave):

    scaleSize = len(scale)

    volume = 100

    rhythm, melody = matchListsSize(rhythm,melody)

    composition = []
    time = 0
    for i in range(len(rhythm)):
        dur = rhythm[i]

        scale_index = melody[i]%scaleSize
        implicit_octave = melody[i]//scaleSize

        note = (scale[scale_index] + 12*(implicit_octave + octave) + root_note)%255

        composition.append((note,dur,volume,time))
        time += dur

    return composition

def compose(notes, durations, scale, root_note, octave, new_midi_path, new_musicxml_path):

    print(notes)
    print(durations)
    print(scale)
    print(root_note)

    composition = toList(durations,notes,scale,root_note,octave)
    print(composition)
    createMidi(new_midi_path, composition)
    os.system("musescore "+ new_midi_path +" -o " + new_musicxml_path)