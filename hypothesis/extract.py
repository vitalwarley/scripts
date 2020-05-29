import os
import argparse
import re
from datetime import datetime
from hypothesis import Hypothesis as H
from hypothesis import HypothesisAnnotation
from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument('--group-id')
parser.add_argument('--date')
parser.add_argument('--today', action='store_true')

load_dotenv()
USERNAME = os.getenv('USERNAME')
TOKEN = os.getenv('TOKEN')

h = H(username=USERNAME, token=TOKEN, debug=True)

args = parser.parse_args()
groupid = args.group_id
date = args.date
today = args.today

if groupid is not None:
    if today:
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone().isoformat()
    elif date is not None:
        # TODO: validate
        pass
    annotations = h.search_all(params={'search_after': date, 'order': 'asc', 'group': groupid})


#annotations = [{
#    'id': a['id'],
#    'created': a['created'],
#    'group': a['group'],
#    'document': a['document']['title'][0],
#    'text': a['target'][0]['selector'][0]['selector'][1]['exact']
#    } for a in annotations]
annotations = [HypothesisAnnotation(row) for row in annotations]

def clean_text(text):
    # spaces
    text = re.sub(' +', ' ', text.strip())
    # punctuation?
    return text

for a in annotations:
    print(clean_text(a.exact))
    print()

