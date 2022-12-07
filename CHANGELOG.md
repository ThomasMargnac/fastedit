## v0.6.0 (2022-12-07)

### Feat

- **Medias**: Verifying parameters type
- **Video**: Adding inplace parameter

## v0.5.2 (2022-12-04)

### Fix

- **Video**: Fixing bug on addAudio() related to subtitles
- **Video**: Mapping subtitles (if they exist) to the destination file
- **Video**: Removing copy of subtitles while looping or clipping
- **Video**: Fixing convert() bug related to file format

### Refactor

- Refactoring code to respect PEP8
- Refactoring code to repect more PEP8
- **tests**: Refactoring tests folder

## v0.5.1 (2022-11-26)

### Fix

- **Video**: Fixing problem that did not keep subtitles during video changes

## v0.5.0 (2022-11-24)

### Feat

- **Video,Overlays**: Adding Text Object and addText() method
- **Video**: Improving addSubtitles() with soft subtitles
- **Video,Subtitles**: Adding method to add hard subtitles to a video

### Fix

- **Media**: Fixing saving problem with subtitles

## v0.4.0 (2022-11-17)

### Feat

- **AudioComposition**: Create AudioComposition class
- **VideoComposition**: Creating VideoComposition
- **Video**: Adding changeFrameRate() method
- **Video**: Adding resize() method
- **Video**: Adding possibility to add silent audio
- **Media**: Adding changeVolume() method
- **Errors**: Adding FFprobeError
- **Medias**: Change verbose type from quiet to error
- **Video**: Adding convert() method
- **Video,Audio**: Adding getMetadata() method

### Fix

- **Composing,Errors**: Removing VideoConcatError
- **Medias**: Fixing overwriting on each method
