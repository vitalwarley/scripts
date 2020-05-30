import argparse

from punctuator import Punctuator
from youtube_transcript_api import YouTubeTranscriptApi

parser = argparse.ArgumentParser()
parser.add_argument('--video-id')
args = parser.parse_args()
video_id = args.video_id
transcript = YouTubeTranscriptApi.get_transcript(video_id)
text = ' '.join([t['text'] for t in transcript])
punctutator = Punctuator('.punctuator/Demo-Europarl-EN.pcl')
print(punctutator.punctuate(text))
