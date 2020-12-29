import os
import argparse

import pyperclip
from punctuator import Punctuator
from youtube_transcript_api import YouTubeTranscriptApi

parser = argparse.ArgumentParser()
parser.add_argument('--video-id')
parser.add_argument('--save-to', default=None)
args = parser.parse_args()

video_id = args.video_id
save_to = args.save_to

transcript = YouTubeTranscriptApi.get_transcript(video_id)
# TODO: parse to markdown
text = ' '.join([t['text'] for t in transcript])
punctutator = Punctuator('.punctuator/Demo-Europarl-EN.pcl')
output = punctutator.punctuate(text)

if save_to:
    save_to = os.path.expanduser(save_to)
    with open(save_to, 'w') as f:
        f.write(output)
else:
    pyperclip.copy(output)
