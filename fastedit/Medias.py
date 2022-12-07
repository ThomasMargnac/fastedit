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
		# Verifying parameters
		if not isinstance(path, str):
			raise TypeError(
				"path must be str, yours is {}".format(type(path))
			)
		if not os.path.exists(path):
			raise ValueError(
				"{} is not a valid path".format(path)
			)
		# Creating temporary folder
		cwd = os.getcwd()
		self._temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		extension = os.path.splitext(path)[1]
		self._main_temp = os.path.join(self._temp_folder.name, "main" + extension)
		shutil.copy(path, self._main_temp)
		self._second_temp = os.path.join(
			self._temp_folder.name,
			"second" + extension
		)

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
		# Verifying parameters
		if not isinstance(path, str):
			raise TypeError(
				"path must be str, yours is {}".format(type(path))
			)
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
		# Verifying parameters
		if not isinstance(volume, (int, float)):
			raise TypeError(
				"volume must be int or float, yours is {}".format(type(volume))
			)
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
		duration,
		inplace: bool = False
	):
		"""
		Create a loop from a video.

		Parameters
		----------
		duration : int or float
			Duration of the loop.
		inplace : bool, default=False
			If True, applying changes to the current object. \
			If False, create a new Video to apply changes.

		Returns
		-------
		Video or None
			If "inplace" is False, it returns a Video containing the video looped. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(duration, (int, float)):
			raise TypeError(
				"Duration must be int or float, "
				"yours is {}".format(type(duration))
			)
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
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
			# Managing files
			if inplace is False:
				return Video(self._second_temp)
			else:
				shutil.move(self._second_temp, self._main_temp)

	def clip(
		self,
		start,
		end,
		inplace: bool = False
	):
		"""
		Extract a part of the video.

		Parameters
		----------
		start : int or float
			Time where the clip starts in seconds.
		end : int or float
			Time where the clip ends in seconds.
		inplace : bool, default=False
			If True, applying changes to the current object. \
			If False, create a new Video to apply changes.

		Returns
		-------
		Video or None
			If "inplace" is False, it returns a Video containing the video clipped. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(start, (int, float)):
			raise TypeError(
				"start must be int or float, "
				"yours is {}".format(type(start))
			)
		if not isinstance(end, (int, float)):
			raise TypeError(
				"end must be int or float, "
				"yours is {}".format(type(end))
			)
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
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
			# Managing files
			if inplace is False:
				return Video(self._second_temp)
			else:
				shutil.move(self._second_temp, self._main_temp)

	def addAudio(
		self,
		audio,
		strategy: str = None,
		inplace: bool = True
	):
		"""
		Add or replace audio on the video.

		Parameters
		----------
		audio : Audio or None
			Audio instance you want to add.
		strategy : str
			Method to add audio. Available options : \
			"replace", "add", "combine" or "silent".
		inplace : bool, default=True
			If True, applying changes to the current object. \
			If False, create a new Video to apply changes.

		Returns
		-------
		Video or None
			If "inplace" is False, it returns a Video containing the new audio. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(audio, (Audio, type(None))):
			raise TypeError(
				"audio must be Audio, yours is {}".format(type(audio))
			)
		types = ["replace", "add", "combine", "silent"]
		if strategy not in types:
			raise ValueError(
				"Type should be one of {}, but yours is {}".format(types, strategy)
			)
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
		# Preparing command
		if audio is not None:
			command = [
				"ffmpeg",
				"-i",
				self._main_temp,
				"-i",
				audio._main_temp
			]
			# The user wants to replace the original audio
			if strategy == "replace":
				end = [
					"-map",
					"0:v",
				]
				# Checking if there's subtitles and if needed map them
				for item in self.getMetadata()["streams"]:
					if item['codec_type'] == 'subtitle':
						end.extend([
							"-map",
							"0:s"
						])
						break
				end.extend([
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
				])
				command.extend(end)
			# The user wants to add another audio file to the video
			elif strategy == "add":
				end = [
					"-map",
					"0",
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
			# The user wants to combine the original audio with another audio file
			elif strategy == "combine":
				end = [
					"-filter_complex",
					"[0:a][1:a]amerge=inputs=2[a]",
					"-map",
					"0:v"
				]
				# Checking if there's subtitles and if needed map them
				for item in self.getMetadata()["streams"]:
					if item['codec_type'] == 'subtitle':
						end.extend([
							"-map",
							"0:s"
						])
						break
				end.extend([
					"-map",
					"[a]",
					"-vcodec",
					"copy",
					"-c:s",
					"copy",
					"-ac",
					"2",
					"-v",
					"error",
					self._second_temp,
					"-y"
				])
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
				"-c:s",
				"copy",
				"-map",
				"0:a",
				"-map",
				"1:v",
			]
			# Checking if there's subtitles and if needed map them
			for item in self.getMetadata()["streams"]:
				if item['codec_type'] == 'subtitle':
					command.extend([
						"-map",
						"1:s"
					])
					break
			command.extend([
				"-shortest",
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
		# Managing files
		if inplace is False:
			return Video(self._second_temp)
		else:
			shutil.move(self._second_temp, self._main_temp)

	def removeAudio(
		self,
		inplace: bool = True
	):
		"""
		Remove audio on the video.

		Parameters
		----------
		inplace : bool, default=True
			If True, applying changes to the current object. \
			If False, create a new Video to apply changes.

		Returns
		-------
		Video or None
			If "inplace" is False, it returns a Video \
			containing the video without audio. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
		# Preparing command
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
		# Managing files
		if inplace is False:
			return Video(self._second_temp)
		else:
			shutil.move(self._second_temp, self._main_temp)

	def convert(
		self,
		container: str = "mp4",
		vcodec: str = "copy",
		acodec: str = "copy",
		inplace: bool = True
	):
		"""
		Convert video to different container and/or codec.

		Parameters
		----------
		container : str, default="mp4"
			File format where the data streams will be embedded.
		vcodec : str, default="copy"
			The way to encode/decode video data stream. \
			Refers to FFmpeg video codecs supported.
		acodec : str, default="copy"
			The way to encode/decode audio data stream. \
			Refers to FFmpeg audio codecs supported.
		inplace : bool, default=True
			If True, applying changes to the current object. \
			If False, create a new Video to apply changes.

		Returns
		-------
		Video or None
			If "inplace" is False, it returns a Video containing the video converted. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(container, str):
			raise TypeError(
				"container must be str, yours is {}".format(type(container))
			)
		if not isinstance(vcodec, str):
			raise TypeError(
				"vcodec must be str, yours is {}".format(type(vcodec))
			)
		if not isinstance(acodec, str):
			raise TypeError(
				"acodec must be str, yours is {}".format(type(acodec))
			)
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
		current_container = os.path.splitext(self._main_temp)[1]
		# Verifying if current container is valid
		main_destination = self._second_temp
		video_format = "." + container
		if video_format != current_container:
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
		if video_format != current_container:
			# Managing files
			if inplace is False:
				return Video(main_destination)
			else:
				# Remove old container files
				if os.path.exists(self._main_temp):
					os.remove(self._main_temp)
				if os.path.exists(self._second_temp):
					os.remove(self._second_temp)
				# Affecting new container files to object
				self._main_temp = main_destination
				self._second_temp = os.path.join(
					self._temp_folder.name,
					"second." + container
				)
		else:
			# Managing files
			if inplace is False:
				return Video(self._second_temp)
			else:
				shutil.move(self._second_temp, self._main_temp)

	def resize(
		self,
		width: int,
		height: int,
		strategy: str = "simple",
		inplace: bool = True
	):
		"""
		Resize video.

		Parameters
		----------
		width : int
			Desired width of the video.
		height : int
			Desired height of the video.
		strategy : int, default="simple"
			Type of resizing. Available options: ["simple", "aspect_ratio"].
		inplace : bool, default=True
			If True, applying changes to the current object. \
			If False, create a new Video to apply changes.

		Returns
		-------
		Video or None
			If "inplace" is False, it returns a Video containing the video resized. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(width, int):
			raise TypeError(
				"width must be int, yours is {}".format(type(width))
			)
		if not isinstance(height, int):
			raise TypeError(
				"height must be int, yours is {}".format(type(height))
			)
		if not isinstance(strategy, str):
			raise TypeError(
				"strategy must be str, yours is {}".format(type(strategy))
			)
		types = ["simple", "aspect_ratio"]
		if strategy not in types:
			raise ValueError(
				"Type should be one of {}, but yours is {}".format(types, strategy)
			)
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp
		]
		if strategy == "simple":
			command.extend([
				"-vf",
				"scale=" + str(width) + ":" + str(height)
				+ ":force_original_aspect_ratio=decrease,pad="
				+ str(width) + ":" + str(height) + ":(ow-iw)/2:(oh-ih)/2"
			])
		elif strategy == "aspect_ratio":
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
		# Managing files
		if inplace is False:
			return Video(self._second_temp)
		else:
			shutil.move(self._second_temp, self._main_temp)

	def changeFrameRate(
		self,
		fps: int = 30,
		inplace: bool = True
	):
		"""
		Change video's frames per seconds.

		Parameters
		----------
		fps : int, default=30
			Desired frames per seconds.
		inplace : bool, default=True
			If True, applying changes to the current object. \
			If False, create a new Video to apply changes.

		Returns
		-------
		Video or None
			If "inplace" is False, it returns a Video \
			containing the video with the new frame rate. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(fps, int):
			raise TypeError(
				"fps must be int, yours is {}".format(type(fps))
			)
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
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
		# Managing files
		if inplace is False:
			return Video(self._second_temp)
		else:
			shutil.move(self._second_temp, self._main_temp)

	def addSubtitles(
		self,
		subtitles: Subtitles,
		strategy: str,
		channel: int = 0,
		lang: str = "eng",
		inplace: bool = True
	):
		"""
		Add subtitles to the video.

		Parameters
		----------
		subtitles : Subtitles
			Subtitles instance containing the subtitles.
		strategy : str
			Type of subtitles. Available options : ["hard", "soft"].\
			"hard" means subtitles are hard coded to the video.\
			"soft" means subtitles are not burned into a video, \
			they can be enabled and disabled during the video playback.
		channel : int, default=0
			If type is "soft", you have to specify the stream subtitle number\
			of these subtitles.
		lang : str, default="eng"
			If type is "soft", you have to specify the subtitle language \
			using the ISO 639 language code with 3 letters.
		inplace : bool, default=True
			If True, applying changes to the current object. \
			If False, create a new Video to apply changes.

		Returns
		-------
		Video or None
			If "inplace" is False, it returns a Video \
			containing the video with the subtitles. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(subtitles, Subtitles):
			raise TypeError(
				"subtitles must be Subtitles, yours is {}".format(type(subtitles))
			)
		if not isinstance(strategy, str):
			raise TypeError(
				"strategy must be str, yours is {}".format(type(strategy))
			)
		types = ["hard", "soft"]
		if strategy not in types:
			raise ValueError(
				"Type of subtitles should be in {} but yours is {}".format(types, strategy)
			)
		if not isinstance(channel, int):
			raise TypeError(
				"channel must be int, yours is {}".format(type(channel))
			)
		if not isinstance(lang, str):
			raise TypeError(
				"lang must be str, yours is {}".format(type(lang))
			)
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
		# Preparing command
		command = [
			"ffmpeg",
			"-i",
			self._main_temp
		]
		filter = []
		if strategy == "hard" and subtitles._container == ".srt":
			filter = [
				"-vf",
				"subtitles=" + "'" + subtitles.getPath() + "'"
			]
		elif strategy == "hard" and subtitles._container == ".ass":
			filter = [
				"-vf",
				"ass=" + "'" + subtitles.getPath() + "'"
			]
		elif strategy == "soft":
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
		# Managing files
		if inplace is False:
			return Video(self._second_temp)
		else:
			shutil.move(self._second_temp, self._main_temp)

	def addText(
		self,
		texts: list,
		inplace: bool = True
	):
		"""
		Add text(s) in the video.

		Parameters
		----------
		text : list[Texts]
			List of text(s) to display on the video.
		inplace : bool, default=True
			If True, applying changes to the current object. \
			If False, create a new Video to apply changes.

		Returns
		-------
		Video or None
			If "inplace" is False, it returns a Video containing the video with texts. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not all(isinstance(item, Text) for item in texts):
			raise TypeError("texts' items should be Text object, at least one of \
				yours is not a Text object")
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
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
			filters += "drawtext=text='{}':x={}:y={}:fontsize={}:fontcolor={}\
				:enable='between(t,{},{})'".format(
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
		# Managing files
		if inplace is False:
			return Video(self._second_temp)
		else:
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
		duration : int or float
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
		# Verifying parameters
		if not isinstance(duration, (int, float)):
			raise TypeError(
				"duration must be int or float, yours is {}".format(type(duration))
			)
		if not isinstance(fps, int):
			raise TypeError(
				"fps must be int, yours is {}".format(type(fps))
			)
		if not isinstance(height, int):
			raise TypeError(
				"height must be int, yours is {}".format(type(height))
			)
		if not isinstance(width, int):
			raise TypeError(
				"width must be int, yours is {}".format(type(width))
			)
		if not isinstance(pix_fmt, str):
			raise TypeError(
				"pix_fmt must be str, yours is {}".format(type(pix_fmt))
			)
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
		duration,
		inplace: bool = False
	):
		"""
		Create a loop of the audio.

		Parameters
		----------
		duration : int or float
			Duration of the loop.
		inplace : bool, default=False
			If True, applying changes to the current object. \
			If False, create a new Audio to apply changes.

		Returns
		-------
		Audio or None
			If "inplace" is False, it returns an Audio containing the audio looped. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(duration, (int, float)):
			raise TypeError(
				"duration must be int or float, "
				"yours is {}".format(type(duration))
			)
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
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
			# Managing files
			if inplace is False:
				return Audio(self._second_temp)
			else:
				shutil.move(self._second_temp, self._main_temp)

	def clip(
		self,
		start,
		end,
		inplace: bool = False
	):
		"""
		Extract a part of the audio.

		Parameters
		----------
		start : int or float
			Time where the clip starts.
		end : int or float
			Time where the clip ends.
		inplace : bool, default=False
			If True, applying changes to the current object. \
			If False, create a new Audio to apply changes.

		Returns
		-------
		Audio or None
			If "inplace" is False, it returns an Audio containing the audio clipped. \
			If "inplace" is True, it returns nothing.
		"""
		# Verifying parameters
		if not isinstance(start, (int, float)):
			raise TypeError(
				"start must be int or float, yours is {}".format(type(start))
			)
		if not isinstance(end, (int, float)):
			raise TypeError(
				"end must be int or float, yours is {}".format(type(end))
			)
		if not isinstance(inplace, bool):
			raise TypeError(
				"inplace must be bool, yours is {}".format(type(inplace))
			)
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
			# Managing files
			if inplace is False:
				return Audio(self._second_temp)
			else:
				shutil.move(self._second_temp, self._main_temp)