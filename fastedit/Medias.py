import subprocess as sp
import tempfile
import shutil
import os

class Media():
	def __init__(
		self,
		path
	):
		"""
		Description
		--------------------------
		Initializing media class

		Argument(s)
		--------------------------
		path: Path to the media file.
		"""
		# Creating temporary folder
		cwd = os.getcwd()
		self._temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		extension = os.path.splitext(path)[1]
		self._main_temp = os.path.join(self._temp_folder.name, "main" + extension)
		shutil.copy(path, self._main_temp)
		self._second_temp = os.path.join(self._temp_folder.name, "second" + extension)
	
	def getDuration(
		self
	):
		"""
		Description
		--------------------------
		Get current media duration.
		"""
		# Preparing command
		command = [
			"ffprobe",
			"-i",
			str(self._main_temp),
			"-show_entries",
			"format=duration",
			"-v",
			"quiet",
			"-of",
			"default=noprint_wrappers=1:nokey=1"
		]
		# Running command and getting output in pipe
		run = sp.run(
			command,
			stdout=sp.PIPE,
			stderr=sp.PIPE
		)
		# Reading stout
		if run.returncode != 0:
			raise ValueError("Something went wrong with FFprobe")
		duration = float(run.stdout.decode().split()[0])
		return duration
	
	def save(
		self,
		path: str,
		codec: str = "copy"
	):
		"""
		Description
		--------------------------
		Saving the media to the file system

		Argument(s)
		--------------------------
		path: Path to the file to save the media.
		codec: Codec to encode the media. "copy" by default which copies the codec from the original media.
		"""
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-c",
			codec,
			"-v",
			"quiet",
			path,
			"-y"
		]
		# Running command
		run = sp.run(
			command
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise ValueError("Something went wrong with FFmpeg")

class Video(Media):
	def __init__(
		self,
		path
	):
		"""
		Description
		--------------------------
		Initializing video class

		Argument(s)
		--------------------------
		path: Path to the video file.
		"""
		# Initializing object
		super().__init__(path)

	def loop(
		self,
		duration
	):
		"""
		Description
		--------------------------
		Create a loop from a video

		Argument(s)
		--------------------------
		duration: Duration of the loop.
		"""
		# Checking type of duration
		if type(duration) not in [int, float]:
			raise TypeError("Duration has to be an Integer or Float, actual duration type is " + type(duration))
		# Getting the actual video duration
		videoDuration = self.getDuration()
		# Apply transformation on video based on desired duration
		if duration != videoDuration:
			# Preparing command
			command = [
				"ffmpeg",
				"-stream_loop",
				"-1",
				"-t",
				str(duration),
				"-i",
				str(self._main_temp),
				"-c",
				"copy",
				"-v",
				"quiet",
				str(self._second_temp),
				"-y"
			]
			# Running command
			run = sp.run(
				command
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise ValueError("Something went wrong with FFmpeg")
			return Video(self._second_temp)
	
	def clip(
		self,
		start,
		end
	):
		"""
		Description
		--------------------------
		Extract a part of the video

		Argument(s)
		--------------------------
		start: Time where the clip starts.
		end: Time where the clip ends.
		"""
		# Verifying arguments' types
		if type(start) not in [int, float]:
			raise TypeError("Start has to be an Integer or Float, actual start type is " + type(start))
		if type(end) not in [int, float]:
			raise TypeError("End has to be an Integer or Float, actual end type is " + type(end))
		# Getting video duration to verify if end is actually lower than it
		videoDuration = self.getDuration()
		# Applying transformation
		if end < videoDuration:
			# Preparing command
			command = [
				"ffmpeg",
				"-ss",
				str(start),
				"-to",
				str(end),
				"-i",
				self._main_temp,
				"-c",
				"copy",
				"-v",
				"quiet",
				self._second_temp,
				"-y"
			]
			# Running command
			run = sp.run(
				command
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise ValueError("Something went wrong with FFmpeg")
			return Video(self._second_temp)

class Image():
	def __init__(
		self,
		path
	):
		"""
		Description
		--------------------------
		Initializing Image class

		Argument(s)
		--------------------------
		path: Path to the Image file.
		"""
		# Initializing object
		super().__init__(path)
		self._video_temp = os.path.join(self._temp_folder.name, "video")

	def toVideo(
		self,
		duration,
		fps: int = 30,
		height: int = 720,
		width: int = 1280,
		pix_fmt: str = "yuv420p",
		format: str = "mp4"
	):
		"""
		Description
		--------------------------
		Convert Image to Video

		Argument(s)
		--------------------------
		duration: Duration of the video in seconds.
		fps: Framerate of the video. Default 30.
		height: Height of the video. Default 720.
		width: Width of the video. Default 1280.
		pix_fmt: Pixel format of the video. Default yuv420p.
		"""
		if duration > 0:
			# Prepare files
			video_temp = os.path.join(self._temp_folder.name, "video." + format)
			# Preparing command
			command = [
				"ffmpeg",
				"-loop",
				"1",
				"-framerate",
				str(fps),
				"-i",
				str(self._main_temp),
				"-t",
				str(duration),
				"-s",
				str(width) + "x" + str(height),
				"-pix_fmt",
				pix_fmt,
				str(video_temp),
				"-v",
				"error",
				"-y"
			]
			# Running command
			run = sp.run(
				command
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise ValueError("Something went wrong with FFmpeg")
			return Video(video_temp)

class Audio(Media):
	def __init__(
		self,
		path
	):
		"""
		Description
		--------------------------
		Initializing audio class

		Argument(s)
		--------------------------
		path: Path to the audio file.
		"""
		# Initializing object
		super().__init__(path)
	
	def loop(
		self,
		duration
	):
		"""
		Description
		--------------------------
		Create a loop from an audio

		Argument(s)
		--------------------------
		duration: Duration of the loop.
		"""
		# Checking type of duration
		if type(duration) not in [int, float]:
			raise TypeError("Duration has to be an Integer or Float, actual duration type is " + type(duration))
		# Getting the actual video duration
		videoDuration = self.getDuration()
		# Apply transformation on video based on desired duration
		if duration != videoDuration:
			# Preparing command
			command = [
				"ffmpeg",
				"-stream_loop",
				"-1",
				"-t",
				str(duration),
				"-i",
				str(self._main_temp),
				"-c",
				"copy",
				"-v",
				"quiet",
				str(self._second_temp),
				"-y"
			]
			# Running command
			run = sp.run(
				command
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise ValueError("Something went wrong with FFmpeg")
			return Audio(self._second_temp)
	
	def clip(
		self,
		start,
		end
	):
		"""
		Description
		--------------------------
		Extract a part of the audio

		Argument(s)
		--------------------------
		start: Time where the clip starts.
		end: Time where the clip ends.
		"""
		# Verifying arguments' types
		if type(start) not in [int, float]:
			raise TypeError("Start has to be an Integer or Float, actual start type is " + type(start))
		if type(end) not in [int, float]:
			raise TypeError("End has to be an Integer or Float, actual end type is " + type(end))
		# Getting video duration to verify if end is actually lower than it
		videoDuration = self.getDuration()
		# Applying transformation
		if end < videoDuration:
			# Preparing command
			command = [
				"ffmpeg",
				"-ss",
				str(start),
				"-to",
				str(end),
				"-i",
				self._main_temp,
				"-c",
				"copy",
				"-v",
				"quiet",
				self._second_temp,
				"-y"
			]
			# Running command
			run = sp.run(
				command
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise ValueError("Something went wrong with FFmpeg")
			return Audio(self._second_temp)

if __name__ == "__main__":
	video = Video("../media/test_video.mp4")
	vlooped = video.clip(0,10)
	vlooped.save("../media/test_video_cliped.mp4")
	audio = Audio("../media/test_audio.mp3")
	alooped = audio.clip(0,10)
	alooped.save("../media/test_audio_cliped.mp3")