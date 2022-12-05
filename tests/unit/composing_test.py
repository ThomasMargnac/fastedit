from fastedit.Composing import VideoComposition, AudioComposition
from fastedit.Medias import Video, Audio
import pytest
import hashlib

# Testing video composition

def test_video_composition():
	# Defining composition
	videos = [Video("../media/test_video.mp4"), Video("../media/test_video_with_audio.mp4")]
	composition = VideoComposition(videos)
	# Getting composition
	video_concat = composition.get()
	meta = video_concat.getMetadata()
	nb_stream_audio = 0
	nb_stream_video = 0
	for item in meta["streams"]:
		if item["codec_type"] == "audio":
			nb_stream_audio += 1
		elif item["codec_type"] == "video":
			nb_stream_video += 1
	# Verifying changes
	assert nb_stream_video == 1
	assert nb_stream_audio == 1

# Testing audio composition

def test_audio_composition():
	# Defining composition
	audios = [Audio("../media/test_audio.mp3"), Audio("../media/test_audio_2.wav")]
	composition = AudioComposition(audios)
	# Getting composition
	audio_concat = composition.get()
	meta = audio_concat.getMetadata()
	nb_stream_audio = 0
	nb_stream_video = 0
	for item in meta["streams"]:
		if item["codec_type"] == "audio":
			nb_stream_audio += 1
		elif item["codec_type"] == "video":
			nb_stream_video += 1
	# Verifying changes
	assert nb_stream_video == 0
	assert nb_stream_audio == 1

if __name__ == "__main__":
	pytest.main()