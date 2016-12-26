import sys
import os
import csv
from collections import namedtuple
import pycrfsuite
import glob


def get_utterances_from_file(dialog_csv_file):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]


def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)


def get_data(data_dir):
    """Generates lists of utterances from each dialog file.

    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))

    for dialog_filename in dialog_filenames:
        yield get_utterances_from_filename(dialog_filename)


DialogUtterance = namedtuple("DialogUtterance", ("act_tag", "speaker", "pos", "text"))

PosTag = namedtuple("PosTag", ("token", "pos"))


def _dict_to_dialog_utterance(du_dict):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)

    #####The code starts from here#####


_author_ = 'rini'

inputpath = sys.argv[1]
inputdata = get_data(inputpath)
unlabeled = sys.argv[2]
testdata = get_data(unlabeled)
xtrain = []
ytrain = []
speaker_current = set()
speaker_set_output = set()
result_dict = {}
count = 0
SPEAKER = ""
baseline_crf = sys.argv[3]

for every in inputdata:
    firstutt = True
    continueSpeak = 1
    speaker_current.clear()
    i = 0
    for UTTERANCE in every:
        i = i + 1
        newout = []

        if firstutt:
            newout.append("FIRST UTTERANCE=True")
            firstutt = False
            newout.append("SPEAKER CHANGED=False")
            speaker_current.add(UTTERANCE[1])

        elif UTTERANCE[1] in speaker_current:
            newout.append("FIRST UTTERANCE=False")
            newout.append("SPEAKER CHANGED=False")

        elif UTTERANCE[1] not in speaker_current:
            newout.append("FIRST UTTERANCE=False")
            newout.append("SPEAKER CHANGED=True")
            speaker_current.clear()
            speaker_current.add(UTTERANCE[1])

        if UTTERANCE[2]:
            for other in UTTERANCE[2]:
                newout.append("token=TOKEN_" + other[0])
                newout.append("pos=POS_" + other[1])
        xtrain.append(newout)
        ytrain.append(UTTERANCE[0])

trainer = pycrfsuite.Trainer(verbose=False)
trainer.set_params({
    'c1': 1.0,
    'c2': 1e-3,
    'max_iterations': 80,
    'feature.possible_transitions': True
})

trainer.append(xtrain, ytrain)
trainer.train('baseline_crffile')
tagger = pycrfsuite.Tagger()
tagger.open('baseline_crffile')
filedict = {}


def get_filename(data_dir, tagtype=None):
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    n = 0
    for dialog_filename in dialog_filenames:
        if tagtype == "Output":
            filedict[n] = dialog_filename.split('/')[-1]
            n += 1
    return filedict


newdict = get_filename(unlabeled, tagtype="Output")

for every in testdata:
    dev_list = []
    output_list = []
    firutt = True
    speaker_set_output.clear()
    j = 0
    continueSpeak = 1
    for UTTERANCE in every:
        newout1 = []
        j = j + 1

        if firutt:
            newout1.append("FIRST UTTERANCE=True")
            firutt = False
            newout1.append("SPEAKER CHANGED=False")
            speaker_set_output.add(UTTERANCE[1])


        elif UTTERANCE[1] in speaker_set_output:
            newout1.append("FIRST UTTERANCE=False")
            newout1.append("SPEAKER CHANGED=False")

        elif UTTERANCE[1] not in speaker_set_output:
            newout1.append("FIRST UTTERANCE=False")
            newout1.append("SPEAKER CHANGED=True")
            speaker_set_output.clear()
            speaker_set_output.add(UTTERANCE[1])

        if UTTERANCE[2]:
            for other in UTTERANCE[2]:
                newout1.append("token=TOKEN_" + other[0])
                newout1.append("pos=POS_" + other[1])
        dev_list.append(newout1)
    output_list = tagger.tag(dev_list)
    result_dict[newdict[count]] = output_list
    count += 1

def save_file():
    return result_dict

with open(baseline_crf, 'w') as f:
    for each in result_dict.keys():
        f.write("Filename=" + "\"" + each + "\"" + "\n")
        for each in result_dict[each]:
            f.write(each + "\n")
        f.write("\n")
