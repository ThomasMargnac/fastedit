class FFmpegError(Exception):
    """Raised when something went wrong with FFmpeg"""

class FFprobeError(Exception):
    """Raised when something went wrong with FFprobe"""

class VideoConcatError(Exception):
    """Raised when something went wrong when concating videos"""