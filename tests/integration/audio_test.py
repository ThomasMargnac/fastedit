from fastedit.Medias import Audio
import pytest

# Global variable(s)

test_audio = "../media/test_audio.mp3"

# Audio generation

def change_volume_video():
	audio = Audio(test_audio)
	audio.changeVolume(0.5)
	return audio

# Audio testings

@pytest.mark.parametrize(
	'audio',
	[
		change_volume_video()
	]
)
class TestAudio:
    def test_change_volume(
        self,
        audio: Audio
    ):
        # Copying audio
        audio = Audio(audio._main_temp)
        before = open(audio._main_temp, "rb").read()
        # Changing volume
        audio.changeVolume(0.5)
        after = open(audio._main_temp, "rb").read()
        # Verifying changes
        assert before != after

if __name__ == "__main__":
    pytest.main()