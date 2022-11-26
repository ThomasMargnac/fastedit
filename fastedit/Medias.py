import subprocess as sp
import tempfile
import shutil
import json
import os
from fastedit.Errors import FFmpegError, FFprobeError
from fastedit.Overlays import Subtitles, Text

class Media():
	def __init__(
		self,
		path: str
	):
		"""
		Initializing media.

		Parameters
		----------
		path : str
			Path to the media file.
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
		Get current media duration.

		Returns
		-------
		float
			Duration of the media.
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
		Get current media metadata.

		Returns
		-------
		dict
			Metadata of the media.
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
		path: str
	):
		"""
		Saving the media to the file system.

		Parameters
		----------
		path : str
			Path to the file to save the media.
		"""
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-c",
			"copy",
			"-c:s",
			"copy",
			"-v",
			"error",
			path,
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

	def changeVolume(
		self,
		volume
	):
		"""
		Change the volume of the audio.

		Parameters
		----------
		volume : int or float
			Factor by which the volume will be changed.
		"""
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-filter:a",
			"volume=" + str(volume),
			"-c:s",
			"copy",
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
		path: str
	):
		"""
		Initializing video.

		Parameters
		----------
		path : str
			Path to the video file.
		"""
		# Initializing object
		super().__init__(path)

	def loop(
		self,
		duration
	):
		"""
		Create a loop from a video.

		Parameters
		----------
		duration : int or float
			Duration of the loop.
		
		Returns
		-------
		Video
			Video containing the video looped.
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
				"-c:s",
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
		Extract a part of the video.

		Parameters
		----------
		start : int or float
			Time where the clip starts in seconds.
		end : int or float
			Time where the clip ends in seconds.
		
		Returns
		-------
		Video
			Video containing the video clipped.
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
				"-c:s",
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
		Add or replace audio on the video.

		Parameters
		----------
		audio : Audio
			Audio instance you want to add.
		type : str
			Method to add audio. Available options : "replace", "add", "combine" or "silent".
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
					"-c:s",
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
		Remove audio on the video.
		"""
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-c",
			"copy",
			"-c:s",
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
		Convert video to different container and/or codec.

		Parameters
		----------
		container : str, default="mp4"
			File format where the data streams will be embedded.
		vcodec : str, default="copy"
			The way to encode/decode video data stream. Refers to FFmpeg video codecs supported.
		acodec : str, default="copy"
			The way to encode/decode audio data stream. Refers to FFmpeg audio codecs supported.
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
			"-c:s",
			"copy",
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
		Resize video.

		Parameters
		----------
		width : int
			Desired width of the video.
		height : int
			Desired height of the video.
		type : int, default="simple"
			Type of resizing. Available options: ["simple", "aspect_ratio"].
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
			"-c:s",
			"copy",
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
		Change video's frames per seconds.

		Parameters
		----------
		fps : int, default=30
			Desired frames per seconds.
		"""
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-filter:v",
			"fps=" + str(fps),
			"-c:s",
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
		shutil.move(self._second_temp, self._main_temp)

	def addSubtitles(
		self,
		subtitles: Subtitles,
		type: str,
		channel: int = 0,
		lang: str = "eng",
	):
		"""
		Add subtitles to the video.

		Parameters
		----------
		subtitles : Subtitles
			Subtitles instance containing the subtitles.
		type : str
			Type of subtitles. Available options : ["hard", "soft"]. "hard" means subtitles are hard coded to the video. "soft" means subtitles are not burned into a video, they can be enabled and disabled during the video playback.
		channel : int, default=0
			If type is "soft", you have to specify the stream subtitle number of these subtitles.
		lang : str, default="eng"
			If type is "soft", you haveto specify the subtitle language using the ISO 639 language code with 3 letters.
		"""
		# Verifying type parameter
		if type not in ["hard", "soft"]:
			raise ValueError("Type of subtitles should be in [\"hard\", \"soft\"] but yours is {}".format(type))
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp
		]
		filter = []
		if type == "hard" and subtitles._container == ".srt":
			filter = [
				"-vf",
				"subtitles=" + "'" + subtitles.getPath() + "'"
			]
		elif type == "hard" and subtitles._container == ".ass":
			filter = [
				"-vf",
				"ass=" + "'" + subtitles.getPath() + "'"
			]
		elif type == "soft":
			filter = [
				"-i",
				subtitles.getPath(),
				"-metadata:s:s:" + str(channel),
				"language=" + str(lang),
				"-map",
				"0",
				"-map",
				"1",
				"-c",
				"copy",
				"-c:s",
				"mov_text"
			]
		else:
			raise TypeError("Something went wrong")
		end = [
			self._second_temp,
			"-v",
			"error",
			"-y"
		]
		# Concatenating command with filter and end
		command.extend(filter)
		command.extend(end)
		# Running command
		run = sp.run(
			command,
			stderr=sp.PIPE
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise FFmpegError(run.stderr.decode())
		shutil.move(self._second_temp, self._main_temp)

	def addText(
		self,
		texts: list[Text]
	):
		"""
		Add text(s) in the video.

		Parameters
		----------
		text : list[Texts]
			List of text(s) to display on the video.
		"""
		# Verifying texts type
		if all(isinstance(item, Text) for item in texts) == False:
			raise TypeError("texts' items should be Text object, at least one of yours is not a Text object")
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp,
			"-vf"
		]
		# Adding all the texts in the list
		filters = ""
		for i in range(len(texts)):
			parameters = texts[i].getText()
			filters += "drawtext=text='{}':x={}:y={}:fontsize={}:fontcolor={}:enable='between(t,{},{})'".format(
				parameters["text"],
				parameters["x"],
				parameters["y"],
				parameters["fontSize"],
				parameters["fontColor"],
				parameters["start"],
				parameters["end"]
			)
			if i < len(texts) - 1:
				filters += ","
		# Concatenating filters
		command.extend([
			filters,
			self._second_temp,
			"-c:s",
			"copy",
			"-v",
			"error",
			"-y"
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

class Image():
	def __init__(
		self,
		path: str
	):
		"""
		Initializing Image.

		Parameters
		----------
		path : str
			Path to the Image file.
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
		Convert Image to Video.

		Parameters
		----------
		duration : int
			Duration of the video in seconds.
		fps : int, default=30
			Framerate of the video.
		height : int, default=720
			Height of the video.
		width : int, default=1280
			Width of the video.
		pix_fmt : str, default="yuv420p"
			Pixel format of the video.
		
		Returns
		-------
		Video
			Video containing the image.
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
		path: str
	):
		"""
		Initializing audio.

		Parameters
		----------
		path : str
			Path to the audio file.
		"""
		# Initializing object
		super().__init__(path)
	
	def loop(
		self,
		duration
	):
		"""
		Create a loop of the audio.

		Parameters
		----------
		duration : int or float
			Duration of the loop.
		
		Returns
		-------
		Audio
			Audio containing the audio looped.
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
		Extract a part of the audio.

		Parameters
		----------
		start : int or float
			Time where the clip starts.
		end : int or float
			Time where the clip ends.
		
		Returns
		-------
		Audio
			Audio containing the audio clipped.
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