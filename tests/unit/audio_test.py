from fastedit.Medias import Audio
import pytest

# Global variables

test_audio_mp3 = "../media/test_audio.mp3"

# Audio testings

def test_audio_loop():
	# Defining audio
	audio = Audio(test_audio_mp3)
	meta_before = audio.getMetadata()
	# Looping audio
	alooped = audio.loop(40)
	meta_after = alooped.getMetadata()
	# Verifying changes
	assert int(float(meta_before["format"]["duration"])) == 27
	assert int(float(meta_after["format"]["duration"])) == 40

def test_audio_clip():
	# Defining audio
	audio = Audio(test_audio_mp3)
	meta_before = audio.getMetadata()
	# Clipping audio
	acliped = audio.clip(0, 10)
	meta_after = acliped.getMetadata()
	# Verifying changes
	assert int(float(meta_before["format"]["duration"])) == 27
	assert int(float(meta_after["format"]["duration"])) == 10

def test_audio_change_volume():
	# Defining audio
	audio = Audio(test_audio_mp3)
	before = open(audio._main_temp, "rb").read()
	# Changing volume
	audio.changeVolume(0.5)
	after = open(audio._main_temp, "rb").read()
	# Verifying changes
	assert before != after

if __name__ == "__main__":
	pytest.main()