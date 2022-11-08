from fastedit.Medias import Video, Audio, Image
import pytest
import hashlib

# Video testings

def test_videoLoop():
	video = Video("../media/test_video.mp4")
	vlooped = video.loop(40)
	expected = open("../media/test_video_looped.mp4", "rb").read()
	generated = open(vlooped._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == hashlib.sha512(expected).hexdigest()

def test_videoClip():
	video = Video("../media/test_video.mp4")
	vcliped = video.clip(0, 10)
	expected = open("../media/test_video_cliped.mp4", "rb").read()
	generated = open(vcliped._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == hashlib.sha512(expected).hexdigest()

# Audio testings

def test_audioLoop():
	pass

def test_audioClip():
	pass

# Image testings

def test_imageToVideo():
	pass

if __name__ == "__main__":
	pytest.main()