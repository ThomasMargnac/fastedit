from fastedit.Medias import Image, Video
import pytest

# Image testings

def test_imageToVideo():
	image = Image("../media/test_image.jpeg")
	video = image.toVideo(10)
	assert isinstance(video, Video)

if __name__ == "__main__":
	pytest.main()