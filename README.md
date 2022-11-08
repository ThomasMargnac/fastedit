# FastEdit

FastEdit is a Python library to edit videos. Thanks to it you can manipulate videos and/or audios with actions such as cut, loop, or concatenate.

FastEdit is based on FFmpeg which means it has to be installed on your machine before using FastEdit.

# Install

```
pip install fastedit
```

# Examples

On videos

```python
# Importing library
from fastedit.Medias import Video

# Importing video
video = Video("input.mp4")

# Get video duration
duration = video.getDuration()

# Looping a video for 100 seconds
video_looped = video.loop(100)

# Clipping video from 0 to 10 seconds
video_cliped = video.clip(0, 10)

# Saving clipped video to file system
video_cliped.save("output.mp4")
```

On audios

```python
# Importing library
from fastedit.Medias import Audio

# Importing audio
audio = Audio("input.mp3")

# Get audio duration
duration = audio.getDuration()

# Looping an audio for 100 seconds
audio_looped = audio.loop(100)

# Clipping audio from 0 to 10 seconds
audio_cliped = audio.clip(0, 10)

# Saving clipped audio to file system
audio_cliped.save("output.mp3")
```

On images

```python
# Importing library
from fastedit.Medias import Image

# Importing images
image = Image("input.jpeg")

# Converting image to a 15 seconds video
video = image.toVideo(15)
```