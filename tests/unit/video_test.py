from fastedit.Medias import Video, Audio
from fastedit.Overlays import Subtitles, Text
import pytest
import os

# Global variables

test_video = "../media/test_video.mp4"
test_video_audio = "../media/test_video_with_audio.mp4"

# Video testings

def test_video_loop():
	# Defining video
	video = Video(test_video)
	meta_before = video.getMetadata()
	# Looping video
	vlooped = video.loop(40)
	meta_after = vlooped.getMetadata()
	# Verifying changes
	assert int(float(meta_before["format"]["duration"])) == 30
	assert int(float(meta_after["format"]["duration"])) == 40

def test_video_clip():
	# Defining video
	video = Video(test_video)
	meta_before = video.getMetadata()
	# Clipping video
	vcliped = video.clip(0, 10)
	meta_after = vcliped.getMetadata()
	# Verifying changes
	assert int(float(meta_before["format"]["duration"])) == 30
	assert int(float(meta_after["format"]["duration"])) == 10

def test_video_add_audio_replace():
	# Defining video and audio
	video = Video(test_video)
	audio = Audio("../media/test_audio.mp3")
	meta_before = video.getMetadata()
	nb_streams_before = 0
	for item in meta_before["streams"]:
		if item["codec_type"] != "audio":
			nb_streams_before += 1
	# Adding audio
	video.addAudio(audio, "replace")
	meta_after = video.getMetadata()
	nb_streams_audio_after = 0
	for item in meta_after["streams"]:
		if item["codec_type"] == "audio":
			nb_streams_audio_after += 1
	# Verifying changes
	assert nb_streams_audio_after == 1
	assert len(meta_after["streams"]) - nb_streams_audio_after == nb_streams_before

def test_video_add_audio_add():
	# Defining video and audio
	video = Video(test_video_audio)
	meta_before = video.getMetadata()
	nb_streams_audio_before = 0
	for item in meta_before["streams"]:
		if item["codec_type"] == "audio":
			nb_streams_audio_before += 1
	audio = Audio("../media/test_audio.mp3")
	# Adding audio
	video.addAudio(audio, "add")
	meta_after = video.getMetadata()
	nb_streams_audio_after = 0
	for item in meta_after["streams"]:
		if item["codec_type"] == "audio":
			nb_streams_audio_after += 1
	# Verifying changes
	assert len(meta_after["streams"]) == len(meta_before["streams"]) + 1
	assert nb_streams_audio_after == nb_streams_audio_before + 1

def test_video_add_audio_combine():
	# Defining video and audio
	video = Video(test_video_audio)
	audio = Audio("../media/test_audio.mp3")
	# Adding audio
	video.addAudio(audio, "combine")
	meta_after = video.getMetadata()
	nb_streams_audio_after = 0
	for item in meta_after["streams"]:
		if item["codec_type"] == "audio":
			nb_streams_audio_after += 1
	# Verifying changes
	assert nb_streams_audio_after == 1

def test_video_add_audio_silent():
	# Defining video and audio
	video = Video(test_video)
	meta_before = video.getMetadata()
	nb_streams_no_audio_before = 0
	for item in meta_before["streams"]:
		if item["codec_type"] != "audio":
			nb_streams_no_audio_before += 1
	# Adding audio
	video.addAudio(None, "silent")
	meta_after = video.getMetadata()
	nb_streams_audio_after = 0
	nb_streams_no_audio_after = 0
	for item in meta_after["streams"]:
		if item["codec_type"] == "audio":
			nb_streams_audio_after += 1
		else:
			nb_streams_no_audio_after += 1
	# Verifying changes
	assert nb_streams_audio_after == 1
	assert nb_streams_no_audio_before == nb_streams_no_audio_after

def test_video_remove_audio():
	# Defining video
	video = Video(test_video)
	# Removing audio
	video.removeAudio()
	meta_after = video.getMetadata()
	# Verifying changes
	for item in meta_after["streams"]:
		assert item["codec_type"] != "audio"

def test_video_convert():
	# Defining video
	video = Video(test_video)
	# Converting video
	video.convert("mov")
	metadata_after = video.getMetadata()
	# Verifying changes
	container_after = os.path.splitext(os.path.basename(metadata_after["format"]["filename"]))[1]
	assert container_after == ".mov"

def test_video_change_volume():
	# Defining video
	video = Video(test_video_audio)
	before = open(video._main_temp, "rb").read()
	# Changing volume
	video.changeVolume(0.5)
	after = open(video._main_temp, "rb").read()
	# Verifying changes
	assert before != after

def test_video_resize_simple():
	# Defining video
	video = Video(test_video)
	# Resizing video
	width = 1280
	height = 720
	video.resize(width, height)
	# Verifying changes
	metadata = video.getMetadata()
	isThereVideo = False
	for item in metadata['streams']:
		if item["codec_type"] == 'video':
			isThereVideo = True
			assert item["width"] == width
			assert item["height"] == height
	assert isThereVideo == True

def test_video_resize_aspect_ratio():
	# Defining video
	video = Video(test_video)
	# Resizing video
	width = 1280
	height = 720
	video.resize(width, height)
	# Verifying changes
	metadata = video.getMetadata()
	isThereVideo = False
	for item in metadata['streams']:
		if item["codec_type"] == 'video':
			isThereVideo = True
			assert item["width"] == width
			assert item["height"] == height
	assert isThereVideo == True

def test_video_change_frame_rate():
	# Defining video
	video = Video(test_video)
	frame_rate_before = video.getMetadata()['streams'][0]['r_frame_rate']
	# Changing frame rate
	video.changeFrameRate(60)
	frame_rate_after = video.getMetadata()['streams'][0]['r_frame_rate']
	# Verifying changes
	assert frame_rate_before != frame_rate_after
	assert frame_rate_after == '60/1'

def test_add_subtitles_srt_hard():
	# Defining video
	video = Video(test_video)
	before = open(video._main_temp, "rb").read()
	subtitles = Subtitles("../media/test_subtitles.srt")
	# Adding hard subtitles
	video.addSubtitles(subtitles, "hard")
	after = open(video._main_temp, "rb").read()
	# Verifying changes
	assert before != after

def test_add_subtitles_ass_hard():
	# Defining video
	video = Video(test_video)
	before = open(video._main_temp, "rb").read()
	subtitles = Subtitles("../media/test_subtitles.ass")
	# Adding hard subtitles
	video.addSubtitles(subtitles, "hard")
	after = open(video._main_temp, "rb").read()
	# Verifying changes
	assert before != after

def test_add_subtitles_srt_soft():
	# Defining video
	video = Video(test_video)
	meta_before = video.getMetadata()
	subtitles = Subtitles("../media/test_subtitles.srt")
	# Adding soft subtitles
	video.addSubtitles(subtitles, "soft", 0, "eng")
	meta_after = video.getMetadata()
	# Verifying changes
	assert len(meta_after["streams"]) == len(meta_before["streams"]) + 1

def test_add_subtitles_ass_soft():
	# Defining video
	video = Video(test_video)
	meta_before = video.getMetadata()
	subtitles = Subtitles("../media/test_subtitles.ass")
	# Adding soft subtitles
	video.addSubtitles(subtitles, "soft", 0, "eng")
	meta_after = video.getMetadata()
	# Verifying changes
	assert len(meta_after["streams"]) == len(meta_before["streams"]) + 1

def test_add_text():
	# Defining video
	video = Video(test_video)
	before = open(video._main_temp, "rb").read()
	texts = [
		Text(
			"First Text",
			x="(w-text_w)/2",
			y="(h-text_h)/2",
			start=0,
			end=10,
			fontSize=24
		),
		Text(
			"Second Text",
			x="(w-text_w)/2",
			y="(h-text_h)/2",
			start=10,
			end=20,
			fontSize=24
		)
	]
	# Adding text to video
	video.addText(texts=texts)
	after = open(video._main_temp, "rb").read()
	# Verifying changes
	assert before != after

if __name__ == "__main__":
	pytest.main()