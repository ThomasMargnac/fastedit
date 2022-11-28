from fastedit.Medias import Video, Audio, Image
from fastedit.Overlays import Subtitles, Text
import pytest
import hashlib
import json

# Global variables

test_video = "../../media/test_video.mp4"
test_video_audio = "../../media/test_video_with_audio.mp4"

test_audio = "../../media/test_audio.mp3"

test_subtitles = "../../media/test_subtitles.srt"

# Video testings

def test_clip_with_everything():
	# Importing video
	video = Video(test_video)
	# Clipping video
	video = video.clip(0, 20)
	# Removing all audios from video
	video.removeAudio()
	# Getting metadata
	metadata = video.getMetadata()
	# Verifying number of streams and length of the video
	assert len(metadata["streams"]) == 1
	assert int(float(metadata["streams"][0]["duration"])) == 20
	# Changing video fps
	video.changeFrameRate(60)
	# Getting metadata
	metadata = video.getMetadata()
	# Verifying fps in metadata
	assert metadata['streams'][0]['r_frame_rate'] == '60/1'
	# Importing audio
	audio = Audio(test_audio)
	# Adding audio to video
	video.addAudio(audio=audio, type="add")
	# Getting metadata
	metadata = video.getMetadata()
	# Verifying number of streams
	assert len(metadata["streams"]) == 2
	# Resizing video to 1280x720
	video.resize(width=1280, height=720, type="simple")
	# Getting metadata
	metadata = video.getMetadata()
	# Verifying dimensions
	assert metadata['streams'][0]['width'] == 1280
	assert metadata['streams'][0]['height'] == 720
	# Adding text
	feed_before = open(video._main_temp, "rb").read()
	video.addText([Text("This is my text", "(w-text_w)/2", "(h-text_h)/2", 0, 20)])
	feed_after = open(video._main_temp, "rb").read()
	# Verifying if feeds are different
	assert feed_before != feed_after
	# Adding subtitles
	subtitles = Subtitles(test_subtitles)
	video.addSubtitles(subtitles, "soft")
	# Getting metadata
	metadata = video.getMetadata()
	# Verifying number of streams
	assert len(metadata["streams"]) == 3
	# Converting the video to H.265/HEVC video codec
	video.convert(vcodec="libx265")
	# Getting metadata
	metadata = video.getMetadata()
	assert metadata["streams"][0]["codec_name"] == "hevc"

if __name__ == "__main__":
	pytest.main()