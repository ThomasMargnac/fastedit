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
		self.__temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		extension = os.path.splitext(path)[1]
		self.__main_temp_video = os.path.join(self.__temp_folder.name, "main" + extension)
		shutil.copy(path, self.__main_temp_video)
		self.__second_temp_video = os.path.join(self.__temp_folder.name, "second" + extension)

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
			str(self.__main_temp_video),
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
				str(self.__main_temp_video),
				"-c",
				"copy",
				"-v",
				"quiet",
				str(self.__second_temp_video),
				"-y"
			]
			# Running command and getting output in pipe
			run = sp.run(
				command
			)
			# Moving second file content to main file
			if run.returncode != 0:
				raise ValueError("Something went wrong with FFmpeg")
			return Video(self.__second_temp_video)
	
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
	"""command = [
		"ffprobe",
		"-i",
		"../videos/sample2.mp4",
		"-show_entries",
		"format=duration",
		"-v",
		"quiet"
	]
	print(" ".join(command))
	# Running command and getting output in pipe
	run = sp.run(
		command,
		stdout=sp.PIPE,
		stderr=sp.PIPE
	)
	print(run.returncode)
	print(run.stdout)
	print(run.stderr)"""
	myvideo = Video("../videos/sample2.mp4")
	print(myvideo.getDuration())
	longer = myvideo.loop(100)
	print(longer.getDuration())