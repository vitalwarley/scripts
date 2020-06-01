import os
import argparse
import re
from datetime import datetime

import pyperclip
from dotenv import load_dotenv

from Hypothesis import Hypothesis as H
from Hypothesis import HypothesisAnnotation

h = None


def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('--group-id')
    parser.add_argument('--date')
    parser.add_argument('--today', action='store_true')
    return parser.parse_args()


def connect_to_hypothesis():
    load_dotenv()
    USERNAME = os.getenv('USERNAME')
    TOKEN = os.getenv('TOKEN')
    h = H(username=USERNAME, token=TOKEN)
    return h


class debug:
    group_id = 'wdkVg8VA'
    today = False
    date = '29-05-2020'


def extract(args=None):
    if args is None:
        return ''

    groupid = args.group_id
    date = args.date
    today = args.today

    if groupid is not None:
        if today:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone().isoformat()
        elif date is not None:
            d, m, y = map(int, date.split('-'))
            date = datetime(y, m, d).astimezone().isoformat()
        annotations_json = h.search_all(params={'search_after': date, 'order': 'asc', 'group': groupid})

    annotations = [HypothesisAnnotation(row) for row in annotations_json]
    return annotations


def add_start_position_to_note(annotation):
    """Adds parent start position to notes.

    Annotations have a `type`: 'annotation', 'reply', or 'pagenote'.

    Only the 'annotation' type have a `start` and `end`.

    For sorting purposes, this function adds a `start` value for the 'reply' type
    annotation. This value is the `end` value of its `references` (the first one).

    Page notes annotations doesn't need to be sorted, as they are generic and not local-specific.
    """
    if annotation.type == 'reply':
        parent_annotation = HypothesisAnnotation(h.get_annotation(annotation.references[0]))  # Why references is a list?
        # And if parent_annotation is another reply? This will only work if the first reply has its start.
        annotation.start = parent_annotation.end
        annotation.text += ' #n'  # To categorize as a note.
    elif annotation.is_page_note:
        annotation.start = 0
        annotation.text += ' #n'  # To categorize as a note.


def preprocess(annotations):

    def clean(text):
        # spaces
        text = re.sub(' +', ' ', text.strip())
        # punctuation 
        text = text.replace('”', '"').replace('“', '"').replace("’", "'")
        return text

    for annotation in annotations:
        add_start_position_to_note(annotation)
        if annotation.type == 'annotation':
            annotation.exact = clean(annotation.exact)
            
    return sorted(annotations, key=lambda a: a.start)


# TODO: how to extract references like (Author et al. 2020)?
def main():
    global h
    h = connect_to_hypothesis()

    args = parse_input()
    annotations = extract(args)
    annotations = preprocess(annotations)

    output = ''
    for a in annotations:
        if a.type == 'reply' or a.is_page_note:
            output += f' - {a.text}\n'
        else:
            output += f'- {a.exact}\n'

    pyperclip.copy(output)
    print('Done! Notes in the clipboard.')

if __name__ == '__main__':
    main()
