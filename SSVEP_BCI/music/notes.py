import pretty_midi
import pickle
import pygame
import base64
import music21 as m21
import numpy as np
import tensorflow as tf
import os

from tqdm import tqdm_notebook
from numpy.random import choice
from keras_self_attention import SeqSelfAttention


noteToMidiId = {
    1: '60',
    2: '62',
    3: '64',
    4: '65',
    5: '67',
    6: '69',
    7: '71'
}
import numpy as np


class NoteTokenizer:
    def __init__(self):
        self.notes_to_index = {}
        self.index_to_notes = {}
        self.num_of_word = 0
        self.unique_word = 0
        self.notes_freq = {}

    def transform(self, list_array):
        """Transform a list of note in string into index.

        Parameters
        ==========
        list_array : list
          list of note in string format

        Returns
        =======
        The transformed list in numpy array.

        """
        transformed_list = []
        for instance in list_array:
            transformed_list.append([self.notes_to_index[note] for note in instance])
        return np.array(transformed_list, dtype=np.int32)

    def partial_fit(self, notes):
        """Partial fit on the dictionary of the tokenizer

        Parameters
        ==========
        notes : list of notes

        """
        for note in notes:
            note_str = ",".join(str(a) for a in note)
            if note_str in self.notes_freq:
                self.notes_freq[note_str] += 1
                self.num_of_word += 1
            else:
                self.notes_freq[note_str] = 1
                self.unique_word += 1
                self.num_of_word += 1
                self.notes_to_index[note_str], self.index_to_notes[self.unique_word] = (
                    self.unique_word,
                    note_str,
                )

    def add_new_note(self, note):
        """Add a new note into the dictionary

        Parameters
        ==========
        note : str
          a new note who is not in dictionary.

        """
        assert note not in self.notes_to_index
        self.unique_word += 1
        self.notes_to_index[note], self.index_to_notes[self.unique_word] = (
            self.unique_word,
            note,
        )


#反馈音符声音
def play_note(pitch="C4", length=2, velocity=127, instrument='Piano'):
    note_1 = m21.note.Note(pitch, quarterLength=length)
    note_1.volume.velocity = velocity
    stream_1 = m21.stream.Stream()
    if instrument == 'Piano':
        stream_1.append(m21.instrument.Piano())
        # stream_1.insert(0, m21.instrument.Piano())
    stream_1.append(note_1)
    s_player = m21.midi.realtime.StreamPlayer(stream_1)
    s_player.play()


#将钢琴卷轴转换为prettymidi对象
def piano_roll_to_pretty_midi(piano_roll, fs=100, program=0):
    '''Convert a Piano Roll array into a PrettyMidi object
     with a single instrument.
    Parameters
    ----------
    piano_roll : np.ndarray, shape=(128,frames), dtype=int
        Piano roll of one instrument
    fs : int
        Sampling frequency of the columns, i.e. each column is spaced apart
        by ``1./fs`` seconds.
    program : int
        The program number of the instrument.
    Returns
    -------
    midi_object : pretty_midi.PrettyMIDI
        A pretty_midi.PrettyMIDI class instance describing
        the piano roll.
    '''
    notes, frames = piano_roll.shape
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program)

    # pad 1 column of zeros so we can acknowledge inital and ending events
    piano_roll = np.pad(piano_roll, [(0, 0), (1, 1)], 'constant')

    # use changes in velocities to find note on / note off events
    velocity_changes = np.nonzero(np.diff(piano_roll).T)

    # keep track on velocities and note on times
    prev_velocities = np.zeros(notes, dtype=int)
    note_on_time = np.zeros(notes)

    for time, note in zip(*velocity_changes):
        # use time + 1 because of padding above
        velocity = piano_roll[note, time + 1]
        time = time / fs
        if velocity > 0:
            if prev_velocities[note] == 0:
                note_on_time[note] = time
                prev_velocities[note] = velocity
        else:
            pm_note = pretty_midi.Note(
                velocity=prev_velocities[note],
                pitch=note,
                start=note_on_time[note],
                end=time)
            instrument.notes.append(pm_note)
            prev_velocities[note] = 0
    pm.instruments.append(instrument)
    return pm


#将ssvep输出音符填充成模型输入序列长度
def generate_from_ssvep_note(note_tokenizer, notes):
  generate = [note_tokenizer.notes_to_index['e'] for i in range(50-len(notes))]
  for i in range(len(notes)):
    generate += [note_tokenizer.notes_to_index[notes[i]]]
  return generate


#model生成音乐
def generate_notes(generate, model, unique_notes, max_generated=1000, seq_len=50):
  for i in tqdm_notebook(range(max_generated), desc='genrt'):
    test_input = np.array([generate])[:,i:i+seq_len]
    predicted_note = model.predict(test_input)
    random_note_pred = choice(unique_notes+1, 1, replace=False, p=predicted_note[0])
    generate.append(random_note_pred[0])
  return generate


#输出midi文件
def write_midi_file_from_generated(generate, note_tokenizer, midi_file_name = "result.mid", start_index=49, fs=8, max_generated=1000):
  note_string = [note_tokenizer.index_to_notes[ind_note] for ind_note in generate]
  array_piano_roll = np.zeros((128,max_generated+1), dtype=np.int16)
  for index, note in enumerate(note_string[start_index:]):
    if note == 'e':
      pass
    else:
      splitted_note = note.split(',')
      for j in splitted_note:
        array_piano_roll[int(j),index] = 1
  generate_to_midi = piano_roll_to_pretty_midi(array_piano_roll, fs=fs)
  print("Tempo {}".format(generate_to_midi.estimate_tempo()))
  for note in generate_to_midi.instruments[0].notes:
    note.velocity = 100
  generate_to_midi.write(midi_file_name)


#接收ssvep生成的音符生成旋律
def ssvep_music(outputNoteList=[1,2,3,4,5,6,7], max_generate=100, expInfo={'participant': 'test', 'session': '1'}):
    seq_len = 50
    # [note_tokenizer.notes_to_index['e'] for i in range(50 - len(notes))]
    notes = [noteToMidiId[i] for i in outputNoteList]
    # print(notes)
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    print(_thisDir)
    model = tf.keras.models.load_model(_thisDir + '/music_model/model_ep100.h5',
                                       custom_objects=SeqSelfAttention.get_custom_objects())
    note_tokenizer = pickle.load(open(_thisDir + "/music_model/tokenizer_ep100.p", "rb"))

    generate = generate_from_ssvep_note(note_tokenizer, notes)
    unique_notes = note_tokenizer.unique_word
    generate = generate_notes(generate, model, unique_notes, max_generate, seq_len)
    filename = _thisDir + './midi/' + expInfo['participant'] + '_' + expInfo['session'] +'.mid'
    write_midi_file_from_generated(generate, note_tokenizer, filename, start_index=49, fs=5, max_generated=max_generate)

# ssvep_music()

def play_music(music_file):
    """
       stream music with mixer.music module in blocking manner
       this will stream the sound from disk while playing
       """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print
        "Music file %s loaded!" % music_file
    except pygame.error:
        print
        "File %s not found! (%s)" % (music_file, pygame.get_error())
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)

def play_ssvep_music(expInfo):
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(0.8)

    _thisDir = os.path.dirname(os.path.abspath(__file__))
    music_file = _thisDir + './midi/' + expInfo['participant'] + '_' + expInfo['session'] +'.mid'

    try:
        # use the midi file you just saved
        play_music(music_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit