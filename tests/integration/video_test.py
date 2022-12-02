from fastedit.Medias import Video, Audio, Image
from fastedit.Overlays import Subtitles, Text
import pytest
import hashlib
import json
import copy
import os

# Global variables

test_video = "../../media/test_video.mp4"
test_audio = "../../media/test_audio.mp3"
test_subtitles = "../../media/test_subtitles.srt"

# Video generation

def add_audio_video():
	video = Video(test_video)
	video.addAudio(Audio(test_audio), "replace")
	return video

def add_subtitles_video():
	video = Video(test_video)
	subtitles = Subtitles(test_subtitles)
	video.addSubtitles(subtitles, "soft")
	return video

def change_frame_rate_video():
	video = Video(test_video)
	video.changeFrameRate(15)
	return video

def change_volume_video():
	video = Video(test_video)
	video.changeVolume(0.5)
	return video

def convert_video():
	video = Video(test_video)
	video.convert("mov")
	return video

def remove_audio_video():
	video = Video(test_video)
	video.removeAudio()
	return video

def resize_video():
	video = Video(test_video)
	video.resize(720, 480, "simple")
	return video

# Video testings

@pytest.mark.parametrize(
	'video',
	[
		add_audio_video(),
		add_subtitles_video(),
		change_frame_rate_video(),
		change_volume_video(),
		convert_video(),
		remove_audio_video()
	]
)
class TestVideo:
	def test_add_subtitles(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
		metadata_before = video.getMetadata()
		# Adding subtitles
		subtitles = Subtitles(test_subtitles)
		video.addSubtitles(subtitles, "soft")
		# Verifying changes
		metadata_after = video.getMetadata()
		assert len(metadata_after["streams"]) == (len(metadata_before["streams"]) + 1)

	def test_add_text(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
		before = open(video._main_temp, "rb").read()
		# Adding text
		texts = [Text("First Text", x="(w-text_w)/2", y="(h-text_h)/2", start=0, end=10, fontSize=24)]
		video.addText(texts=texts)
		after = open(video._main_temp, "rb").read()
		# Verifying changes
		assert before != after

	def test_change_frame_rate(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
		frame_rate_before = video.getMetadata()['streams'][0]['r_frame_rate']
		# Changing frame rate
		video.changeFrameRate(60)
		frame_rate_after = video.getMetadata()['streams'][0]['r_frame_rate']
		# Verifying changes
		assert frame_rate_before != frame_rate_after
		assert frame_rate_after == '60/1'

	def test_change_volume(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
		before = open(video._main_temp, "rb").read()
		# Changing volume
		video.changeVolume(0.5)
		after = open(video._main_temp, "rb").read()
		# Verifying changes
		assert before != after

	def test_clip(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
		duration_before = int(float(video.getMetadata()["format"]["duration"]))
		# Clipping video
		video = video.clip(0, 10)
		duration_after = int(float(video.getMetadata()["format"]["duration"]))
		# Verifying changes
		assert duration_before != duration_after
		assert duration_after == 10

	def test_convert(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
		metadata_before = video.getMetadata()
		# Converting video
		video.convert(vcodec="libx265")
		metadata_after = video.getMetadata()
		# Verifying changes
		assert metadata_before["streams"][0]["codec_name"] == "h264"
		assert metadata_before["streams"][0]["codec_name"] != metadata_after["streams"][0]["codec_name"]
		assert metadata_after["streams"][0]["codec_name"] == "hevc"

	def test_loop(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
		duration_before = int(float(video.getMetadata()["format"]["duration"]))
		# Looping over video
		video = video.loop(40)
		duration_after = int(float(video.getMetadata()["format"]["duration"]))
		# Verifying changes
		assert duration_before == 30
		assert duration_before != duration_after
		assert duration_after == 40

	def test_remove_audio(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
		# Removing audio
		video.removeAudio()
		# Verifying changes
		metadata = video.getMetadata()
		for item in metadata['streams']:
			assert item["codec_type"] != 'audio'

	def test_resize(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
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

	def test_save(
		self,
		video: Video
	):
		# Copying video
		video = Video(video._main_temp)
		# Saving file
		name = os.path.basename(video._main_temp)
		video.save(name)
		# Verifying changes
		assert os.path.isfile(name) == True

if __name__ == "__main__":
	pytest.main()