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
		Initializing video composition.

		Parameters
		----------
		videos : list
			List of Video to concatenate in the right order.
		container : str, default="mp4"
			File format where the data streams will be embedded.
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
		Get the videos concatenated.

		Parameters
		----------
		width : int, default=1280
			Desired width of the video.
		height : int, default=720
			Desired height of the video.
		fps : int, default=30
			Desired frames per seconds.

		Returns
		-------
		Video
			Video containing the concatenation of the defined videos.
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
			if isAudio is False:
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
		filter_concat += "concat=n=" + \
			str(len(self._videos)) + ":v=1:a=1[outv][outa]"
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
		"""
		Initializing audio composition.

		Parameters
		----------
		audios : list
			List of Audio to concatenate in the right order.
		container : str, default="wav"
			File format where the data streams will be embedded.
		"""
		# Creating temporary folder
		cwd = os.getcwd()
		self._temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		self._output = os.path.join(self._temp_folder.name, "output." + container)
		self._audios = audios

	def get(
		self
	):
		"""
		Get the audios concatenated.

		Returns
		-------
		Audio
			Audio containing the concatenation of the defined audios.
		"""
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