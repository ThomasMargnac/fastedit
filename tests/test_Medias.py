from fastedit.Medias import Video, Audio, Image
import pytest
import hashlib

# Video testings

def test_video_loop():
	video = Video("../media/test_video.mp4")
	vlooped = video.loop(40)
	expected = open("../media/test_video_looped.txt", "r").read()
	generated = open(vlooped._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_clip():
	video = Video("../media/test_video.mp4")
	vcliped = video.clip(0, 10)
	expected = open("../media/test_video_cliped.txt", "r").read()
	generated = open(vcliped._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_add_audio_replace():
	video = Video("../media/test_video.mp4")
	audio = Audio("../media/test_audio.mp3")
	video.addAudio(audio, "replace")
	expected = open("../media/test_video_add_audio_replace.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_add_audio_add():
	video = Video("../media/test_video_with_audio.mp4")
	audio = Audio("../media/test_audio.mp3")
	video.addAudio(audio, "add")
	expected = open("../media/test_video_add_audio_add.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_add_audio_combine():
	video = Video("../media/test_video_with_audio.mp4")
	audio = Audio("../media/test_audio.mp3")
	video.addAudio(audio, "combine")
	expected = open("../media/test_video_add_audio_combine.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_remove_audio():
	video = Video("../media/test_video_with_audio.mp4")
	video.removeAudio()
	expected = open("../media/test_video_remove_audio.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

# Audio testings

def test_audio_loop():
	audio = Audio("../media/test_audio.mp3")
	alooped = audio.loop(40)
	expected = open("../media/test_audio_looped.txt", "r").read()
	generated = open(alooped._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_audio_clip():
	audio = Audio("../media/test_audio.mp3")
	acliped = audio.clip(0, 10)
	expected = open("../media/test_audio_cliped.txt", "r").read()
	generated = open(acliped._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

# Image testings

def test_imageToVideo():
	image = Image("../media/test_image.jpeg")
	video = image.toVideo(10)
	expected = open("../media/test_image_to_video.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

if __name__ == "__main__":
	pytest.main()