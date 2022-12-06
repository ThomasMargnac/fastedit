# FastEdit

[![GitHub](https://img.shields.io/github/license/ThomasMargnac/fastedit?color=blue)](https://www.apache.org/licenses/LICENSE-2.0)
[![build](https://github.com/ThomasMargnac/fastedit/actions/workflows/ci.yml/badge.svg)](https://github.com/ThomasMargnac/fastedit/actions/workflows/ci.yml)
[![PyPI](https://badge.fury.io/py/fastedit.svg)](https://badge.fury.io/py/fastedit)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastedit)

FastEdit is a Python library to edit videos. Thanks to it you can manipulate videos and/or audios with actions such as cut, loop, or concatenate.

# Installation

FastEdit is based on FFmpeg which means it has to be installed on your machine before using FastEdit.

### Using `pip`

If `pip` is installed on your machine, you can install FastEdit by typing the following command:

```
pip install fastedit
```

If you want a specific version of FastEdit via `pip`, type the following command:

```
pip install fastedit==VERSION
```

If you want to install FastEdit from this GitHub repository, type the following command:

```
pip install git+https://github.com/ThomasMargnac/fastedit@main
```

### Try your first FastEdit program

```python
from fastedit.Medias import Video

video = Video("video.mp4")
clip = video.clip(0, 10)
clip.save("new_video.mp4")
```

For more information and examples, checkout the [wiki](https://github.com/ThomasMargnac/fastedit/wiki/Getting-started).

# Resources

|Type|Link|
|:---:|:---:|
|📚 **Wiki**|[GitHub Wiki](https://github.com/ThomasMargnac/fastedit/wiki)|
|🛠 **API Reference**|[GitHub Page](https://thomasmargnac.github.io/fastedit/)|
|🚨 **Bug Reports**|[GitHub Issue Tracker](https://github.com/ThomasMargnac/fastedit/issues)|