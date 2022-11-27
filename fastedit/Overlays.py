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
			raise TypeError(
				"File format should be .srt or .ass, yours is {}".format(self._container)
			)
		# Creating temporary folder
		cwd = os.getcwd()
		self._temp_folder = tempfile.TemporaryDirectory(dir=cwd)
		# Defining temporary files
		self._path = os.path.join(
			self._temp_folder.name,
			"subtitles_" + str(id(self)) + self._container
		)
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


class Text():
	def __init__(
		self,
		text: str,
		x,
		y,
		start,
		end,
		fontSize: int = 18,
		fontColor: str = "white"
	):
		"""
		Initialize text.

		Parameters
		----------
		text : str
			String to display.
		x : int or str
			x-axis of the text.
		y : int or str
			y-axis of the text.
		start : int or float
			Start timestamp to start displaying the text.
		end : int or float
			End timestamp to end displaying the text.
		fontSize : int, default=18
			Size of the text's font.
		fontColor : str, default="white"
			Color of the text's font.
		"""
		# Verifying parameters' types
		coordinates = (int, str)
		timestamps = (int, float)
		if isinstance(text, str) is False:
			raise TypeError(
				"text should be str, yours is {}".format(type(text))
			)
		if isinstance(x, coordinates) is False:
			raise TypeError(
				"x should be in {}, yours is {}".format(coordinates, type(x))
			)
		if isinstance(y, coordinates) is False:
			raise TypeError(
				"y should be in {}, yours is {}".format(coordinates, type(y))
			)
		if isinstance(start, timestamps) is False:
			raise TypeError(
				"start should be in {}, yours is {}".format(timestamps, type(start))
			)
		if isinstance(end, timestamps) is False:
			raise TypeError(
				"end should be in {}, yours is {}".format(timestamps, type(end))
			)
		if isinstance(fontSize, int) is False:
			raise TypeError(
				"fontSize should be int, yours is {}".format(type(fontSize))
			)
		if isinstance(fontColor, str) is False:
			raise TypeError(
				"fontSize should be str, yours is {}".format(type(fontColor))
			)
		# Initializing Text
		self._text = {
			"text": text,
			"x": str(x),
			"y": str(y),
			"start": str(start),
			"end": str(end),
			"fontSize": str(fontSize),
			"fontColor": fontColor
		}

	def getText(
		self
	):
		"""
		Getting text with parameters.

		Returns
		-------
		dict
			Dictionnary containing the text and its parameters.
		"""
		return self._text