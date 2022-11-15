from fastedit.Composing import VideoComposition
from fastedit.Medias import Video, Audio
import pytest
import hashlib

# Testing video composition

# ffmpeg -i ../media/test_video.mp4 -i ../media/test_video_with_audio.mp4 -filter_complex "concat=n=2:v=1:a=1" -v error output.mp4

def test_video_composition():
	videos = [Video("../media/test_video.mp4"), Video("../media/test_video_with_audio.mp4")]
	composition = VideoComposition(videos)
	video_concat = composition.get()
	expected = open("../media/test_video_composition.txt", "r").read()
	generated = open(video_concat._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

# Testing audio composition

def test_audio_composition():
	pass

if __name__ == "__main__":
	test_video_composition()