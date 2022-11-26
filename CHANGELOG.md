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
