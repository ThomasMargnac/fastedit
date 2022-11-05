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
			# Returning the video
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
				"-i",
				self.__main_temp_video,
				"-to",
				str(end),
				"-c",
				"copy",
				"-v",
				"quiet",
				self.__second_temp_video,
				"-y"
			]
			# Running command and getting output in pipe
			run = sp.run(
				command
			)
			# Returning the video
			if run.returncode != 0:
				raise ValueError("Something went wrong with FFmpeg")
			return Video(self.__second_temp_video)

	def flip(
		self,
		type
	):
		pass

	def save(
		self,
		path: str,
		codec: str = "copy"
	):
		"""
		Description
		--------------------------
		Saving the video to the file system

		Argument(s)
		--------------------------
		path: Path to the file to save the video.
		codec: Codec to encode the video. "copy" by default which copies the codec from the original video.
		"""
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self.__main_temp_video,
			"-c",
			codec,
			"-v",
			"quiet",
			path,
			"-y"
		]
		# Running command and getting output in pipe
		run = sp.run(
			command
		)
		# Moving second file content to main file
		if run.returncode != 0:
			raise ValueError("Something went wrong with FFmpeg")

class Audio():
	def __init__(
		self,
		path
	):
		pass

if __name__ == "__main__":
	myvideo = Video("../videos/sample2.mp4")
	print(myvideo.getDuration())
	longer = myvideo.clip(0,10)
	longer.save("final.mp4")