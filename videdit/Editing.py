import subprocess as sp
import tempfile
import shutil
import os

class Video():
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
		path: Path to the video.
		"""
		# Creating temporary folder
		cwd = os.getcwd()
		temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		self.__main_temp_video = tempfile.NamedTemporaryFile(dir=temp_folder.name, delete=False)
		shutil.copy(path, self.__main_temp_video.name)
		self.__second_temp_video = tempfile.NamedTemporaryFile(dir=temp_folder.name, delete=False)

	def getDuration(
		self
	):
		"""
		Description
		--------------------------
		Get current video duration.
		"""
		# Preparing command
		command = [
			"ffprobe",
			"-i",
			str(self.__main_temp_video.name),
			"-show_entries",
			"format=duration",
			"-v",
			"quiet",
			#"-of",
			#"csv=\"p=0\""
		]
		# Running command and getting output in pipe
		run = sp.run(
			command
		)
		# Reading stout

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
				str(self.__main_temp_video.name),
				"-c",
				"copy",
				str(self.__second_temp_video.name),
				"-y"
			]
			# Running command and getting output in pipe
			run = sp.Popen(
				command
			)
			# Moving second file content to main file
			shutil.move(
				self.__second_temp_video.name,
				self.__main_temp_video.name
			)
	
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
		pass

	def flip(
		self,
		type
	):
		pass

	def save(
		self,
		path,
		codec
	):
		pass

class Audio():
	def __init__(
		self,
		path
	):
		pass

class Composition():
	def __init__(
		self
	):
		pass

if __name__ == "__main__":
	myvideo = Video("../videos/sample2.mp4")
	myvideo.getDuration()
	#myvideo.loop(40.5)