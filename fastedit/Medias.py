import subprocess as sp
import tempfile
import shutil
import json
import os
from fastedit.Errors import FFmpegError, FFprobeError

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
			"error",
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
			raise FFprobeError("Something went wrong with FFprobe")
		duration = float(run.stdout.decode().split()[0])
		return duration
	
	def getMetadata(
		self
	):
		"""
		Description
		--------------------------
		Get current media metadata.
		"""
		# Preparing command
		command = [
			"ffprobe",
			"-loglevel",
			"0",
			"-print_format",
			"json",
			"-show_format",
			"-show_streams",
			"-v",
			"error",
			str(self._main_temp)
		]
		# Running command and getting output in pipe
		run = sp.run(
			command,
			stdout=sp.PIPE,
			stderr=sp.PIPE
		)
		# Reading stout
		if run.returncode != 0:
			raise FFprobeError("Something went wrong with FFprobe")
		metadata = json.loads(run.stdout.decode())
		return metadata
	
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
			"error",
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

	def changeVolume(
		self,
		volume
	):
		"""
		Description
		--------------------------
		Change the volume of the audio

		Argument(s)
		--------------------------
		volume: Factor by which the volume will be changed
		"""
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-filter:a",
			"volume=" + str(volume),
			"-v",
			"error",
			self._second_temp
		]
		# Running command
		run = sp.run(
			command,
			stderr=sp.PIPE
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise FFmpegError(run.stderr.decode())
		# Moving generated audio to Object audio
		shutil.move(self._second_temp, self._main_temp)

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
				"error",
				str(self._second_temp),
				"-y"
			]
			# Running command
			run = sp.run(
				command,
				stderr=sp.PIPE
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise FFmpegError(run.stderr.decode())
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
				"error",
				self._second_temp,
				"-y"
			]
			# Running command
			run = sp.run(
				command,
				stderr=sp.PIPE
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise FFmpegError(run.stderr.decode())
			return Video(self._second_temp)

	def addAudio(
		self,
		audio,
		type: str = None
	):
		"""
		Description
		--------------------------
		Add or replace audio on the video

		Argument(s)
		--------------------------
		audio: Audio instance you want to add.
		type: Method to add audio. Available options : "replace", "add", "combine" or "silent".
		"""
		# Verifying if type is correct
		types = ["replace", "add", "combine", "silent"]
		if type not in types:
			raise ValueError("Type should be one of {}, but yours is {}".format(types, type))
		# Preparing command
		if audio != None:
			command = [
				"ffmpeg",
				"-i",
				self._main_temp,
				"-i",
				audio._main_temp
			]
			# The user wants to replace the original audio
			if type == "replace":
				end = [
					"-map",
					"0:v",
					"-map",
					"1:a",
					"-vcodec",
					"copy",
					"-v",
					"error",
					self._second_temp,
					"-y"
				]
				command.extend(end)
			# The user wants to add another audio file to the video
			elif type == "add":
				end = [
					"-map",
					"0",
					"-map",
					"1:a",
					"-vcodec",
					"copy",
					"-v",
					"error",
					self._second_temp,
					"-y"
				]
				command.extend(end)
			# The user wants to combine the original audio with another audio file
			elif type == "combine":
				end = [
					"-filter_complex",
					"[0:a][1:a]amerge=inputs=2[a]",
					"-map",
					"0:v",
					"-map",
					"[a]",
					"-vcodec",
					"copy",
					"-ac",
					"2",
					"-v",
					"error",
					self._second_temp,
					"-y"
				]
				command.extend(end)
		else:
			command = [
				"ffmpeg",
				"-f",
				"lavfi",
				"-i",
				"anullsrc",
				"-i",
				self._main_temp,
				"-vcodec",
				"copy",
				"-acodec",
				"aac",
				"-map",
				"0:a",
				"-map",
				"1:v",
				"-shortest",
				self._second_temp
			]
		# Running command
		run = sp.run(
			command,
			stderr=sp.PIPE
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise FFmpegError(run.stderr.decode())
		shutil.move(self._second_temp, self._main_temp)

	def removeAudio(
		self
	):
		"""
		Description
		--------------------------
		Remove audio on the video
		"""
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-c",
			"copy",
			"-an",
			"-v",
			"error",
			self._second_temp,
			"-y"
		]
		# Running command
		run = sp.run(
			command,
			stderr=sp.PIPE
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise FFmpegError(run.stderr.decode())
		shutil.move(self._second_temp, self._main_temp)

	def convert(
		self,
		container: str = "mp4",
		vcodec: str = "copy",
		acodec: str = "copy"
	):
		"""
		Description
		--------------------------
		Converting video to different container and/or codec.

		Argument(s)
		--------------------------
		container: File format where the data streams will be embedded.
		vcodec: The way to encode/decode video data stream. Refers to FFmpeg video codecs supported.
		acodec: The way to encode/decode audio data stream. Refers to FFmpeg audio codecs supported.
		"""
		current_container = os.path.splitext(self._main_temp)[1]
		# Verifying if current container is valid
		main_destination = self._second_temp
		if container != current_container:
			main_destination = os.path.join(self._temp_folder.name, "main." + container)
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-acodec",
			acodec,
			"-vcodec",
			vcodec,
			"-v",
			"error",
			main_destination,
			"-y"
		]
		# Running command
		run = sp.run(
			command,
			stderr=sp.PIPE
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise FFmpegError(run.stderr.decode())
		# Managing file based on container type
		if container != current_container:
			# Remove old container files
			if os.path.exists(self._main_temp):
				os.remove(self._main_temp)
			if os.path.exists(self._second_temp):
				os.remove(self._second_temp)
			# Affecting new container files to object
			self._main_temp = main_destination
			second_destination = os.path.join(self._temp_folder.name, "second." + container)
			self._second_temp = second_destination
		else:
			shutil.move(self._second_temp, self._main_temp)

	def resize(
		self,
		width: int,
		height: int,
		type: str = "simple"
	):
		"""
		Description
		--------------------------
		Resizing the video

		Argument(s)
		--------------------------
		width: Desired width of the video.
		height: Desired height of the video.
		type: Type of resizing. Available options: ["simple", "aspect_ratio"]
		"""
		# Verifying type
		types = ["simple", "aspect_ratio"]
		if type not in types:
			raise ValueError("Type should be one of {}, but yours is {}".format(types, type))
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp
		]
		if type == "simple":
			command.extend([
				"-vf",
				"scale=" + str(width) + ":" + str(height) + ":force_original_aspect_ratio=decrease,pad=" + str(width) + ":" + str(height) + ":(ow-iw)/2:(oh-ih)/2"
			])
		elif type == "aspect_ratio":
			command.extend([
				"-vf",
				"scale=" + str(width) + ":-2"
			])
		command.extend([
			"-v",
			"error",
			self._second_temp
		])
		# Running command
		run = sp.run(
			command,
			stderr=sp.PIPE
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise FFmpegError(run.stderr.decode())
		shutil.move(self._second_temp, self._main_temp)

	def changeFrameRate(
		self,
		fps: int = 30
	):
		"""
		Description
		--------------------------
		Changing frames per seconds of the video

		Argument(s)
		--------------------------
		fps: Desired frames per seconds.
		"""
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-filter:v",
			"fps=" + str(fps),
			"-v",
			"error",
			self._second_temp,
			"-y"
		]
		# Running command
		run = sp.run(
			command,
			stderr=sp.PIPE
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise FFmpegError(run.stderr.decode())
		shutil.move(self._second_temp, self._main_temp)

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
		# Creating temporary folder
		cwd = os.getcwd()
		self._temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		extension = os.path.splitext(path)[1]
		self._main_temp = os.path.join(self._temp_folder.name, "main" + extension)
		shutil.copy(path, self._main_temp)

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
				command,
				stderr=sp.PIPE
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise FFmpegError(run.stderr.decode())
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
				"error",
				str(self._second_temp),
				"-y"
			]
			# Running command
			run = sp.run(
				command,
				stderr=sp.PIPE
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise FFmpegError(run.stderr.decode())
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
				"error",
				self._second_temp,
				"-y"
			]
			# Running command
			run = sp.run(
				command,
				stderr=sp.PIPE
			)
			# Verifying if everything went well
			if run.returncode != 0:
				raise FFmpegError(run.stderr.decode())
			return Audio(self._second_temp)