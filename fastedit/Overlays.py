import tempfile
import os
import shutil

class Subtitles():
	def __init__(
		self,
		subtitles: str
	):
		"""
		Initialize subtitles.

		Parameters
		----------
		subtitles : str
			Path to the file containing the subtitles.
		"""
		# Verifying subtitles file format
		self._container = os.path.splitext(subtitles)[1]
		if self._container not in [".srt", ".ass"]:
			raise TypeError("File format should be .srt or .ass, yours is {}".format(self._container))
		# Creating temporary folder
		cwd = os.getcwd()
		self._temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		self._path = os.path.join(self._temp_folder.name, "subtitles_" + str(id(self)) + self._container)
		shutil.copy(subtitles, self._path)
	
	def getPath(
		self
	):
		"""
		Getting subtitles path.

		Returns
		-------
		str
			Path to the subtitles file.
		"""
		return self._path