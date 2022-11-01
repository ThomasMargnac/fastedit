import subprocess as sp

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
		self.__original_video_path = path
		self.__main_temp_video_path = ""
		self.__second_temp_video_path = ""

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
			str(self.__main_temp_video_path),
			"-show_entries",
			"format=duration",
			"-v",
			"quiet",
			"-of",
			"csv='p=0'"
		]
		# Running command and getting output in pipe
		run = sp.Popen(
			command,
			stdout=sp.PIPE,
			stderr=sp.PIPE
		)
		# Reading stout
		print(run.returncode)
		out, err = run.communicate()
		print(out, err)

	def adjustDuration(
		self,
		duration,
		start = 0
	):
		"""
		Description
		--------------------------
		Create a loop from a video

		Argument(s)
		--------------------------
		duration: Duration of the new video.
		start: Start time of the video where the video start playing. Default 0.
		"""
		# Getting the user's desired duration
		desiredDuration = start + duration
		# Getting the actual video duration
		videoDuration = self.getDuration()
		# Apply transformation on video based on 
		if desiredDuration < videoDuration:
			# ffmpeg -i <entry> -ss <start> -to <end> test.mp4
			command = [
				"ffmpeg",
				"-i",
				str(self.__main_temp_video_path),
				"-ss",
				str(start),
				"-to",
				str(desiredDuration),
				str(self.__second_temp_video_path)
			]
		elif desiredDuration > videoDuration:
			print("test")

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