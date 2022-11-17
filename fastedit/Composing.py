from fastedit.Medias import Video, Audio
from fastedit.Errors import FFmpegError
import subprocess as sp
import tempfile
import os

class VideoComposition():
	def __init__(
		self,
		videos,
		container: str = "mp4"
	):
		"""
		Description
		--------------------------
		Initializing video compisition class

		Argument(s)
		--------------------------
		videos: List of Video to concatenate in the right order.
		container: File format where the data streams will be embedded. Default "mp4".
		"""
		# Creating temporary folder
		cwd = os.getcwd()
		self._temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		self._output = os.path.join(self._temp_folder.name, "output." + container)
		self._videos = videos

	def get(
		self,
		width: int = 1280,
		height: int = 720,
		fps: int = 30,
	):
		"""
		Description
		--------------------------
		Get the videos concatened

		Argument(s)
		--------------------------
		width: Desired width of the video.
		height: Desired height of the video.
		fps: Desired frames per seconds.
		"""
		# Setting the same dimension and frame rate
		isAudio = False
		for i in self._videos:
			isAudio = False
			metadata = i.getMetadata()
			for j in metadata['streams']:
				if j['codec_type'] == 'audio':
					isAudio = True
			i.resize(width, height)
			i.changeFrameRate(fps)
			if isAudio == False:
				i.addAudio(None, "silent")
		# Preparing command
		command = [
			"ffmpeg"
		]
		inputs = []
		filter_concat = ""
		for i in range(len(self._videos)):
			inputs.extend([
				"-i",
				self._videos[i]._main_temp
			])
			filter_concat += "[" + str(i) + ":v][" + str(i) + ":a]"
		filter_concat += "concat=n=" + str(len(self._videos)) + ":v=1:a=1[outv][outa]"
		end = [
			"-filter_complex",
			filter_concat,
			"-map",
			"[outv]",
			"-map",
			"[outa]",
			self._output,
			"-v",
			"error",
			"-y"
		]
		command.extend(inputs)
		command.extend(end)
		# Running command
		run = sp.run(
			command,
			stderr=sp.PIPE
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise FFmpegError(run.stderr.decode())
		return Video(self._output)

class AudioComposition():
	def __init__(
		self,
		audios,
		container: str = "wav"
	):
		# Creating temporary folder
		cwd = os.getcwd()
		self._temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		self._output = os.path.join(self._temp_folder.name, "output." + container)
		self._audios = audios

	def get(
		self
	):
		# Preparing command
		command = [
			"ffmpeg"
		]
		inputs = []
		filter_concat = ""
		for i in range(len(self._audios)):
			inputs.extend([
				"-i",
				self._audios[i]._main_temp
			])
			filter_concat += "[" + str(i) + ":0]"
		filter_concat += "concat=n=" + str(len(self._audios)) + ":v=0:a=1[out]"
		end = [
			"-filter_complex",
			filter_concat,
			"-map",
			"[out]",
			self._output,
			"-v",
			"error",
			"-y"
		]
		command.extend(inputs)
		command.extend(end)
		print(" ".join(command))
		# Running command
		run = sp.run(
			command,
			stderr=sp.PIPE
		)
		# Verifying if everything went well
		if run.returncode != 0:
			raise FFmpegError(run.stderr.decode())
		return Audio(self._output)