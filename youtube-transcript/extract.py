import argparse

import pyperclip
from punctuator import Punctuator
from youtube_transcript_api import YouTubeTranscriptApi

parser = argparse.ArgumentParser()
parser.add_argument('--video-id')
args = parser.parse_args()
video_id = args.video_id
transcript = YouTubeTranscriptApi.get_transcript(video_id)
# TODO: parse to markdown
text = ' '.join([t['text'] for t in transcript])
punctutator = Punctuator('.punctuator/Demo-Europarl-EN.pcl')
pyperclip.copy(punctutator.punctuate(text))
