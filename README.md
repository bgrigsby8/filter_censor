# Video Censorship Script

This Python script censors specific words in the audio of a video file by replacing them with a beep sound.

## Features

- Uses Whisper for speech recognition to identify words in the video.
- Replaces specific words in the audio with a beep sound.
- Outputs a new video file with censored audio.

## Requirements

- Python 3.7 or higher
- ffmpeg
- Whisper
- pydub

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install the dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `ffmpeg` is installed on your system. You can install it using:
   - On Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - On macOs: `brew install ffmpeg`
   - On Windows: Download it from FFMPEG's official site

## Usage

Run the script by passing the path to the input video file:

```bash
python script_name.py input_video.mp4
```

The output will be a new video file with `_edited` append to the original file name.

## License

This project is licensed under the MIT license
