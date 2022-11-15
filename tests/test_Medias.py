from fastedit.Medias import Video, Audio, Image
import pytest
import hashlib

# Media testings

def test_media_metadata():
	video = Video("../media/test_video.mp4")
	expected = open("../media/test_media_metadata.txt", "r").read()
	generated = video.getMetadata()
	assert expected == expected

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

def test_video_add_audio_silent_replace():
	video = Video("../media/test_video_with_audio.mp4")
	video.addAudio(None, type="silent")
	expected = open("../media/test_video_add_audio_silent_replace.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_add_audio_silent():
	video = Video("../media/test_video.mp4")
	video.addAudio(None, type="silent")
	expected = open("../media/test_video_add_audio_silent.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_remove_audio():
	video = Video("../media/test_video_with_audio.mp4")
	video.removeAudio()
	expected = open("../media/test_video_remove_audio.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_convert():
	video = Video("../media/test_video.mp4")
	video.convert("mov")
	expected = open("../media/test_video_convert.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_change_volume():
	video = Video("../media/test_video_with_audio.mp4")
	video.changeVolume(0.5)
	expected = open("../media/test_video_change_volume.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_resize_simple():
	video = Video("../media/test_video.mp4")
	video.resize(720, 480, "simple")
	expected = open("../media/test_video_resize_simple.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_resize_aspect_ratio():
	video = Video("../media/test_video.mp4")
	video.resize(720, 480, "aspect_ratio")
	expected = open("../media/test_video_resize_aspect_ratio.txt", "r").read()
	generated = open(video._main_temp, "rb").read()
	assert hashlib.sha512(generated).hexdigest() == expected

def test_video_change_frame_rate():
	video = Video("../media/test_video.mp4")
	video.changeFrameRate(60)
	frame_rate = video.getMetadata()['streams'][0]['r_frame_rate']
	assert frame_rate == '60/1'

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

def test_audio_change_volume():
	audio = Audio("../media/test_audio.mp3")
	audio.changeVolume(0.5)
	expected = open("../media/test_audio_change_volume.txt", "r").read()
	generated = open(audio._main_temp, "rb").read()
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