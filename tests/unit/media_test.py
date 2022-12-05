from fastedit.Medias import Video
import pytest

# Global variables

test_video = "../media/test_video.mp4"

# Media testings

def test_media_metadata():
	video = Video(test_video)
	metadata = video.getMetadata()
	# Verifying changes
	assert len(metadata["streams"]) == 2

if __name__ == "__main__":
	pytest.main()