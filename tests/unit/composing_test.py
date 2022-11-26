from fastedit.Composing import VideoComposition, AudioComposition
from fastedit.Medias import Video, Audio
import pytest
import hashlib

# Testing video composition

def test_video_composition():
	videos = [Video("../media/test_video.mp4"), Video("../media/test_video_with_audio.mp4")]
	composition = VideoComposition(videos)
	video_concat = composition.get()
	expected = open("../media/test_video_composition.txt", "r").read()
	generated = open(video_concat._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

# Testing audio composition

def test_audio_composition():
	audios = [Audio("../media/test_audio.mp3"), Audio("../media/test_audio_2.wav")]
	composition = AudioComposition(audios)
	audio_concat = composition.get()
	expected = open("../media/test_audio_composition.txt", "r").read()
	generated = open(audio_concat._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

if __name__ == "__main__":
	pytest.main()